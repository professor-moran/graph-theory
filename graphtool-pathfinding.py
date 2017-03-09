import graph_tool.all as gt
import sys
import os
import gc
import timeit
from memory_profiler import profile
import multiprocessing

#from graph_tool.all import *


# Created: 12-17-2016
#
# (c) Michael Moran
#
#
"""
Program to read the small-world graphs generated by the graph generator script. 
It then loads the maps, one by one, into Graph-Tool to calculate 
shortest paths.

Pipe the output to text file for subsequent parsing and reporting of the results.

For reference, see:
http://stackoverflow.com/questions/5086430/how-to-pass-parameters-of-a-function-when-using-timeit-timer
"""



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
#def heuristic(v, target, pos):
#
#    return sqrt(sum((pos[v].a - pos[target].a) ** 2))
#



############################################################
# Graph-Tool graph manipulations
#
# This function takes a simple GraphML text file name as input.
# The file itself should follow GraphML characteristics, discussed here:
# http://graphml.graphdrawing.org
#
# Warning: if drawGraph is True, it will write the graphs to the file system, one-by-one
# as they are processed for pathfinding operations. You will not see them on the screen.
# Additionally, this slows down the pathfinding operations!!!
# So, set the drawGraph parameter to true only during testing.
#
# The pathfinding algorithm parameter accepts a 1, 2, or 3, 
# which (alphabetical order) indicates the following:
#   1 = A* (A-star) algorithm   <--- this is the default
#   2 = Bellman-Ford algorithm
#   3 = Dijkstra's algorithm
#
def performGraphToolCalculations(graphmlFileName, path, algorithm=1, drawGraph=False, debug=False, memoryMode=False):

    algorithm = int(algorithm)
    drawGraph = bool(drawGraph)
    debug = bool(debug)

    if debug: 
        print("Performing Graph-Tool pathfinding calculations...")  
        print("GraphML File Name = %s" % graphmlFileName)
        print("Path = %s" % path)
        print("Algorithm = %d" % algorithm) #1 = Astar, 2 = BellmanFord, 3 = Dijkstra
        print("Draw Graph = %s" % drawGraph)

    #new:
    print("Memory Mode = %s" % memoryMode)


    #boundary checking:
    if algorithm < 1: algorithm = 1
    if algorithm > 3: algorithm = 3

    #Get the path to the target GraphML file:
    graphmlPathFile = os.path.join(path, graphmlFileName)

    start_time = 0.0

    #Now calculate the shortest paths, based on the user-specified algorithm.
    if algorithm == 1:
        if debug: print("Algorithm: A-Star")
        
        if (memoryMode):
            print("RESULTS|A-star|memoryConsumption(MB)|...\n")
        else:
            start_time = timeit.default_timer() #get the start time

        manager = multiprocessing.Manager()
        state = manager.list()
        state.append({})
        args = state[0]
        args["input_path_file"] = graphmlPathFile
        args["draw_graph"] = drawGraph
        args["debug"] = debug
        state[0] = args
        #start_time = timeit.default_timer() #get the start time
        #runAstar(G, startNode, destNode)
        #p = multiprocessing.Process(target=runAstar, args=(state,) )
        if (memoryMode): 
            #run the decorated version to collect memory use statistics:
            p = multiprocessing.Process(target=runAstar, args=(state,) )
        else:
            #do not run the decorated version (i.e., don't collect memory usage data):
            p = multiprocessing.Process(target=runAstarNoMem, args=(state,) )
        
        p.start()
        p.join() #wait for child process to finish.
        
        if (memoryMode):
            print("RESULTS|A-star|pathLength|%d" % int(state[0]["pathLength"]) )
            print("RESULTS|A-star|path|%s" % str(state[0]["path"]) )
        else:
            end_time = timeit.default_timer() #get the end time
            elapsed_time = end_time - start_time

    elif algorithm == 2:
        if debug: print("Algorithm: Bellman-Ford")

        if (memoryMode):
            print("RESULTS|Bellman-Ford|memoryConsumption(MB)|...\n")
        else:
            start_time = timeit.default_timer() #get the start time

        manager = multiprocessing.Manager()
        state = manager.list()
        state.append({})
        args = state[0]
        args["input_path_file"] = graphmlPathFile
        args["draw_graph"] = drawGraph
        args["debug"] = debug
        state[0] = args
        #start_time = timeit.default_timer() #get the start time
        #runBellmanFord(G, startNode, destNode)
        #p = multiprocessing.Process(target=runBellmanFord, args=(state,) )
        if (memoryMode): 
            #run the decorated version to collect memory use statistics:
            p = multiprocessing.Process(target=runBellmanFord, args=(state,) )
        else:
            #do not run the decorated version (i.e., don't collect memory usage data):
            p = multiprocessing.Process(target=runBellmanFordNoMem, args=(state,) )

        p.start()
        p.join() #wait for child process to finish.
        
        if (memoryMode):
            print("RESULTS|Bellman-Ford|pathLength|%d" % int(state[0]["pathLength"]) )
            print("RESULTS|Bellman-Ford|path|%s" % str(state[0]["path"]) )
        else:
            end_time = timeit.default_timer() #get the end time
            elapsed_time = end_time - start_time

    elif algorithm == 3:
        if debug: print("Algorithm: Dijkstra")

        if (memoryMode):
            print("RESULTS|Dijkstra|memoryConsumption(MB)|...\n")
        else:
            start_time = timeit.default_timer() #get the start time

        manager = multiprocessing.Manager()
        state = manager.list()
        state.append({})
        args = state[0]
        args["input_path_file"] = graphmlPathFile
        args["draw_graph"] = drawGraph
        args["debug"] = debug
        state[0] = args
        #start_time = timeit.default_timer() #get the start time
        #runDijkstra(G, startNode, destNode)
        #p = multiprocessing.Process(target=runDijkstra, args=(state,) )
        if (memoryMode): 
            #run the decorated version to collect memory use statistics:
            p = multiprocessing.Process(target=runDijkstra, args=(state,) )
        else:
            #do not run the decorated version (i.e., don't collect memory usage data):
            p = multiprocessing.Process(target=runDijkstraNoMem, args=(state,) )

        p.start()
        p.join() #wait for child process to finish.
        
        if (memoryMode):
            print("RESULTS|Dijkstra|pathLength|%d" % int(state[0]["pathLength"]) )
            print("RESULTS|Dijkstra|path|%s" % str(state[0]["path"]) )
        else:
            end_time = timeit.default_timer() #get the end time
            elapsed_time = end_time - start_time

    #cleanup:
    del graphmlPathFile
    
    #Done:
    if (memoryMode):
        return
    else:
        return elapsed_time


############################################################
#
# The A-Star wrapper function without Memory Consumption analysis.
#
# This version does NOT use the '@profile' decorator for memory usage data gathering.
#
# The only difference between this version and the original is that this one is
# not decorated with '@profile', therefore this one doesn't collect memory stats.
#
def runAstarNoMem(state):

    input_path_file = state[0]["input_path_file"]
    draw_graph = state[0]["draw_graph"]
    debug = state[0]["debug"]

    if debug: print ("In runAstar()")
    if debug: print ("input_path_file = %s" % input_path_file)
    if debug: print ("draw_graph = %s" % draw_graph)
    if debug: print ("debugMode = %s" % debug)
    
    g = gt.Graph()
    g = gt.load_graph( input_path_file )


    startNode = g.vertex(1) #always start at node index 1 (not index zero)
    middle = g.num_vertices()/2 + 1
    destNode = g.vertex( int(middle) ) # set dest halfway between first and last nodes


    #give all edges a weight of 1:
    weights = g.new_edge_property("int")
    #weight.set_value(1)
    for e in g.edges():
        weights[e] = 1
        #print (">>> weights[%s] = %s" % (str(e), str(weights[e])) )


    #Call the Graph-Tool function that actually does the pathfinding:
    dist, pred = gt.astar_search(g, startNode, weight=weights)


    #Graph-Tool's A* method doesn't return a simple path, nor
    # a path length, like NetworkX. Instead it returns two lists: a predecessor, 
    # and a distance list. So, we must do some list traversal to find the desired values:
    i = 0
    path = []   #build the list of node predecessors.
    for p in pred:
        path.append( [i, int(p)] )
        i += 1

    astarPath = [] #create an empty path.
    astarPath.append( int(destNode) ) # append the destination node, then find its predecessor.
    currNode = destNode #set current node to destination node

    #The following loop will start from the destination and work our way back to 
    # the start node, one node link at a time.
    # The predecessor list is in [int][int] format, specifically [index][pred node index],
    # so pred[99][1] means that while on the way to searching from the source to the
    # destination node, the node at index 99 has a predecessor of node index 1.
    while currNode != startNode:  #start with destination node...
        astarPath.append( path [int(currNode)][1] ) #append the predecessor node...
        currNode = path [int(currNode)][1]  #update the current node... keep looping backwards.
    astarPath.reverse() #now reverse the list, so it displays in correct order
    if debug: print("A-Star Path = %s" % astarPath)
    if debug: print("A-Star Path Length = %d" % (len(astarPath) -1) ) #subtract 1 to not count starting node.


    if draw_graph == True:
        #graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(300,300), output="small_100x100_k2_p05_1.png")
        #pos = gt.sfdp_layout(g)
        #gt.graph_draw(g, pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )
        pos = gt.arf_layout(g, max_iter=0)
        #pos = gt.arf_layout(g, max_iter=0, d = 0.95)
        #pos = gt.fruchterman_reingold_layout(g, circular=True, grid=True)
        #gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_text=g.vertex_index, vertex_font_size=12, vertex_color=[1,1,1,0], vertex_size=15, edge_pen_width=1.2, output=(input_path_file + ".png") )
        gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )


    #Return results by loading the list shared between processes.
    state.append({})
    args = state[0]
    args["pathLength"] = len(astarPath) -1 #subtract 1 to not count starting node.
    args["path"] = astarPath
    state[0] = args


############################################################
#
# The A-Star wrapper function
#
# This is a separate Graph-Tool function to make timing calculations
# more fine-grained and specific to the graph algorithm.
#
# This function is run as a separate process, to permit collection of memory
# consumption data due to complexity with the Python memory manager
# vs the OS memory manager. See the following links for details:
#
# http://stackoverflow.com/questions/23937189/how-do-i-use-subprocesses-to-force-python-to-release-memory/24126616#24126616
# https://docs.python.org/2/library/multiprocessing.html
# http://deeplearning.net/software/theano/tutorial/python-memory-management.html
#
@profile(precision=4)
def runAstar(state):

    input_path_file = state[0]["input_path_file"]
    draw_graph = state[0]["draw_graph"]
    debug = state[0]["debug"]

    if debug: print ("In runAstar()")
    if debug: print ("input_path_file = %s" % input_path_file)
    if debug: print ("draw_graph = %s" % draw_graph)
    if debug: print ("debugMode = %s" % debug)
    
    g = gt.Graph()
    g = gt.load_graph( input_path_file )


    startNode = g.vertex(1) #always start at node index 1 (not index zero)
    middle = g.num_vertices()/2 + 1
    destNode = g.vertex( int(middle) ) # set dest halfway between first and last nodes


    #give all edges a weight of 1:
    weights = g.new_edge_property("int")
    #weight.set_value(1)
    for e in g.edges():
        weights[e] = 1
        #print (">>> weights[%s] = %s" % (str(e), str(weights[e])) )


    #Call the Graph-Tool function that actually does the pathfinding:
    dist, pred = gt.astar_search(g, startNode, weight=weights)


    #Graph-Tool's A* method doesn't return a simple path, nor
    # a path length, like NetworkX. Instead it returns two lists: a predecessor, 
    # and a distance list. So, we must do some list traversal to find the desired values:
    i = 0
    path = []   #build the list of node predecessors.
    for p in pred:
        path.append( [i, int(p)] )
        i += 1

    astarPath = [] #create an empty path.
    astarPath.append( int(destNode) ) # append the destination node, then find its predecessor.
    currNode = destNode #set current node to destination node

    #The following loop will start from the destination and work our way back to 
    # the start node, one node link at a time.
    # The predecessor list is in [int][int] format, specifically [index][pred node index],
    # so pred[99][1] means that while on the way to searching from the source to the
    # destination node, the node at index 99 has a predecessor of node index 1.
    while currNode != startNode:  #start with destination node...
        astarPath.append( path [int(currNode)][1] ) #append the predecessor node...
        currNode = path [int(currNode)][1]  #update the current node... keep looping backwards.
    astarPath.reverse() #now reverse the list, so it displays in correct order
    if debug: print("A-Star Path = %s" % astarPath)
    if debug: print("A-Star Path Length = %d" % (len(astarPath) -1) ) #subtract 1 to not count starting node.


    if draw_graph == True:
        #graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(300,300), output="small_100x100_k2_p05_1.png")
        #pos = gt.sfdp_layout(g)
        #gt.graph_draw(g, pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )
        pos = gt.arf_layout(g, max_iter=0)
        #pos = gt.arf_layout(g, max_iter=0, d = 0.95)
        #pos = gt.fruchterman_reingold_layout(g, circular=True, grid=True)
        #gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_text=g.vertex_index, vertex_font_size=12, vertex_color=[1,1,1,0], vertex_size=15, edge_pen_width=1.2, output=(input_path_file + ".png") )
        gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )


    #Return results by loading the list shared between processes.
    state.append({})
    args = state[0]
    args["pathLength"] = len(astarPath) -1 #subtract 1 to not count starting node.
    args["path"] = astarPath
    state[0] = args


############################################################
#
# The Bellman-Ford wrapper function without Memory Consumption analysis.
#
# This version does NOT use the '@profile' decorator for memory usage data gathering.
#
# The only difference between this version and the original is that this one is
# not decorated with '@profile', therefore this one doesn't collect memory stats.
#
def runBellmanFordNoMem(state):

    input_path_file = state[0]["input_path_file"]
    draw_graph = state[0]["draw_graph"]
    debug = state[0]["debug"]

    if debug: print ("In runBellmanFord()")
    if debug: print ("input_path_file = %s" % input_path_file)
    if debug: print ("draw_graph = %s" % draw_graph)
    if debug: print ("debugMode = %s" % debug)

    g = gt.Graph()
    g = gt.load_graph( input_path_file )
    
    
    startNode = g.vertex(1) #always start at node index 1 (not zero)
    middle = g.num_vertices()/2 + 1
    destNode = g.vertex( int(middle) ) # destination node is always halfway between first and last nodes


    #give all edges a weight of 1:
    weights = g.new_edge_property("int")
    #weight.set_value(1)
    for e in g.edges():
        weights[e] = 1
        #print (">>> weights[%s] = %s" % (str(e), str(weights[e])) )


    #According to documentation, if negative_weights=True, then function shortest_path()
    # will start a Bellman_Ford path search (no specific weights property needed).
    # For documentation and details, see: https://graph-tool.skewed.de/static/doc/topology.html?highlight=shortest_path#graph_tool.topology.shortest_path
    #Call the Graph-Tool function that actually does the pathfinding:
    vertList, edgeList = gt.shortest_path(g, startNode, destNode, negative_weights=True)


    bellmanFordPath = [] #create an empty path.
    for v in vertList:
        bellmanFordPath.append( int(v) )
    if debug: print ("Bellman-Ford Path = %s" % ( str(bellmanFordPath) ) )
    if debug: print ("Bellman-Ford Path length = %d" % ( len(bellmanFordPath)-1 ) ) #subtract 1 to not count starting node.


    if draw_graph == True:
        #graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(300,300), output="small_100x100_k2_p05_1.png")
        #pos = gt.sfdp_layout(g)
        #gt.graph_draw(g, pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )
        pos = gt.arf_layout(g, max_iter=0)
        #pos = gt.arf_layout(g, max_iter=0, d = 0.95)
        #pos = gt.fruchterman_reingold_layout(g, circular=True, grid=True)
        #gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_text=g.vertex_index, vertex_font_size=12, vertex_color=[1,1,1,0], vertex_size=15, edge_pen_width=1.2, output=(input_path_file + ".png") )
        gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )


    #Return results by loading the list shared between processes.
    state.append({})
    args = state[0]
    args["pathLength"] = ( len(bellmanFordPath) -1) #subtract 1 to not count starting node.
    args["path"] = str(bellmanFordPath)
    state[0] = args


############################################################
#
# The Bellman-Ford wrapper function
#
# This is a separate Graph-Tool function to make timing calculations
# more fine-grained and specific to the graph algorithm.
#
# This function is run as a separate process, to permit collection of memory
# consumption data due to complexity with the Python memory manager
# vs the OS memory manager. See the following links for details:
#
# http://stackoverflow.com/questions/23937189/how-do-i-use-subprocesses-to-force-python-to-release-memory/24126616#24126616
# https://docs.python.org/2/library/multiprocessing.html
# http://deeplearning.net/software/theano/tutorial/python-memory-management.html
#
@profile(precision=4)
def runBellmanFord(state):

    input_path_file = state[0]["input_path_file"]
    draw_graph = state[0]["draw_graph"]
    debug = state[0]["debug"]

    if debug: print ("In runBellmanFord()")
    if debug: print ("input_path_file = %s" % input_path_file)
    if debug: print ("draw_graph = %s" % draw_graph)
    if debug: print ("debugMode = %s" % debug)

    g = gt.Graph()
    g = gt.load_graph( input_path_file )
    
    
    startNode = g.vertex(1) #always start at node index 1 (not zero)
    middle = g.num_vertices()/2 + 1
    destNode = g.vertex( int(middle) ) # destination node is always halfway between first and last nodes


    #give all edges a weight of 1:
    weights = g.new_edge_property("int")
    #weight.set_value(1)
    for e in g.edges():
        weights[e] = 1
        #print (">>> weights[%s] = %s" % (str(e), str(weights[e])) )


    #According to documentation, if negative_weights=True, then function shortest_path()
    # will start a Bellman_Ford path search (no specific weights property needed).
    # For documentation and details, see: https://graph-tool.skewed.de/static/doc/topology.html?highlight=shortest_path#graph_tool.topology.shortest_path
    #Call the Graph-Tool function that actually does the pathfinding:
    vertList, edgeList = gt.shortest_path(g, startNode, destNode, negative_weights=True)


    bellmanFordPath = [] #create an empty path.
    for v in vertList:
        bellmanFordPath.append( int(v) )
    if debug: print ("Bellman-Ford Path = %s" % ( str(bellmanFordPath) ) )
    if debug: print ("Bellman-Ford Path length = %d" % ( len(bellmanFordPath)-1 ) ) #subtract 1 to not count starting node.


    if draw_graph == True:
        #graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(300,300), output="small_100x100_k2_p05_1.png")
        #pos = gt.sfdp_layout(g)
        #gt.graph_draw(g, pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )
        pos = gt.arf_layout(g, max_iter=0)
        #pos = gt.arf_layout(g, max_iter=0, d = 0.95)
        #pos = gt.fruchterman_reingold_layout(g, circular=True, grid=True)
        #gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_text=g.vertex_index, vertex_font_size=12, vertex_color=[1,1,1,0], vertex_size=15, edge_pen_width=1.2, output=(input_path_file + ".png") )
        gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )


    #Return results by loading the list shared between processes.
    state.append({})
    args = state[0]
    args["pathLength"] = ( len(bellmanFordPath) -1) #subtract 1 to not count starting node.
    args["path"] = str(bellmanFordPath)
    state[0] = args


############################################################
#
# The Dijkstra wrapper function without Memory Consumption analysis.
#
# This version does NOT use the '@profile' decorator for memory usage data gathering.
#
# The only difference between this version and the original is that this one is
# not decorated with '@profile', therefore this one doesn't collect memory stats.
#
def runDijkstraNoMem(state):

    input_path_file = state[0]["input_path_file"]
    draw_graph = state[0]["draw_graph"]
    debug = state[0]["debug"]

    if debug: print ("In runDijkstra()")
    if debug: print ("input_path_file = %s" % input_path_file)
    if debug: print ("draw_graph = %s" % draw_graph)
    if debug: print ("debugMode = %s" % debug)

    g = gt.Graph()
    g = gt.load_graph( input_path_file )


    startNode = g.vertex(1) #always start at node index 1 (not index zero)
    middle = g.num_vertices()/2 + 1
    destNode = g.vertex( int(middle) ) # set dest halfway between first and last nodes


    weights = g.new_edge_property("int")
    #give all edges a weight of 1
    #weight.set_value(1)
    for e in g.edges():
        weights[e] = 1
        #print (">>> weights[%s] = %s" % (str(e), str(weights[e])) )


    #Call the Graph-Tool function that actually does the pathfinding:
    dist, pred = gt.dijkstra_search(g, startNode, weight=weights)

    #Graph-Tool's Dijkstra method doesn't return a simple path, nor
    # a path length, unlike NetworkX. Instead it returns two lists: a predecessor, 
    # and a distance list. So we must do some list traversal to find the desired values.
    i = 0
    path = []   #build the list of node predecessors.
    for p in pred:
        path.append( [i, int(p)] )
        i += 1

    dijkPath = [] #create an empty path.
    dijkPath.append( int(destNode) ) # append the destination node, then find its predecessor.
    currNode = destNode #set current node to destination node

    #The following loop will start from the destination and work our way back to 
    # the start node, one node link at a time.
    # The predecessor list is in [int][int] format, specifically [index][pred node index],
    # so pred[99][1] means that while on the way to searching from the source to the
    # destination node, the node at index 99 has a predecessor of node index 1.
    while currNode != startNode:  #start with destination node...
        dijkPath.append( path [int(currNode)][1] ) #append the predecessor node...
        currNode = path [int(currNode)][1]  #update the current node... keep looping backwards.
    dijkPath.reverse() #now reverse the list, so it displays in correct order
    #print("Dijkstra Path = %s" % dijkPath)
    #print("Dijkstra Path Length = %d" % (len(dijkPath) -1) ) #subtract 1 to not count starting node.


    if draw_graph == True:
        #graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(300,300), output="small_100x100_k2_p05_1.png")
        #pos = gt.sfdp_layout(g)
        #gt.graph_draw(g, pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )
        pos = gt.arf_layout(g, max_iter=0)
        #pos = gt.arf_layout(g, max_iter=0, d = 0.95)
        #pos = gt.fruchterman_reingold_layout(g, circular=True, grid=True)
        #gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_text=g.vertex_index, vertex_font_size=12, vertex_color=[1,1,1,0], vertex_size=15, edge_pen_width=1.2, output=(input_path_file + ".png") )
        gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )


    #Return results by loading the list shared between processes.
    state.append({})
    args = state[0]
    args["pathLength"] = len(dijkPath) -1 #subtract 1 to not count starting node.
    args["path"] = dijkPath
    state[0] = args


############################################################
#
# The Dijkstra wrapper function
#
# This is a separate Graph-Tool function to make timing calculations
# more fine-grained and specific to the graph algorithm.
#
# This function is run as a separate process, to permit collection of memory
# consumption data due to complexity with the Python memory manager
# vs the OS memory manager. See the following links for details:
#
# http://stackoverflow.com/questions/23937189/how-do-i-use-subprocesses-to-force-python-to-release-memory/24126616#24126616
# https://docs.python.org/2/library/multiprocessing.html
# http://deeplearning.net/software/theano/tutorial/python-memory-management.html
#
@profile(precision=4)
def runDijkstra(state):

    input_path_file = state[0]["input_path_file"]
    draw_graph = state[0]["draw_graph"]
    debug = state[0]["debug"]

    if debug: print ("In runDijkstra()")
    if debug: print ("input_path_file = %s" % input_path_file)
    if debug: print ("draw_graph = %s" % draw_graph)
    if debug: print ("debugMode = %s" % debug)

    g = gt.Graph()
    g = gt.load_graph( input_path_file )


    startNode = g.vertex(1) #always start at node index 1 (not index zero)
    middle = g.num_vertices()/2 + 1
    destNode = g.vertex( int(middle) ) # set dest halfway between first and last nodes


    weights = g.new_edge_property("int")
    #give all edges a weight of 1
    #weight.set_value(1)
    for e in g.edges():
        weights[e] = 1
        #print (">>> weights[%s] = %s" % (str(e), str(weights[e])) )


    #Call the Graph-Tool function that actually does the pathfinding:
    dist, pred = gt.dijkstra_search(g, startNode, weight=weights)

    #Graph-Tool's Dijkstra method doesn't return a simple path, nor
    # a path length, unlike NetworkX. Instead it returns two lists: a predecessor, 
    # and a distance list. So we must do some list traversal to find the desired values.
    i = 0
    path = []   #build the list of node predecessors.
    for p in pred:
        path.append( [i, int(p)] )
        i += 1

    dijkPath = [] #create an empty path.
    dijkPath.append( int(destNode) ) # append the destination node, then find its predecessor.
    currNode = destNode #set current node to destination node

    #The following loop will start from the destination and work our way back to 
    # the start node, one node link at a time.
    # The predecessor list is in [int][int] format, specifically [index][pred node index],
    # so pred[99][1] means that while on the way to searching from the source to the
    # destination node, the node at index 99 has a predecessor of node index 1.
    while currNode != startNode:  #start with destination node...
        dijkPath.append( path [int(currNode)][1] ) #append the predecessor node...
        currNode = path [int(currNode)][1]  #update the current node... keep looping backwards.
    dijkPath.reverse() #now reverse the list, so it displays in correct order
    #print("Dijkstra Path = %s" % dijkPath)
    #print("Dijkstra Path Length = %d" % (len(dijkPath) -1) ) #subtract 1 to not count starting node.


    if draw_graph == True:
        #graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(300,300), output="small_100x100_k2_p05_1.png")
        #pos = gt.sfdp_layout(g)
        #gt.graph_draw(g, pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )
        pos = gt.arf_layout(g, max_iter=0)
        #pos = gt.arf_layout(g, max_iter=0, d = 0.95)
        #pos = gt.fruchterman_reingold_layout(g, circular=True, grid=True)
        #gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_text=g.vertex_index, vertex_font_size=12, vertex_color=[1,1,1,0], vertex_size=15, edge_pen_width=1.2, output=(input_path_file + ".png") )
        gt.graph_draw(g, pos=pos, output_size=(800,800), vertex_color=[1,1,1,0], vertex_size=10, edge_pen_width=1.2, output=(input_path_file + ".png") )


    #Return results by loading the list shared between processes.
    state.append({})
    args = state[0]
    args["pathLength"] = len(dijkPath) -1 #subtract 1 to not count starting node.
    args["path"] = dijkPath
    state[0] = args


############################################################
#
# Main Graph-Tool Graph Generator and Performance Test Harness:
# This script assumes that graph files (graphml text format) have already been generated
# by the script: graph_generator.py
#
def main():

    print ("\nUsage:\n %s [path to input GraphML files] [algorithm: 1, 2, or 3] [drawGraphs: 0 or 1] [debugMode: 0 or 1] [forceGC: 0 or 1]\n" % str(sys.argv[0]) )
    print ("Where algorithm: 1 = A* (A-star), 2 = Bellman-Ford, 3 = Dijkstra.\n")
    print ("To save program output for parsing, redirect ('>') stdout to text file.")
    print ("e.g.,\n  python  %s  inputSubDir  3  0  1  0  >  ./temp/output.txt \n\n" % str(sys.argv[0]) )


    path = str(sys.argv[1])
    if isNotEmpty(path) == False:
        print("Target folder cannot be null or blank.")
        sys.exit(1)
    else:
        #verify if the path exists:
        if checkPath( path, False) == False:
            print("Target folder '%s' could not be found." % path)
            sys.exit(2)
        else:
            print("Found target folder: %s" % path)


    algorithm = int(sys.argv[2])
    if algorithm < 1: algorithm = 1
    if algorithm > 3: algorithm = 3
    algorithmName = ''
    if algorithm == 1: algorithmName = 'A-star'
    elif algorithm == 2: algorithmName = 'Bellman-Ford'
    elif algorithm == 3: algorithmName = 'Dijkstra'
    else: algorithmName = 'Unknown'


    drawGraphs = int(sys.argv[3])
    if drawGraphs == 1: drawGraphs = True
    else: displayGraphs = False


    debug = int(sys.argv[4])
    if debug == 1: debug = True
    else: debug = False


    forceGC = int(sys.argv[5])
    if forceGC == 1: forceGC = True
    else: forceGC = False
    print ("Forced garbage collection = %r" % forceGC)


    advert = "(where 1 = A* (A-star), 2 = Bellman-Ford, 3 = Dijkstra)"
    print("Running Graph-Tool pathfinding with user-selected options:\n"),
    print("  inputFilePath=%s\n  algorithm=%d  %s\n  drawGraphs=%s\n  debug=%s\n  forceGarbageCollection=%s\n" 
        % (path, algorithm, advert, drawGraphs, debug, forceGC) )


    #This version combined the elapsed time and memory consumption data collection:
    #print("\nProcessing GraphML graph files (text format) in subdir: '%s'" % path)
    #count = 0
    #for root, dirs, files in os.walk (path):
    #    for fileName in files:
    #        if fileName.endswith('.graphml'):
    #            count += 1
    #
    #            #Force a garbage collection before data collection:
    #            if forceGC:
    #                gc.enable()
    #                gc.collect()
    #
    #            print ("ALGORITHM|%s" % algorithmName)
    #           print ("INFILECOUNTER|%d" % count)
    #           print ("INFILENAME|%s" % fileName)
    #
    #            #call the function that does the pathfinding:
    #            elapsed_time = performGraphToolCalculations( fileName, path, algorithm, drawGraphs, debug )
    #
    #            elapsed_time = format( float(elapsed_time), '.4f') #bring it all through, let subsequent scripts change precision as they need.
    #            print("RESULTS|%s|elapsedTime|%s" % (algorithmName, elapsed_time) )


    #This version separates the elapsed time measurement from the memory consumption 
    #measurement, so that one measurement has no potential to interfere with the other.
    memoryMode = False # True = collect memory consumption statistics only (no elapsed time stats). False = collect elapsed time statistics only (not memory stats).
    print("\nProcessing GraphML graph files (text format) in subdir: '%s'" % path)
    count = 0
    for root, dirs, files in os.walk (path):
        for fileName in files:
            if fileName.endswith('.graphml'):
                count += 1

                #Force a garbage collection before data collection:
                if forceGC:
                    gc.enable()
                    gc.collect()

                print ("ALGORITHM|%s" % algorithmName)
                print ("INFILECOUNTER|%d" % count)
                print ("INFILENAME|%s" % fileName)

                #Part 1 of 2: Do the MEMORY CONSUMPTION assessment:
                memoryMode = True # assess (collect) memory consumption statistics only (no elapsed time stats).
                #call the function that does the (memory aware) pathfinding:
                performGraphToolCalculations( fileName, path, algorithm, drawGraphs, debug, memoryMode )

                #Part 2 of 2: Do the ELAPSED TIME assessment:
                memoryMode = False # assess (collect) elapsed time statistics only (not memory stats).
                #call the function that does the (non-memory aware) pathfinding, but get timing info:
                elapsed_time = performGraphToolCalculations( fileName, path, algorithm, drawGraphs, debug, memoryMode )
                elapsed_time = format( float(elapsed_time), '.4f') #bring it all through, let subsequent scripts change precision as they need.
                print("RESULTS|%s|elapsedTime|%s\n" % (algorithmName, elapsed_time) )

    print ("\nDone.\n")


############################################################

if __name__ == '__main__':
    main()
