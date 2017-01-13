import random
import math
import pandas as pd
import networkx as nx
import pylab
from pylab import rcParams
import sys
import os


"""
Program to randomly select graph files (with either .CSV or .graphml file extention)
in a source directory, and move those (randomly selected) files to a target directory.

The purpose of doing this is to be able to randomly select graph files (i.e., samples)
from a source sub population that has already been stratified based on desired map 
attributes (e.g., size, complexity), and move those randomly selected files into other
folders that are for specific experimental treatment groups.

Although running this script is not required, if you want to randomly select samples
for your treatment groups, then this script is important. Else you can skip this script
and run your pathfinding tests on the file samples in the main population folder(s) (but
is not a recommended approach as randomization is important in experimental studies).

REQUIREMENT: This script requires that the "graph_generator.py" program be run first.


Steps to follow:

Prelude:
So lets say a population of 1000 graph files have been randomly generated (via the
script graph_generator.py), and half of those are of demographic type "small & simple", 
and the other half are of demographic type "large and complex".

First, outside this script, split population of files into two subdirectories, 
based on their demographic attributes: 
1. "small_and_simple" -- subdir has 500 files
2. "large_and_complex" -- subdir has the other 500 files
(Obviously, use more subdirectories, if you need to stratify into more subgroups.)

Second, determine how many treatment groups need samples from the subdir containing
files in the first demographic subgroup (in this case, "small and simple").
--> Let's say, 3 treatment groups need such files.

Third, create 2 (in this case) target directories for the small and simple files:
 a. mkdir "ss_1"  (for small & simple, treatment group #1)
 b. mkdir "ss_2"  (for small & simple, treatment group #2)
 c. mkdir "ss_3"  (for small & simple, treatment group #3)

Fourth, determine how many samples to randomly pull from the main sample demographic 
sub group (in this case, the small and simple files), to move into the first
treatment group subdirectory (i.e., "ss_1" for the small & simple treatment group #1).
--> Let's say we want 100 randomly selected files from the small and simple demographic 
subgroup (contained in the subdirectory "small_and_simple" described earlier), to go
into each of the small & simple treatment group folders ("ss_1", "ss_2" and "ss_3").

Fifth, run this program, using the input source directory "small_and_simple" since that 
has the entire population of 500 small and simple files, from which we will draw our
sample size of 100 per small & simple treatment group. 
And use the target directory "ss_1", as this is our first treatment group that needs
the small & simple samples.

Sixth, repeat step 5, but for the other "small & simple" treatment group(s), until 
all treatment groups have received their randomly selected stratified samples (where 
stratification was based on the demographic traits described in step 1 above).

Seventh, repeat steps 2 through 6, but for the other demographically stratified subgroup,
which in this case would be the "large and complex" files. 

Once all treatment group subdirectories have been populated with randomly selected files
that correspond to their required demographics, you can then serially run the pathfinding
algorithm tests on the samples in each of the treatment group subdirectories.

Done!

"""

############################################################
def isNotEmpty(s):
    return bool(s and s.strip())
    
############################################################
def printMatrix( maxWidth, maxHeight, matrix ):
    x,y = 0, 0
    for y in range(maxHeight):
        for x in range(maxWidth):
            print matrix[x][y],     #the ',' keeps printing on same line
        print   #now print new line to wrap the row.


############################################################
def removeLoops( maxWidth, maxHeight, matrix ):
    #Set the values of the main diagonal to zero to remove loops.
    newValue = 0
    x,y = 0, 0
    for y in range(maxHeight):
        for x in range(maxWidth):
            if x == y:
                matrix[x][y] = newValue
                #print "Setting cell [%d][%d] to %d" % (x, y, newValue)
    #print("Removed the self-loops (i.e., main diagonal cleared).")


############################################################
def createFilePath( fileName, path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print(">> script_dir = %s" % script_dir)
    
    #get path to output path + file:
    dest_dir = os.path.join(script_dir, path)
    if debug: print(">> dest_dir = %s" % dest_dir)
    
    #attempt to make the directory, if it doesn't already exist:
    try:
        os.makedirs(dest_dir)
        if debug: print(">> created directory: %s" % dest_dir)
    except OSError:
        if debug: print(">> directory already exists?: %s" % dest_dir )
        pass    #path already exists

    finalPathFileName = os.path.join( dest_dir, fileName )
    return finalPathFileName


############################################################
def checkFilePath( fileName, path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print(">> script_dir = %s" % script_dir)
    
    #get path to output path + file:
    dest_dir = os.path.join(script_dir, path)
    if debug: print(">> dest_dir = %s" % dest_dir)
    
    #does path exist?
    if os.path.exists(dest_dir):
        
        #does target file exist?
        targetFile = os.path.join (dest_dir, fileName)
        if os.path.isfile(targetFile):
            if debug: print(">> found target file %s" % targetFile)
            return True
        else:
            print(">> target file %s does not exist." % targetFile)
            return False
    else: 
        print(">> path %s does not exist." % dest_dir)
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
# This method assumes the input matrix is a k-regular matrix
# that has already been initialized to k-regular form.
#
# Variable 'prob' is a float, and represents the probability of 
# rewiring, a la Watts & Strogatz (1998) "small world" network style.
#
# This method doesn't change the main diagonal cells, to 
# prevent generation of self-loops.
#
def createSmallWorldMatrix( prob, maxWidth, maxHeight, matrix, debug=False ):
    # check boundaries:
    if prob < 0.0:  prob = 0.0      #a 0-percent chance of rewiring
    if prob > 1.0:  prob = 1.0      #a 100-percent chance of rewiring
    
    x,y = 0, 0
    for y in range(maxHeight):
        for x in range(maxWidth):
            #Ignore the main diagonal (where x = y), don't create self-loops:
            if x != y: 
                rand = random.random()
                if (rand <= prob) and matrix[x][y] != 0:
                
                    #time to rewire...
                    if debug==True:
                        print ("Rand = %f, Prob = %f. [x,y]: [%d,%d] = %d" % (rand, prob, x, y, matrix[x][y] ) )

                    #1. disconnect the 2-way (x,y) and (y,x) connections:
                    matrix[x][y] = 0
                    matrix[y][x] = 0
                    if debug==True:
                        print (">> Set [%d][%d] to 0, and [%d][%d] to 0" % (x,y,y,x) )
                    
                    
                    #2. find new random connection for (x,y) and (y,x), and ensure
                    # that we don't reconnect to the already existing links. 
                    newY = y
                    done = False
                    while done != True:
                        newY = random.randint(0, maxHeight-1)
                        
                        #Don't create edges to already existing edges, and don't
                        # create self-loops:
                        if y != newY and x != newY and matrix[x][newY] != 1 \
                            and matrix[newY][x] != 1:
                            done = True
                    
                    if debug==True:
                        print (">> original x,y = [%d][%d], and y,x = [%d][%d]" % (x,y,y,x) )
                        print (">> new [x]-->[y] = [%d][%d]" % (x, newY) )
                        print (">> new [y]-->[x] = [%d][%d]" % (newY, x) )
                    
                    # Now set new matrix cells to connected:
                    matrix[x][newY] = 1
                    matrix[newY][x] = 1


############################################################
#
# This method assumes the input matrix is initialized to zero.
# This method calls in the internal function _regularMatrixCalc()
# which does the actual link creation for the regular network graph.
#
def createRegularMatrix( k, maxWidth, maxHeight, matrix):

    #check the boundaries:
    if maxWidth < 5 or maxHeight < 5: maxWidth, maxHeight, k = 5, 5, 2
    if k < 1: k = 1
    if k > 4: k = 4
    print("Creating k-regular matrix with x = %d, y = %d, k = %d" % (width, height, k) )
    
    #Set the values of the main diagonal to zero to remove loops.
    removeLoops( maxWidth, maxHeight, matrix ) #clear the diagonal, just in case.

    #call the method that does the actual work.
    count = 1
    while count <= k:
        _regularMatrixCalc(count, maxWidth, maxHeight, matrix )
        count += 1


############################################################
#
# This internal method does the k-regular network link creation.
# It should only be called by the method createRegularMatrix().
#
def _regularMatrixCalc(k, maxWidth, maxHeight, matrix):

    #set the row k-below the diagonal to 1 (connected)
    x = 0
    y = k
    while y <= maxHeight-1:
        x = 0
        while x <= maxWidth-1:
            if y-x == (1*k):
                matrix[x][y] = 1
            x += 1
        y += 1

    #set the row k-above the diagonal to 1 (connected)
    x = k
    y = 0
    while y <= maxHeight-1:
        x = k
        while x <= maxWidth-1:
            if x-y == (1*k):
                matrix[x][y] = 1
            x += 1
        y += 1

    #now link the ends of the chain together (i.e., connect
    # the SW, and NE nodes in the matrix):
    count = 0
    while count < k:
        matrix[count][maxHeight - k + count] = 1
        matrix[maxWidth - k + count][count] = 1
        count += 1


############################################################
# NetworkX graph manipulations
#
# This function takes a simple adjacency matrix CSV file name as input.
# The adjacency matrix itself should have no label/column/row headers.
# It just needs the connection data. 
# E.g., an example of 3x3 adjacency matrix file contents:
#
#       1,0,0
#       0,1,1
#       1,0,0
#
# The export file type can be "graphml" for GraphML format, or
# it can be "pajek" for Pajek file format.
#
def writeGraphFile( csvFileNamePrefix, csvExtention, path, exportType, debug=False ):

    exportType = str.lower(exportType)

    if exportType == 'pajek':
        print (">> Export file type = '%s'" % exportType)
    elif exportType == 'graphml':
        print (">> Export file type = '%s'" % exportType)
    else:
        print("Error: file type for export can only be (a) 'graphml', or (b) 'pajek'")
        return False


    csvFileName = csvFileNamePrefix + '.' + csvExtention

    csvPathFile = os.path.join(path, csvFileName)

    #does input CSV file exist?
    if checkFilePath( csvFileName, path, debug) == False:
        print ("Input CSV file %s not found." % csvPathFile )
        return False
    else:
        if debug: print("Found input CSV file %s" % csvPathFile )


    #read adjacency matrix file into pandas:
    #input_data = pd.read_csv(adjMatrixFileName, index_col=0)
    #input_data = pd.read_csv(adjMatrixFileName, header=None)
    input_data = pd.read_csv(csvPathFile, header=None)

    #load NetworkX with adjacency matrix graph data (via Pandas)
    #G = nx.grid_graph(dim=[10,10] )
    #G = nx.DiGraph( input_data.values ) #for directed graphs
    G = nx.Graph( input_data.values )  #for undirected graphs

    #Use NetworkX to translate/write graph to Pajek graph file (text) format.
    #extention = "pajek"
    extention = exportType
    exportFile = csvFileNamePrefix + "." + extention
    exportPathFile = os.path.join(path, exportFile)
    if exportType == 'pajek':
        nx.write_pajek(G, exportPathFile)
        print ("Wrote network graph (Pajek format) to text file: %s") % exportPathFile
    elif exportType == 'graphml':
        nx.write_graphml(G, exportPathFile)
        print ("Wrote network graph (GraphML format) to text file: %s") % exportPathFile    
    else:
        print ("Error: unknown export type '%s'" % exportType)
        return False


############################################################


# Main Graph Random Selector Main Test Harness:

print ("\nUsage:\n %s [#iterations: int] [size: int] [k: int] [p: float] [path: str] [filename: str] [exportType: 'graphml' or 'pajek'] [starting ID: 1] [debugMode: 0 or 1]\n" % str(sys.argv[0]) )
print ("e.g., for small '50x50' maps:\n  python  %s  10  50  2  0.05  outputDir  small_   graphml  1  0\n" % str(sys.argv[0]) )
print ("e.g., for large '1000x1000' maps:\n  python  %s  10  1000  2  0.0025  outputDir  large_   pajek  1  1\n" % str(sys.argv[0]) )


iterations = int(sys.argv[1]) #get first command line parameter after script name (argv[0])
if iterations <= 1: iterations = 1
if iterations >= 200: iterations = 200

maxLen1 = int(sys.argv[2])
if maxLen1 < 10: maxLen1 = 10
if maxLen1 > 3000: maxLen1 = 3000

k = int(sys.argv[3])
if k < 0: k = 1
if k > 4: k = 4

p = float(sys.argv[4])
if p < 0.0: p = 0.0
if p > 1.0: p = 1.0

path = str(sys.argv[5])
if isNotEmpty(path) == False: path = "outputPath"

fileNamePrefix = str(sys.argv[6])
if isNotEmpty(fileNamePrefix) == False: fileNamePrefix = "outGraph_"

exportType = str(sys.argv[7])
if isNotEmpty(exportType) == False: exportType="graphml"

startId = int(sys.argv[8])
if startId < 1: startId = 1

debug = int(sys.argv[9])
if debug == 1: debug = True
elif debug == 0: debug = False
else: debug = False

print("Running with options:\n  #iterations=%d\n  size=%d\n  cluster depth k=%d\n  rewiring percentage p=%f\n  path=%s\n  fileName=%s\n  export file type=%s\n  starting file ID number=%s\n  debugMode=%s\n" % (iterations, maxLen1, k, p, path, fileNamePrefix, exportType, startId, debug) )


count = startId #(startID is the starting number used in numbering the output files.) 
if count < 0: count = 0

while count < (iterations + startId):
    print("\nIteration: %d\n" % count)

    width = maxLen1 
    height = maxLen1

    #Initialize the 2D matrix, and set each cell value to desired initial value:
    initialValue = 0 #zero means unconnected.
    matrix1 = [[ initialValue for x in range(width) ] for y in range(height) ]
    if debug: print("Created initial empty matrix.")
    if debug: printMatrix( width, height, matrix1 )

    #Create a regular matrix, of type k-regular (where k is a positive integer).
    createRegularMatrix( k, width, height, matrix1)
    if debug: print("Created a k-regular matrix (where cluster depth k = %d)." % k)
    if debug: printMatrix( width, height, matrix1 )

    #Create a small-world matrix, with rewiring probability 'p' equal to a value < 1.0:
    smallWorld = matrix1
    createSmallWorldMatrix( p, width, height, smallWorld, debug )
    if debug: print("Created a small-world matrix with rewiring probability p = %f" % p)
    if debug: printMatrix( width, height, smallWorld )

    #now write simple adjacency matrix to text file in CSV format:
    csvExtention = 'csv'
    fileName = str(fileNamePrefix + str(count)) #append count to file name
    results = writeCsvFile( fileName, csvExtention, path, ",", width, height, matrix1, debug)
    print ("Wrote network graph to CSV file to: %s" % results )

    #Call NetworkX to translate the CSV file into a Pajek format graph text file:
    writeGraphFile( fileName, csvExtention, path, exportType, debug)

    count += 1


print ("\nDone.\n")
