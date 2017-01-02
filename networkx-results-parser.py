import sys
import os
import csv


#Program to parse the results of the NetworkX analyzer program that 
# collected memory consumption and elapsed time data from parsing
# input CSV graph files.


############################################################
def isNotEmpty(s):
    return bool(s and s.strip())


############################################################
def createFilePath( fileName, path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print("script_dir = %s" % script_dir)
    
    #get path to output path + file:
    dest_dir = os.path.join(script_dir, path)
    if debug: print("dest_dir = %s" % dest_dir)
    
    #attempt to make the directory, if it doesn't already exist:
    try:
        os.makedirs(dest_dir)
        if debug: print("created directory: %s" % dest_dir)
    except OSError:
        if debug: print("directory already exists?: %s" % dest_dir )
        pass    #path already exists

    finalPathFileName = os.path.join( dest_dir, fileName )
    return finalPathFileName


############################################################
def checkFilePath( fileName, path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print("script_dir = %s" % script_dir)
    
    #get path to output path + file:
    dest_dir = os.path.join(script_dir, path)
    if debug: print("dest_dir = %s" % dest_dir)
    
    #does path exist?
    if os.path.exists(dest_dir):
        
        #does target file exist?
        targetFile = os.path.join (dest_dir, fileName)
        if os.path.isfile(targetFile):
            if debug: print("found target file %s" % targetFile)
            return True
        else:
            print("target file %s does not exist." % targetFile)
            return False
    else: 
        print("path %s does not exist." % dest_dir)
        return False


############################################################
def checkPath( path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print("script_dir = %s" % script_dir)
    
    #get path to input path:
    input_dir = os.path.join(script_dir, path)
    if debug: print("target dir = %s" % input_dir)
    
    #does path exist?
    if os.path.exists(input_dir):
        
        if debug: print("found target input path %s" % input_dir)
        return True
        
    else: 
        print("Path %s does not exist." % input_dir)
        return False


############################################################
#def writeCsvFile( fileName, path, delimiter, maxWidth, maxHeight, matrix, debug=False ):
def writeCsvFile( fileNamePrefix, csvExtention, path, delimiter, maxWidth, maxHeight, matrix, debug=False ):

    csvFileName = fileNamePrefix + '.' + csvExtention
    
    finalPathFileName = createFilePath( csvFileName, path, debug)

    file = open(finalPathFileName, 'w')
    file.truncate() #delete existing file contents (if any)
    x,y = 0, 0
    delim = delimiter
    for y in range(maxHeight):
        line = ""
        for x in range(maxWidth):
            line += str(matrix[x][y])
            if (x < maxWidth-1):
                line = line + delim
            if (x >= maxWidth-1):
                file.write(line + "\n")
    file.close()
    return finalPathFileName #return output filename


############################################################
#
# Initial method to parse the data file.
# The data will come in a record block across multiple lines as follows, in this exact 
# order (and note, the record blocks can occur multiple times, per file):
#
#<start of file>
#
#<...snip...>
#
#<start of record block>
#
#   ALGORITHM|A-star
#   INFILECOUNTER|1
#   INFILENAME|large2000_1.csv
#   RESULTS|A-star|memoryConsumption(MB)|...
#   
#   Filename: networkx-docstudy.py
#   
#   Line #    Mem usage    Increment   Line Contents
#   ================================================
#      270  20.0078 MiB   0.0000 MiB   @profile(precision=4)
#      271                             def runAstar(state):
#   <snip...>
#      296 178.8203 MiB   0.0117 MiB       args = state[0]
#      297 178.8203 MiB   0.0000 MiB       args["pathLength"] = aStarPathLength
#      298 178.8203 MiB   0.0000 MiB       args["path"] = aStarPath
#      299 148.6953 MiB -30.1250 MiB       state[0] = args
#   
#   RESULTS|A-star|pathLength|3
#   RESULTS|A-star|path|[1, 1999, 1997, 1001]
#   RESULTS|A-star|elapsedTime|1.680891991
#
#<end of record block>
#
#<...snip...>
#
#<end of file>
#
# So the start of one reading begins with "ALGORITHM|<algorithm name>"
# And ends with "RESULTS|<algorithm name>|elapsedTime|<floating point value>"
# NOTE: The algorithm will differ per file, and there are 3 aforementioned algorithms.
#
# Thus, there are 5 core data points to derive from each record block that need
# to be saved and written to the target CSV file:
#
# (1) algorithm name (e.g., 'A-star', 'Bellman-Ford', or 'Dijkstra')
# (2) input file name -- as this can be useful for subsequent graph file post analysis.
# (3) memory consumption in MB (for that algorithm) -- this will be most complicated as it involves multiple lines.
# (4) path length (for that algorithm) -- an integer
# (5) elapsedTime in seconds (for that algorithm)
#
# Currently, we don't care about the actual node path. 
# We marginally care about the path length only because these may be interesting from
# a statistical analysis perspective, as these records may be "outliers" in MANOVA.
#
def parseFile( inPathFile, path, outCsvFileNamePrefix, outCsvFileExt, algorithm = 'A-star', debug=False):

    outCsvPathFileName = createFilePath ( (outCsvFileNamePrefix + outCsvFileExt), path, debug)
    outFile = open(outCsvPathFileName, 'wt')    #will overwrite existing file (if there)
    #write column header line (comma separated) to the output file:
    #headerLine = 'ALGORITHM,FILE_NAME,PATH_LENGTH,ELAPSED_TIME,MEMORY_CONSUMED,MIN_MEMORY,MAX_MEMORY\n'
    headerLine = 'ALGORITHM,FILE_NAME,PATH_LENGTH,ELAPSED_TIME,MEMORY_CONSUMED\n'
    outFile.write( headerLine )


    with open( inPathFile, 'rt') as inFile:
        
        count = 0
        buffer = []
        
        algName = ''
        graphFileName = ''
        pathLength = ''
        elapsedTime = ''
        memoryConsumed = '0.0'
        #minMemory = '0.0'
        #maxMemory = '0.0'

        buffering = False

        for line in inFile:
            count = count+1
            #print("%d>>%s" % (count,line) )
            
            #do some parsing...
            line = line.strip()
            
            if buffering == True:
                #While buffering, did we reach the next section?
                if line.startswith('RESULTS|' + algorithm + '|pathLength|'):
                    #we reached the next section after memory consumption. 
                    #turn off buffering and move on.
                    
                    buffering = False #turn off line buffering, as we reached new section.
                    
                    #collect the pathLength data:
                    pathLength = parseLine( line, 3, '|', debug)
                    
                    #send the buffer to the memory processing function for parsing.
                    #memoryBuffList = parseEntireMemoryConsumptionBuffer( buffer, debug )
                    memoryBuffList = parseTargetedMemoryConsumptionBuffer( buffer, algorithm, debug )
                    memoryConsumed = memoryBuffList[0]
                    #minMemory = memoryBuffList[1]
                    #maxMemory = memoryBuffList[2]
                    
                #Else simply add the line to the buffer:
                else: buffer.append(line)

            else:
                #look for the Algorithm identifier line:
                if buffering == False and line.startswith('ALGORITHM|' + algorithm):
                    algName = algorithm
            
                elif buffering == False and line.startswith('INFILENAME|'):
                    graphFileName = parseLine( line, 1, '|', debug)

                #Get memory consumption data. Basically buffer all memory data until 
                # we reach the next section ('pathLength'). Then send the buffered data 
                # to the function which handles it.
                elif buffering == False and line.startswith('RESULTS|' + algorithm + '|memoryConsumption(MB)|'):
                    buffering = True
                    buffer.append(line)

                elif buffering == False and line.startswith('RESULTS|' + algorithm + '|pathLength|'):
                    pathLength = parseLine( line, 3, '|', debug)
            
                #elif buffering == False and line.startswith('RESULTS|' + algorithm + '|elapsedTime(ms)|'):
                elif buffering == False and line.startswith('RESULTS|' + algorithm + '|elapsedTime|'):
                    elapsedTime = parseLine( line, 3, '|', debug)
            
            
            
                #If we gathered all data, then write it to output CSV file:
                if isNotEmpty(algName) \
                    and isNotEmpty(graphFileName) \
                    and isNotEmpty(pathLength) \
                    and isNotEmpty(elapsedTime) \
                    and buffering == False and len(buffer) > 0:
                    #and buffering == False:
                
                    elapsedTime = format( float(elapsedTime), '.3f')
                    memoryConsumed = format( float(memoryConsumed), '.3f')
                    
                    #Write the combined line, comma-separated, to the target CSV file:
                    #dataLine = algName + ',' + graphFileName + ',' + pathLength + ',' + elapsedTime + ',' + memoryConsumed + ',' + minMemory + ',' + maxMemory + '\n'
                    dataLine = algName + ',' + graphFileName + ',' + pathLength + ',' + elapsedTime + ',' + memoryConsumed + '\n'
                    #print(">>dataLine = %s" % dataLine )
                    outFile.write( dataLine )
                
                    #clear out data for next iteration:
                    algName = ''
                    graphFileName = ''
                    pathLength = ''
                    elapsedTime = ''
                    memoryConsumed = '0.0'
                    #minMemory = '0.0'
                    #maxMemory = '0.0'
                    buffer = []
                    buffering = False


    print("\nCompleted processing input file: %s\n" % inPathFile)
    outFile.close()
    print("\nCompleted writing results to output file: %s\n" % outCsvPathFileName)

    return True


############################################################
#
# NOTE: the parameter 'indexFieldToExtract' is zero-based.
#
# WARNING: This is VERY fragile code. Any change to the NetworkX analyzer program 
# may break the parsing done in this function!
#
def parseLine( line, indexFieldToExtract=0, delimiter='', debug=False ):

    line = line.strip()
    
    #tokenize string by delimiter, then extract and return desired index field:
    if isNotEmpty(delimiter):
        data = line.split(delimiter)
    else:
        data = line.split()

    #if debug: print("Number tokens: %d, desired token index: %d" % (len(data), indexFieldToExtract) )
    ##if debug: print(">>line:%s" % data)

    if len(data) > indexFieldToExtract:
        return data[indexFieldToExtract]
    else:
        return ''


############################################################
#
# This function will gather all "Mem Usage" column values.
# Then it sorts them from the lowest to highest "MiB" value order.
# The minimum and maximum MiB values are saved, and the difference
# is calculated. All 3 values (min, max, diff) are returned.
#
# NOTE: because of the way the underlying MiB values were generated,
# this function could overstate the amount of memory consumed.
# A more specific memory consumption calculator would look at 
# specific MiB values for particular sub-functions called, not the
# entire pathfinding operation (which may include actions not 
# specific to the tested graph analysis framework or pathfinding 
# algorithm, but nonetheless had to occur for the pathfinding
# operation to commence).
#
# WARNING: This is VERY fragile code. Any change to the NetworkX analyzer program 
# may break the parsing done in this function!
#
def parseEntireMemoryConsumptionBuffer( buffer, debug=False ):

    consumed = 0.0
    min = 0.0
    max = 0.0
    #data = [consumed, min, max]
    data = [consumed]
    memory = []

    if len(buffer) > 0:
        if debug: print ("\n>>total buffer line count: %d" % len(buffer) )
        if debug: print (">>Parsing buffer contents (line by line):")
        count = 0
        for line in buffer:
            count += 1
            #if debug: print ("[%d]:%s" % (count, line) )

            line = line.strip()
            
            #each row of memory contents is space delimited. Tokenize it, then
            # get index 1 (the second item in row) if index 2 = 'MiB', as this row would 
            # contain pertinent memory data.
            unitOfMeasurement = parseLine(line, 2, '', debug)
            
            if unitOfMeasurement == 'MiB':
                #Got a row with memory data. Grab the contents at index 1.
                data = parseLine(line, 1, '', debug)
                data = float(data)
                #append the data to the memory list:
                memory.append( data )

        #done collecting data from each (relevant)row. Now process memory values:
        
        #can't use list.sort() as shown here: http://stackoverflow.com/questions/7301110/why-does-return-list-sort-return-none-not-the-list
        # Python is weird that way...
        memory = sorted(memory)
        if debug: print ("memory:"),
        if debug: print ( sorted(memory) ) 
        if debug: print ("memory list items: %d" % len(memory) )
        maximum = memory[ len(memory) -1]
        minimum = memory[0]
        consumed = maximum - minimum
        #consumed = format(consumed, '.1f') # format the floating point values
        #consumed = format(consumed, '.2f') # format the floating point values
        consumed = format(consumed, '.4f') # format the floating point values (bring it all through; let subsequent scripts/functions deal with it).

        if debug: print ("Memory: max = %f, min = %f, diff = %f" % (maximum, minimum, consumed) )
        #data = [str(consumed), str(minimum), str(maximum)]
        data = [str(consumed)]
        return data

    else:
        return data


############################################################
#
# The algorithm parameter can be one of the following:
#   'A-star', 'Bellman-Ford', or 'Dijkstra'
#
# Unlike the function "parseEntireMemoryConsumptionBuffer()",
# this function will search for specific lines within the memory
# buffer, so as to capture a more accurate reading on the amount of memory
# consumed by each pathfinding algorithm tested in the NetworkX graph
# analysis framework.
#
# This function will specific values of the "Increment" column, not the "Mem usage"
# column as is done in the other, more generic function 
# "parseEntireMemoryConsumptionBuffer()".
#
# The specific lines parsed from the buffer, in this function, will contain 
# the following substrings. Bellman-Ford is slightly different because the
# interface provided by NetworkX for the BellmanFord algorithm is different
# than the interfaces it provides for the A-star and Dijkstra algorithms:
#
# 1. For A-star pathfinding algorithm (5 lines):
#
#       "G = nx.Graph( input_data.values )"
#       "nodeList = G.nodes()"
#       "nodeListData = G.nodes(data=True)"
#       "aStarPath = nx.astar_path(G, startNode, destNode )"
#       "aStarPathLength = nx.astar_path_length(G, startNode, destNode )"
#
# 2. For Bellman-Ford pathfinding algorithm (4 lines):
#
#       "G = nx.Graph( input_data.values )"
#       "nodeList = G.nodes()"
#       "nodeListData = G.nodes(data=True)"
#       "pred, dist = nx.bellman_ford(G, startNode )"
#
# 3. For Dijkstra algorithm (5 lines):
#
#       "G = nx.Graph( input_data.values )"
#       "nodeList = G.nodes()"
#       "nodeListData = G.nodes(data=True)"
#       "dijkstraPath = nx.dijkstra_path(G, startNode, destNode )"
#       "dijkstraPathLength = nx.dijkstra_path_length(G, startNode, destNode )"
#
# WARNING: This is VERY fragile code. Any change to the NetworkX analyzer program 
# may break the parsing done in this function!
#
def parseTargetedMemoryConsumptionBuffer( buffer, algorithm = 'A-star', debug=False ):

    total = 0.0
    #min = 0.0
    #max = 0.0
    #data = [total, min, max]
    data = [total]
    memory = []

    if len(buffer) > 0:
        if debug: print ("\n>>total buffer line count: %d" % len(buffer) )
        if debug: print (">>Parsing buffer contents (line by line):")
        count = 0

        if debug: print ("Algorithm = %s" % algorithm)
        for line in buffer:
            count += 1
            #if debug: print ("[%d]:%s" % (count, line) )

            line = line.strip()

            #each row of memory contents is space delimited. Tokenize it, then
            # get index 3 (the fourth item in row) if index 4 = 'MiB', and if the
            # line contains one of the substrings in index 5, listed in the 
            # function comments above, for the pathfinding algorithm in question, 
            # then grab the memory data in the row at index 3, which is the memory
            # value for the 'Increment' column.
            unitOfMeasurement = parseLine(line, 4, '', debug)

            #Only the lines containing 'MiB' could possibly contain what we want...
            if unitOfMeasurement == 'MiB':
                #Got a row with memory data. 
                # Check the substring, per algorithm type.
                # If there is pathfinding algorithm-specific
                # substring match, then grab the 'Increment' column 
                # memory value.
                
                if algorithm == 'A-star':

                    substring1 = "G = nx.Graph( input_data.values )"
                    substring2 = "nodeList = G.nodes()"
                    #substring3 = "nodeListData = G.nodes(data=True)"
                    substring4 = "aStarPath = nx.astar_path(G, startNode, destNode )"
                    #substring5 = "aStarPathLength = nx.astar_path_length(G, startNode, destNode )"

                    if substring1 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring1) )
                        data = float(data)
                        memory.append( data )
                    
                    elif substring2 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring2) )
                        data = float(data)
                        memory.append( data )
                    
                    #elif substring3 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring3) )
                    #    data = float(data)
                    #    memory.append( data )
                    
                    elif substring4 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring4) )
                        data = float(data)
                        memory.append( data )
                    
                    #elif substring5 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring5) )
                    #    data = float(data)
                    #    memory.append( data )

                elif algorithm == 'Bellman-Ford':

                    substring1 = "G = nx.Graph( input_data.values )"
                    substring2 = "nodeList = G.nodes()"
                    #substring3 = "nodeListData = G.nodes(data=True)"
                    substring4 = "pred, dist = nx.bellman_ford(G, startNode )"
                    #substring5 = "while currNode != startNode:"
                    #substring6 = "bfPathLengthsAll = dict(dist)"

                    if substring1 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring1) )
                        data = float(data)
                        memory.append( data )
                    
                    elif substring2 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring2) )
                        data = float(data)
                        memory.append( data )
                    
                    #elif substring3 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring3) )
                    #    data = float(data)
                    #    memory.append( data )
                    
                    elif substring4 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring4) )
                        data = float(data)
                        memory.append( data )

                    #elif substring5 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring5) )
                    #    data = float(data)
                    #    memory.append( data )
                    #
                    #elif substring6 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring6) )
                    #    data = float(data)
                    #    memory.append( data )

                elif algorithm == 'Dijkstra':

                    substring1 = "G = nx.Graph( input_data.values )"
                    substring2 = "nodeList = G.nodes()"
                    #substring3 = "nodeListData = G.nodes(data=True)"
                    substring4 = "dijkstraPath = nx.dijkstra_path(G, startNode, destNode )"
                    #substring5 = "dijkstraPathLength = nx.dijkstra_path_length(G, startNode, destNode )"                

                    if substring1 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring1) )
                        data = float(data)
                        memory.append( data )
                    
                    elif substring2 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring2) )
                        data = float(data)
                        memory.append( data )
                    
                    #elif substring3 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring3) )
                    #    data = float(data)
                    #    memory.append( data )
                    
                    elif substring4 in line:
                        data = parseLine(line, 3, '', debug)
                        if debug: print ("found memory value: %s, for substring %s" % (data, substring4) )
                        data = float(data)
                        memory.append( data )
                    
                    #elif substring5 in line:
                    #    data = parseLine(line, 3, '', debug)
                    #    if debug: print ("found memory value: %s, for substring %s" % (data, substring5) )
                    #    data = float(data)
                    #    memory.append( data )

        #done collecting data from each (relevant)row. Now process memory values:

        #can't use list.sort() as shown here: http://stackoverflow.com/questions/7301110/why-does-return-list-sort-return-none-not-the-list
        # Python is weird that way...
        memory = sorted(memory)
        if debug: print ("memory (sorted):"),
        if debug: print ( sorted(memory) ) 
        if debug: print ("memory list items: %d" % len(memory) )
        #maximum = memory[ len(memory) -1 ]
        #minimum = memory[0]
        total = sum(memory)
        if debug: print ("Memory: total (before rounding) = %f" % total )
        #total = format(total, '.1f') # format the floating point values
        total = format(total, '.4f') # format the floating point values (bring it all through, let subsequent scripts/functions deal with it)
        #avg = float(total) / len(memory)

        #if debug: print ("Memory: total = %f, min = %f, max = %f, avg = %f" % (total, minimum, maximum, avg) )
        if debug: print ("Memory: total = %s" % total )
        #data = [str(total), str(minimum), str(maximum)]
        data = [ total ]
        return data

    else:
        return data


############################################################


# Main NetworkX Results Parser:
def run_parser():

    print ("\nUsage: %s [path to files: str] [input file: str] [output filename prefix: str] [algorithm: 1, 2 or 3] [debugMode: 0 or 1]" \
        % str(sys.argv[0]) )
    print ("e.g.,\n  python  %s  aSubDir  inFile.txt  outFileNamePrefix  1  0\n" \
        % str(sys.argv[0]) )

    path = str(sys.argv[1])
    if isNotEmpty(path) == False: path = "output"

    #get first command line parameter after script name
    inFileName = str(sys.argv[2])
    if isNotEmpty(inFileName) == False: 
        print("Error: input file name cannot be empty/null. Exiting.")
        sys.exit(1)

    outCsvFileNamePrefix = str(sys.argv[3])
    if isNotEmpty(outCsvFileNamePrefix) == False:
        outCsvFileNamePrefix = inFileName + "_parsed"  #give it a default name

    algorithm = int(sys.argv[4])
    if algorithm < 1: algorithm = 1
    if algorithm > 3: algorithm = 3
    algorithmName = ''
    if algorithm == 1: algorithmName = 'A-star'
    elif algorithm == 2: algorithmName = 'Bellman-Ford'
    elif algorithm == 3: algorithmName = 'Dijkstra'
    else: algorithmName = 'Unknown'

    debug = int(sys.argv[5])
    if debug == 1: debug = True
    elif debug == 0: debug = False
    else: debug = False

    advert = "(where 1 = A* (A-star), 2 = Bellman-Ford, 3 = Dijkstra)"
    print("Running with user-selected options:\n"),
    print("  filePath=%s\n  inFileName=%s\n  outCsvFileNamePrefix=%s\n  algorithm=%d  %s\n debugMode=%s\n" \
        % (path, inFileName, outCsvFileNamePrefix, algorithm, advert, debug) )

    outCsvFileExt = ".csv"

    inPathFile = os.path.join(path, inFileName)

    #does input data file exist?
    if checkFilePath( inFileName, path, debug) == False:
        print ("Input CSV file %s not found." % inPathFile )
        return False
    else:
        if debug: print("Found input CSV file %s" % inPathFile )

    #call method to parse file:
    parseFile( inPathFile, path, outCsvFileNamePrefix, outCsvFileExt, algorithmName, debug)


############################################################

if __name__ == '__main__':
    #print("In main()")
    run_parser()
