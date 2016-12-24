import random
import math
import pandas as pd
import networkx as nx
import pylab
from pylab import rcParams


"""
Create a two-dimensional adjacency matrix. 
Note -- only square matrices are considered.

Initialize and create a small-world matrix.
Then print the entire matrix.
Then save the matrix to CSV file format.
Then read the CSV file with Pandas library.
Then create a NetworkX graph based on the CSV file input.
Save the map in Pajek format.
Do some pathfinding calculations: use Dijkstra, Bellman-Ford and A* algorithms.
Then draw the graph.

For reference, see:
http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python
and
http://stackoverflow.com/questions/29192644/passing-a-multidimensional-array-to-a-function-in-python
and
http://stackoverflow.com/questions/29572623/plot-networkx-graph-from-adjacency-matrix-in-csv-file#29574772

"""

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
    print("Removed the self-loops (i.e., main diagonal cleared).")


############################################################
def writeCsvFile( fileName, delimiter, maxWidth, maxHeight, matrix ):
    file = open(fileName, 'w')
    file.truncate() #delete existing file contents (if any)
    x,y = 0, 0
    delim = delimiter
    for y in range(maxHeight):
        line = ""
        for x in range(maxWidth):
            #print "matrix[%r][%r] = %r", % (x, y, (matrix[x][y]) )    
            #print matrix[x][y],     #the ',' keeps printing on same line
            line += str(matrix[x][y])
            if (x < maxWidth-1):
                line = line + delim
            if (x >= maxWidth-1):
                ##line = line + "\n"
                file.write(line + "\n")
                #print(line)
    file.close()
#print ("Wrote output file: %s" % filename)


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
def performNetworkXCalculations( width, height, adjMatrixFileName ):

    #boundary checking:
    if width < 0 or width > 16: width = 10
    if height < 0 or height > 10: height = 10
    
    #read adjacency matrix file into pandas:
    #input_data = pd.read_csv(adjMatrixFileName, index_col=0)
    input_data = pd.read_csv(adjMatrixFileName, header=None)

    #set graph display to x,y screen inches:
    rcParams['figure.figsize'] = width, height

    #load NetworkX with adjacency matrix graph data (via Pandas)
    #G = nx.DiGraph( input_data.values ) #for directed graphs
    G = nx.Graph( input_data.values )  #for undirected graphs
    #G = nx.grid_graph(dim=[10,10] )

    #Use NetworkX to translate/write graph to Pajek graph file (text) format.
    filename = "graph.pajek"
    nx.write_pajek(G, filename)
    print ("Wrote network graph to (Pajek format) text file: %s") % filename

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

############################################################


# Main Test Harness:
#For the doc study, consider (a) 50x50, k=2, p=.05; and (b) 1000x1000, k=2, p=0.0025

debug = True
initialValue = 0 # zero means disconnected, 1 means connected.
k = 2   #depth of default connections per node. Watts & Strogatz small-worlds use k=2.
p = 0.0 #the randomization percent used in small-world network generation

#maxLen1 = 1000     #the maximum dimension of the square matrix (zero-index).
maxLen1 = 50        #the maximum dimension of the square matrix (zero-index).

if maxLen1 == 50: p, debug = 0.05, True           #randomization for small map
elif maxLen1 == 1000: p, debug = 0.0025, False     #randomization for large map

width = maxLen1 
height = maxLen1

#Initialize the 2D matrix, and set each cell value to desired initial value:
matrix1 = [[ initialValue for x in range(width) ] for y in range(height) ]
if debug: print("Created initial empty matrix.")
if debug: printMatrix( width, height, matrix1 )

#Create a regular matrix, of type k-regular (where k is a positive integer).
createRegularMatrix( k, width, height, matrix1)
if debug: print("Created a k-regular matrix (where k = %d)." % k)
if debug: printMatrix( width, height, matrix1 )

#Create a small-world matrix, with rewiring probability 'p' equal to a value < 1.0:
createSmallWorldMatrix( p, width, height, matrix1, debug )
if debug: print("Created a small-world matrix with rewiring probability = %f" % p)
if debug: printMatrix( width, height, matrix1 )


#now write simple adjacency matrix to text file
fileName = 'graph.csv'
writeCsvFile( fileName, ",", width, height, matrix1)
print ("Wrote network graph to CSV file: %s" % fileName)


#Call NetworkX to do pathfinding calculations, and calculate shortest paths
performNetworkXCalculations( 10, 10, fileName )


print ("\nDone.\n")
