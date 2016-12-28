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
#
#   <...snip...>
#
#      296 178.8203 MiB   0.0117 MiB       args = state[0]
#      297 178.8203 MiB   0.0000 MiB       args["pathLength"] = aStarPathLength
#      298 178.8203 MiB   0.0000 MiB       args["path"] = aStarPath
#      299 148.6953 MiB -30.1250 MiB       state[0] = args
#   
#   RESULTS|A-star|pathLength|3
#   RESULTS|A-star|path|[1, 1999, 1997, 1001]
#   RESULTS|A-star|elapsedTime(ms)|1680.891991
#
#<end of record block>
#
#<...snip...>
#
#<end of file>
#
# So the start of one reading begins with "ALGORITHM|<algorithm name>"
# And ends with "RESULTS|<algorithm name>|elapsedTime(ms)|<floating point value>"
# NOTE: The algorithm will differ per file, and there are 3 aforementioned algorithms.
#
# Thus, there are 5 core data points to derive from each record block that need
# to be saved and written to the target CSV file:
#
# (1) algorithm name (e.g., 'A-star', 'Bellman-Ford', or 'Dijkstra')
# (2) input file name -- as this can be useful for subsequent graph file post analysis.
# (3) elapsedTime in milliseconds (for that algorithm)
# (4) memory consumption in MB (for that algorithm) -- this will be most complicated as it involves multiple lines.
# (5) path length (for that algorithm) -- an integer
#
# Currently, we don't care about the actual node path. 
# We marginally care about the path length only because these may be interesting from
# a statistical analysis perspective, as these records may be "outliers" in MANOVA.
#
def parseFile( inPathFile, path, outCsvFileNamePrefix, outCsvFileExt, algorithm = 'A-star', debug=False):

    outCsvPathFileName = createFilePath ( (outCsvFileNamePrefix + outCsvFileExt), path, debug)
    outFile = open(outCsvPathFileName, 'wt')    #will overwrite existing file (if there)
    #write column header line (comma separated) to the output file:
    headerLine = 'ALGORITHM,FILE_NAME,PATH_LENGTH,ELAPSED_TIME,MEMORY_CONSUMED\n'
    outFile.write( headerLine )


    with open( inPathFile, 'rt') as inFile:
        
        count = 0
        buffer = ()
        
        algName = ''
        graphFileName = ''
        pathLength = ''
        elapsedTime = ''
        memoryConsumed = '0.0'

        for line in inFile:
            count = count+1
            #print("%d>>%s" % (count,line) )
            
            #do some parsing...
            line = line.strip()
            
            #look for the Algorithm identifier line:
            if line.startswith('ALGORITHM|' + algorithm):
                algName = algorithm
            
            elif line.startswith('INFILENAME|'):
                graphFileName = parseLine( line, 1, '|', debug)
                
            elif line.startswith('RESULTS|' + algorithm + '|pathLength|'):
                pathLength = parseLine( line, 3, '|', debug)
            
            elif line.startswith('RESULTS|' + algorithm + '|elapsedTime(ms)|'):
                elapsedTime = parseLine( line, 3, '|', debug)
            
            #Get memory consumption data:
            
            
            #If we gathered all data, then write it to output CSV file:
            if isNotEmpty(algName) \
                and isNotEmpty(graphFileName) \
                and isNotEmpty(pathLength) \
                and isNotEmpty(elapsedTime):
                
                #Write the combined line, comma-separated, to the target CSV file:
                dataLine = algName + ',' + graphFileName + ',' + pathLength + ',' + elapsedTime + ',' + memoryConsumed + '\n'
                #print(">>dataLine = %s" % dataLine )
                outFile.write( dataLine )
                
                #clear out data for next iteration:
                algName = ''
                graphFileName = ''
                pathLength = ''
                elapsedTime = ''
                memoryConsump = ''


    print("\nCompleted processing input file: %s\n" % inPathFile)
    outFile.close()
    print("\nCompleted writing results to output file: %s\n" % outCsvPathFileName)

    return True


############################################################
#
# NOTE: the parameter 'indexFieldToExtract' is zero-based.
#
def parseLine( line, indexFieldToExtract=0, delimiter='|', debug=False ):

    #tokenize string by delimiter, then extract and return desired index field:
    data = line.split(delimiter)
    return data[indexFieldToExtract]


############################################################
def parseMultiLines( line, debug=False ):
    data = ''
    
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
