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

REQUIREMENTS: 
1. This script requires that the "graph_generator.py" program be run first.
2. This script assumes the input files in the input file directory, have unique file names.


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

Third, create three (in this case) target directories for the small and simple files:
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

Seventh, repeat steps 2 through 6, but for the other demographically stratified subgroups,
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
def checkPath( path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print("Script_dir = [%s]" % script_dir)
    
    #get path to input path:
    input_dir = os.path.join(script_dir, path)
    if debug: print("Target dir = [%s]" % input_dir)
    
    #does path exist?
    if os.path.exists(input_dir):
        
        if debug: print("Found path: [%s]" % input_dir)
        return True
        
    else: 
        print("Path does not exist: [%s]" % input_dir)
        return False


############################################################
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
def getFilenamesByExtention( path, extension ):
    list_dir = []
    list_dir = os.listdir(path)
    desired_files = []
    count = 0
    for file in list_dir:
        if file.endswith(extension): # eg: '.txt'
            desired_files.append( str(file) )
            count += 1

    return count, desired_files


"""
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
"""


############################################################
# Main Graph Random Selector Main Test Harness:

def main():

    print ("\nUsage:\n %s [source files subdir: str] [target subdir: str] [# files to randomly select: int] [file type: 0 = 'csv', 1 = 'graphml'] [[debugMode: 0 or 1]\n" % str(sys.argv[0]) )
    print ("e.g., python  %s  small_maps_100x100  group1  100  0  1\n" % str(sys.argv[0]) )
    print ("e.g., python  %s  large_maps_1000x1000  group2  75  1  0\n" % str(sys.argv[0]) )


    sourceDir = str(sys.argv[1]) #get first command line parameter after argv[0]

    destDir = str(sys.argv[2])

    numFilesToRandomSelect = int(sys.argv[3])
    if numFilesToRandomSelect < 0: numFilesToRandomSelect = 0

    fileType = int(sys.argv[4])
    if fileType < 0: fileType = 0   #csv
    if fileType > 1: fileType = 1   #graphml

    debug = int(sys.argv[5])
    if debug == 1: debug = True
    elif debug == 0: debug = False
    else: debug = False

    advert = "(where 0 = CSV files, and 1 = graphML files)"
    print("Running with options:\n  source file path=%s\n  destination file path=%s\n  number of files to random select=%d\n  file type=%d  %s\n  debugMode=%s\n" % (sourceDir, destDir, numFilesToRandomSelect, fileType, advert, debug) )


    csvExtention = ".csv"
    graphmlExtention = ".graphml"
    extention = ""
    if fileType == 0: extention = csvExtention
    elif fileType == 1: extention = graphmlExtention
    else: fileType = -1 #error


    #Calculate path to current working directory (where we assume this program runs):
    cwd = os.path.abspath(".")
    #Calculate paths to input and output files folders:
    sourcePath = os.path.join(cwd, sourceDir)
    destPath = os.path.join(cwd, destDir)


    #do input and output directories exist?
    if checkPath( sourcePath, debug ) == False: sys.exit(-1)
    if checkPath(  destPath, debug  ) == False: sys.exit(-2)


    #get count and names of desired files in source folder:
    fileCount, fileNames = getFilenamesByExtention( sourcePath, extention )
    if numFilesToRandomSelect > fileCount:
        print("Error: you want %d files, but only %d input files were found in directory:" % (numFilesToRandomSelect, fileCount) )
        print(sourcePath)
        sys.exit(-3)

    print("Found file(s):")
    for name in fileNames:
        print (">> [%s]" % name)
    print ("File count (with extention [%s]): %d" % (extention, fileCount) )
    #rand = random.randint(0, fileCount-1)
    #print ("fileNames[0] = %s" % fileNames[0] ) 
    #print ("fileNames[%d] = %s" % (fileCount-1, fileNames[fileCount-1]) )
    #print ("fileNames[%d] = %s" % (rand, fileNames[rand]) )


    count = 0
    inputListFileCount = fileCount
    outputFileNames = []
    while count < numFilesToRandomSelect:
        
        #1. get a random file from the input list
        rand = random.randint(0, inputListFileCount-1)
        selectedFileName = fileNames[rand]
        print("Random selected file: %s", selectedFileName)
        
        #2. add it to the output list
        outputFileNames.append(selectedFileName)

        #3. remove the randomly selected file from input list:
        fileNames = list( set(fileNames) - set(outputFileNames) )
        
        #4. update counts:
        inputListFileCount = len( fileNames ) #should decrement by 1 each iteration
        print ("new length of input file list = %d" % len(fileNames) )
        count += 1


    print("\nRandomly selected the following file(s):")
    for name in sorted(outputFileNames):
        print (">> [%s]" % name)


    print("\nRemaining file(s) in input folder:")
    for name in sorted(fileNames):
        print (">> [%s]" % name)


    """
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
    """

    print ("\nDone.\n")


############################################################

if __name__ == '__main__':
    main()
