import random
import math
import pandas as pd
import networkx as nx
import pylab
from pylab import rcParams
import sys
import os


"""
Program to create random small-world graphs in the form of
two-dimensional adjacency matrices. 
Note -- only square matrices are considered.
This program creates adjacency matrix files, and corresponding Pajek format text files.
It uses NetworkX to do the file transformations (adjacency matrix --> Pajek).

Initialize and create a small-world matrix.
Then print the entire matrix.
Then save the matrix to CSV file format.
Then read the CSV file with Pandas library.
Then create a NetworkX graph based on the CSV file input.
Save the map in Pajek format.

For reference, see:
http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python
and
http://stackoverflow.com/questions/29192644/passing-a-multidimensional-array-to-a-function-in-python
and
http://stackoverflow.com/questions/29572623/plot-networkx-graph-from-adjacency-matrix-in-csv-file#29574772

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
def writeCsvFile( fileName, path, delimiter, maxWidth, maxHeight, matrix, debug=False ):

    """
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
    """

    finalPathFileName = createFilePath( fileName, path, debug)
    
    
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
#def performNetworkXCalculations(width, height, adjMatrixFileName):
#def writePajekFile( width, height, adjMatrixFileName, path, debug=False ):
def writePajekFile( adjMatrixFileName, path, debug=False ):

    #read adjacency matrix file into pandas:
    #input_data = pd.read_csv(adjMatrixFileName, index_col=0)
    input_data = pd.read_csv(adjMatrixFileName, header=None)

    #load NetworkX with adjacency matrix graph data (via Pandas)
    #G = nx.grid_graph(dim=[10,10] )
    #G = nx.DiGraph( input_data.values ) #for directed graphs
    G = nx.Graph( input_data.values )  #for undirected graphs

    #Use NetworkX to translate/write graph to Pajek graph file (text) format.
    filename = ""
    nx.write_pajek(G, filename)
    print ("Wrote network graph to (Pajek format) text file: %s") % filename

"""
    #boundary checking:
    if width < 0 or width > 16: width = 10
    if height < 0 or height > 10: height = 10

    #set graph display to x,y screen inches:
    rcParams['figure.figsize'] = width, height

    #Get list of nodes:
    nodeList = G.nodes()
    #print("Node list: \n %s") % nodeList
    nodeListData = G.nodes(data=True)
    #print("Node list data: \n %s") % nodeListData

    #determine start and destination nodes for pathfinding purposes
    startNode = 1
    destNode = maxLen1/2 + 1
    print ("Start node: %d" % startNode)
    print ("Destination node: %d" % destNode)

    #get Dijkstra distance between start and destination nodes:
    dijkstraPath = nx.dijkstra_path(G, startNode, destNode )
    print ("dijkstraPath = %s") % dijkstraPath
    dijkstraPathLength = nx.dijkstra_path_length(G, startNode, destNode )
    print ("dijkstraPathLength = %d") % dijkstraPathLength
    #print ("dijkstra: length of path list = %d") % ( len(dijkstraPath)-1 )

    #get Bellman-Ford distance between the startNode and all the other nodes:
    pred, dist = nx.bellman_ford(G, startNode )
    #print ("bellmanFord: pred = %s") % sorted(pred.items())
    #print ("bellmanFord: dist = %s") % sorted(dist.items())
    #if destNode in dist:
    #    print dist.index(destNode)

    #get A* distance between start and destination nodes:
    aStarPath = nx.astar_path(G, startNode, destNode )
    print ("aStarPath = %s") % aStarPath
    aStarPathLength = nx.astar_path_length(G, startNode, destNode )
    print ("aStarPathLength = %d") % aStarPathLength
    #print ("aStar: length of path list = %d") % ( len(aStarPath)-1 )

    #now draw the graph with a circular shape:
    print ("Drawing graph...")
    nx.draw_circular(G, with_labels=True)
    #nx.draw(G, with_labels=True)
    #nx.draw_spectral(G, with_labels=True)
    #nx.draw_spring(G, with_labels=True)
    #nx.draw_shell(G, with_labels=True)
    #nx.draw_networkx(G, with_labels=True)
    #nx.draw_random(G, with_labels=True)

    pylab.show() #show the graph output to screen
"""

############################################################


# Main Graph Generator Test Harness:
#For the doc study, consider (a) 50x50, k=2, p=.05; and (b) 1000x1000, k=2, p=0.0025

print ("\nUsage: %s [#iterations: int] [size: int] [k: int] [p: float] [path: str] [filename: str] [debugMode: 0 or 1]\n" % str(sys.argv[0]) )
print ("e.g., for small '50x50' maps:\n  python  %s  10  50  2  0.05  subdir  small_  0\n" % str(sys.argv[0]) )
print ("e.g., for large '1000x1000' maps:\n  python  %s  10  1000  2  0.0025  subdir  large_  1\n" % str(sys.argv[0]) )


iterations = int(sys.argv[1]) #get first command line parameter after script name (argv[0])
if iterations <= 1: iterations = 1
if iterations >= 200: iterations = 200

maxLen1 = int(sys.argv[2])
if maxLen1 < 10: maxLen1 = 10
if maxLen1 > 1000: maxLen1 = 1000

k = int(sys.argv[3])
if k < 0: k = 1
if k > 4: k = 4

p = float(sys.argv[4])
if p < 0.0: p = 0.0
if p > 1.0: p = 1.0

path = str(sys.argv[5])
if isNotEmpty(path) == False: path = "file_output"

fileNamePrefix = str(sys.argv[6])
if isNotEmpty(fileNamePrefix) == False: fileNamePrefix = "graph"

debug = int(sys.argv[7])
if debug == 1: debug = True
elif debug == 0: debug = False
else: debug = False

print("Running with options:\n #iterations=%d\n size=%d\n k=%d\n p=%f\n path=%s\n fileName=%s\n debug=%s" % (iterations, maxLen1, k, p, path, fileNamePrefix, debug) )

#initialValue = 0 # zero means disconnected, 1 means connected.
#k = 2   #depth of default connections per node. Watts & Strogatz small-worlds use k=2.
#p = 0.0 #the randomization percent used in small-world network generation

#maxLen1 = 1000     #the maximum dimension of the square matrix (zero-index).
#maxLen1 = 50        #the maximum dimension of the square matrix (zero-index).
#maxLen1 = 20

#if maxLen1 == 50: p, debug = 0.05, True           #randomization for small map
#elif maxLen1 == 1000: p, debug = 0.0025, False     #randomization for large map
#else: maxLen1, p, debug = 100, 0.1, True

count = 0
while count < iterations:
    count += 1
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
    if debug: print("Created a k-regular matrix (where k = %d)." % k)
    if debug: printMatrix( width, height, matrix1 )

    #Create a small-world matrix, with rewiring probability 'p' equal to a value < 1.0:
    smallWorld = matrix1
    createSmallWorldMatrix( p, width, height, smallWorld, debug )
    if debug: print("Created a small-world matrix with rewiring probability = %f" % p)
    if debug: printMatrix( width, height, smallWorld )

    #now write simple adjacency matrix to text file
    fileName = fileNamePrefix + str(count) + '.csv'
    #fileName = str(fnamePrefix + '.csv')
    writeCsvFile( fileName, path, ",", width, height, matrix1, debug)
    print ("Wrote network graph to CSV file to: %s/%s" % (path, fileName) )


"""
#Call NetworkX to do pathfinding calculations, and calculate shortest paths
performNetworkXCalculations( 10, 10, fileName )


print ("\nDone.\n")
"""