import random
import math
import pandas as pd
import networkx as nx
import pylab
from pylab import rcParams


"""
Create a two-dimensional adjacency matrix. 
Note -- only square matrices are considered.

Initialize all matrix values to some integer value.
Remove self-loops by setting self-connected values to zero (i.e. not connected).
Then print the entire matrix.
Then save the matrix to CSV file format.

Then read the CSV file with Pandas library.
Then create a NetworkX graph based on the CSV file input.
Then draw the graph.

Calculate the Dijkstra, Bellman-Ford and A* distances and paths.

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

############################################################
def mutateMatrix( mutantPercent, maxWidth, maxHeight, matrix):
    if mutantPercent >= 0.99:
        mutantPercent = .99
    if mutantPercent <= 0.0:
        mutantPercent = .01

    newValue = 0
    numCells = maxWidth * maxHeight
    numCellsNoDiagonal = numCells - maxWidth
    numCellPairs = numCells / 2
    numCellPairsNoDiagonal = numCellsNoDiagonal / 2

    #Calculate number of cells to mutate, not counting cells along main diagonal:
    mutantCellCount = numCellsNoDiagonal * mutantPercent
    
    #Since matrix is symmetric, each mutantPairCount includes the (x,y) and (y,x) pair.
    #This values tells us how main pairs of cells will be modified.
    #Do not count the cells of the main diagonal, as those cannot be modified.
    mutantPairCount = mutantCellCount / 2.0

    print "Input desired mutant percentage: %f" % float(mutantPercent)
    print "Total number of 2D matrix cells: %d" % numCells
    print "Total number of 2D matrix cells excluding main diagonal: %f" % numCellsNoDiagonal
    print "Total number of 2D matrix cell pairs: %f" % numCellPairs
    print "Total number of 2D matrix cell pairs excluding main diagonal: %f" % numCellPairsNoDiagonal
    print "Number of cell pairs to mutate: %f" % mutantPairCount
    print "Percentage of cell pairs to mutate out of available cell pairs",
    print   "(i.e., not counting cells along main diagonal): %f" \
            % (mutantPairCount / numCellPairsNoDiagonal )
    print "Percentage of cell pairs to mutate out of all cell pairs",
    print   "(i.e., including cells along main diagonal): %f" \
            % (mutantPairCount / numCellPairs )
    #print "Percentage of cells to mutate out of available cells ",
    #print   "(i.e., not counting cells along main diagonal): %f" \
    #        % (mutantCellCount / float(numCellsNoDiagonal))
    #print "Percentage of cells to mutate out of all cells (i.e., including",
    #print   "cells along main diagonal): %f" % (mutantCellCount / float(numCells))
    
    currentMutantPairCount = 0
    newValue = 0    #zero means unconnected vertex pair

    #Iteratively disconnect vertices using random generation. Continue until goal reached.
    while (currentMutantPairCount < mutantPairCount):
        #Randomly determine the cell to mutate. Use height-1, and width-1, 
        # so as to not exceed array boundaries:
        randx = random.randint(0, maxWidth-1)
        randy = random.randint(0, maxHeight-1)
        #print "randx = %s, randy = %s" % (randx, randy)
        
        #don't bother changing cells which already equal the new value,
        # and don't change values along the main diagonal (i.e., where x=y):
        if (matrix[randx][randy] != newValue) and (randx != randy):
            matrix[randx][randy] = newValue #change the (x --> y) cell value
            matrix[randy][randx] = newValue #change the inverse (y --> x) cell value
            currentMutantPairCount += 1
        #else:
        #    print "collision detected at %d,%d (count=%d)" % (randx, randy, currentMutantPairCount)

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


maxLen1 = 7    #the maximum height and width of square matrix (zero-based).
width = maxLen1 #Note, using maxLen +1, to include space for labels
height = maxLen1
initialValue = 1

#Initialize the 2D matrix, and set each cell value to 1.
matrix1 = [[ initialValue for x in range(width) ] for y in range(height) ]
printMatrix( width, height, matrix1 )


#now remove all self-loops, by setting those cell values to 0 (i.e., not connected):
removeLoops( width, height, matrix1 )
print("Removed self-loops.")
printMatrix( width, height, matrix1 )


#now set the percentage of Connected nodes that will be randomly set Unconnected.
mutantPercent = 0.50
mutateMatrix( mutantPercent, width, height, matrix1 )
print("Mutated matrix (excluding the main diagonal).")
printMatrix(width, height, matrix1)


#now write simple adjacency matrix to text file
filename = 'graph.csv'
writeCsvFile( filename, ",", width, height, matrix1)
print ("Wrote network graph to CSV file: %s" % filename)


#read adjacency matrix file into pandas:
#input_data = pd.read_csv(filename, index_col=0)
input_data = pd.read_csv(filename, header=None)


############################################################
# NetworkX graph manipulations
############################################################


#set graph display to 5 x 5 inches
rcParams['figure.figsize'] = 10, 10

#load NetworkX with adjacency matrix graph data (via Pandas)
#G = nx.DiGraph( input_data.values ) #for directed graphs
G = nx.Graph( input_data.values )  #for undirected graphs
#G = nx.grid_graph(dim=[10,10] )

#write graph to text file in Pajek format.
filename = "graph.pajek"
nx.write_pajek(G, filename)
print ("Wrote network graph to (Pajek format) text file: %s") % filename

#Get list of nodes:
nodeList = G.nodes()
#print("Node list: \n %s") % nodeList
nodeListData = G.nodes(data=True)
#print("Node list data: \n %s") % nodeListData


#get Dijkstra distance between node 2 and node (maxLen1 - 2):
dijkstraPath = nx.dijkstra_path(G, 2, (maxLen1-2) )
print ("dijkstraPath = %s") % dijkstraPath
dijkstraPathLength = nx.dijkstra_path_length(G, 2, (maxLen1-2) )
print ("dijkstraPathLength = %d") % dijkstraPathLength
#print ("dijkstra: length of path list = %d") % ( len(dijkstraPath)-1 )


#get Bellman-Ford distance between node 2 and all the other nodes:
pred, dist = nx.bellman_ford(G, 2 )
print ("bellmanFord: pred = %s") % sorted(pred.items())
print ("bellmanFord: dist = %s") % sorted(dist.items())
#bellmanFordPathLength = nx.bellman_ford_path_length(G, 2, (maxLen1-2) )
#print ("bellmanFordPathLength = %d") % bellmanFordPathLength
#print ("bellmanFord: length of path list = %d") % ( len(bellmanFordPath)-1 )


#get A* distance between node 2 and node (maxLen1 - 2):
aStarPath = nx.astar_path(G, 2, (maxLen1-2) )
print ("aStarPath = %s") % aStarPath
aStarPathLength = nx.astar_path_length(G, 2, (maxLen1-2) )
print ("aStarPathLength = %d") % aStarPathLength
#print ("aStar: length of path list = %d") % ( len(aStarPath)-1 )


#now draw the graph with a circular shape:
print ("Drawing graph...")
#nx.draw(G, with_labels=True)
#nx.draw_spectral(G, with_labels=True)
nx.draw_circular(G, with_labels=True)
#nx.draw_spring(G, with_labels=True)
#nx.draw_shell(G, with_labels=True)
#nx.draw_networkx(G, with_labels=True)
#nx.draw_random(G, with_labels=True)

pylab.show() #show the graph output to screen
print ("\nDone.\n")
