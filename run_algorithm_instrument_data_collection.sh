#!/bin/sh

# Created: 2017-01-21
#
# This is the main test harness driver for my doctoral study's algorithm
# instrument validation and reliability tests.
# It's purpose is the run the pathfinding tests on (already existing) graph
# files, and then parses the raw output for export to CSV (Excel) and then
# eventually into SPSS (for statistical analyses).
# This file assumes the graph files have already been generated.
# If the graph files have not been generated, then consider running
# the graph generation script (or running its steps manually):
#   run_graph_gen.sh
#
# Useful "pause" commands:
#   sleep 5s (for pausing 5 seconds)
#   sleep 5m (for pausing 5 minutes)
#   read -p "Press ENTER to continue"
#
# For reference, see:
# http://stackoverflow.com/questions/21620406/how-do-i-pause-my-shell-script-for-1-second-before-continuing
#
###########################################


ls -al

echo "Running algorithm instrument tests."
date
source activate 2.7
cd /Volumes/ExtMacDrive1/edu/GRAPH_FILES


###########################################
#STEP 1: Generate the GRAPH-TOOL pathfinding data (assumes the *.graphml graph files already exist).
#

#Group (i.e., iteration) #1:
#_______________________
#(do each of the following commands, 3 times): 
echo "STEP 1: Generating GRAPH-TOOL data..."

python  graphtool-pathfinding.py  mann-whitney-graphtool-astar_grp1  1  0  0  0  >  mw_gt_astar_grp1.txt
echo '.'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-astar_grp1  1  0  0  0  >  mw_gt_astar_grp1.txt
echo '..'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-astar_grp1  1  0  0  0  >  mw_gt_astar_grp1.txt
echo '...'
sleep 2s

python  graphtool-pathfinding.py  mann-whitney-graphtool-bellmanford_grp1  2  0  0  0  >  mw_gt_bellford_grp1.txt
echo '....'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-bellmanford_grp1  2  0  0  0  >  mw_gt_bellford_grp1.txt
echo '.....'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-bellmanford_grp1  2  0  0  0  >  mw_gt_bellford_grp1.txt
echo '......'
sleep 2s

python  graphtool-pathfinding.py  mann-whitney-graphtool-dijkstra_grp1  3  0  0  0  >  mw_gt_dijk_grp1.txt
echo '.......'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-dijkstra_grp1  3  0  0  0  >  mw_gt_dijk_grp1.txt
echo '........'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-dijkstra_grp1  3  0  0  0  >  mw_gt_dijk_grp1.txt
echo '.........'
sleep 2s
echo "GRAPH-TOOL data created for group 1 (of 2)."

#Group (i.e., iteration) #2:
#_______________________
#(do each of the following commands, 3 times):

python  graphtool-pathfinding.py  mann-whitney-graphtool-astar_grp2  1  0  0  0  >  mw_gt_astar_grp2.txt
echo '.'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-astar_grp2  1  0  0  0  >  mw_gt_astar_grp2.txt
echo '..'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-astar_grp2  1  0  0  0  >  mw_gt_astar_grp2.txt
echo '...'
sleep 2s

python  graphtool-pathfinding.py  mann-whitney-graphtool-bellmanford_grp2  2  0  0  0  >  mw_gt_bellford_grp2.txt
echo '....'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-bellmanford_grp2  2  0  0  0  >  mw_gt_bellford_grp2.txt
echo '.....'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-bellmanford_grp2  2  0  0  0  >  mw_gt_bellford_grp2.txt
echo '......'
sleep 2s

python  graphtool-pathfinding.py  mann-whitney-graphtool-dijkstra_grp2  3  0  0  0  >  mw_gt_dijk_grp2.txt
echo '.......'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-dijkstra_grp2  3  0  0  0  >  mw_gt_dijk_grp2.txt
echo '........'
sleep 2s
python  graphtool-pathfinding.py  mann-whitney-graphtool-dijkstra_grp2  3  0  0  0  >  mw_gt_dijk_grp2.txt
echo '.........'
sleep 2s
echo "GRAPH-TOOL data created for group 2 (of 2)."
sleep 2s


###########################################
#STEP 2: Generate the NetworkX pathfinding data (assumes the *.csv graph files already exist):
#
#Group (i.e., iteration) #1:
#_______________________
#(do each of the following commands, 3 times): 
echo "STEP 2: Generating NETWORKX data..."

python  networkx-pathfinding.py  mann-whitney-networkx-astar_grp1  1  0  0  0  >  mw_nx_astar_grp1.txt
echo '.'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-astar_grp1  1  0  0  0  >  mw_nx_astar_grp1.txt
echo '..'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-astar_grp1  1  0  0  0  >  mw_nx_astar_grp1.txt
echo '...'
sleep 1s

python  networkx-pathfinding.py  mann-whitney-networkx-bellmanford_grp1  2  0  0  0  >  mw_nx_bellford_grp1.txt
echo '....'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-bellmanford_grp1  2  0  0  0  >  mw_nx_bellford_grp1.txt
echo '.....'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-bellmanford_grp1  2  0  0  0  >  mw_nx_bellford_grp1.txt
echo '......'
sleep 1s

python  networkx-pathfinding.py  mann-whitney-networkx-dijkstra_grp1  3  0  0  0  >  mw_nx_dijk_grp1.txt
echo '.......'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-dijkstra_grp1  3  0  0  0  >  mw_nx_dijk_grp1.txt
echo '........'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-dijkstra_grp1  3  0  0  0  >  mw_nx_dijk_grp1.txt
echo '.........'
sleep 1s
echo "NETWORKX data created for group 1 (of 2)."

#Group (i.e., iteration) #2:
#_______________________
#(do each of the following commands, 3 times): 

python  networkx-pathfinding.py  mann-whitney-networkx-astar_grp2  1  0  0  0  >  mw_nx_astar_grp2.txt
echo '.'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-astar_grp2  1  0  0  0  >  mw_nx_astar_grp2.txt
echo '..'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-astar_grp2  1  0  0  0  >  mw_nx_astar_grp2.txt
echo '...'
sleep 1s

python  networkx-pathfinding.py  mann-whitney-networkx-bellmanford_grp2  2  0  0  0  >  mw_nx_bellford_grp2.txt
echo '....'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-bellmanford_grp2  2  0  0  0  >  mw_nx_bellford_grp2.txt
echo '.....'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-bellmanford_grp2  2  0  0  0  >  mw_nx_bellford_grp2.txt
echo '......'
sleep 1s

python  networkx-pathfinding.py  mann-whitney-networkx-dijkstra_grp2  3  0  0  0  >  mw_nx_dijk_grp2.txt
echo '.......'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-dijkstra_grp2  3  0  0  0  >  mw_nx_dijk_grp2.txt
echo '........'
sleep 1s
python  networkx-pathfinding.py  mann-whitney-networkx-dijkstra_grp2  3  0  0  0  >  mw_nx_dijk_grp2.txt
echo '.........'
sleep 1s
echo "NETWORKX data created for group 2 (of 2)."
sleep 1s


###########################################
#STEP 3: Moving all raw output files generated above to a work results folder for simplicity.
echo "STEP 3: Movinging raw output files to working folder."
rm -rf mann-whitney-instrument-analysis
mkdir mann-whitney-instrument-analysis
mv  mw_gt_astar_grp1.txt  mann-whitney-instrument-analysis
mv  mw_gt_bellford_grp1.txt  mann-whitney-instrument-analysis
mv  mw_gt_dijk_grp1.txt  mann-whitney-instrument-analysis

mv  mw_gt_astar_grp2.txt  mann-whitney-instrument-analysis
mv  mw_gt_bellford_grp2.txt  mann-whitney-instrument-analysis
mv  mw_gt_dijk_grp2.txt  mann-whitney-instrument-analysis

mv  mw_nx_astar_grp1.txt  mann-whitney-instrument-analysis
mv  mw_nx_bellford_grp1.txt  mann-whitney-instrument-analysis
mv  mw_nx_dijk_grp1.txt  mann-whitney-instrument-analysis

mv  mw_nx_astar_grp2.txt  mann-whitney-instrument-analysis
mv  mw_nx_bellford_grp2.txt  mann-whitney-instrument-analysis
mv  mw_nx_dijk_grp2.txt  mann-whitney-instrument-analysis
echo "Moved pathfinding raw output files to folder: 'mann-whitney-instrument-analysis'"
sleep 2s


###########################################
#STEP 4: Parse the GRAPH-TOOL raw output files to get the actual GRAPH-TOOL results.
echo "STEP 4: Parsing GRAPH-TOOL raw output files..."

#Group (i.e., iteration) #1:
#_______________________
python  graphtool-results-parser.py  mann-whitney-instrument-analysis/  mw_gt_astar_grp1.txt  mw_gt_astar_grp1-PARSED  1  0
python  graphtool-results-parser.py  mann-whitney-instrument-analysis/  mw_gt_bellford_grp1.txt  mw_gt_bellford_grp1-PARSED  2  0
python  graphtool-results-parser.py  mann-whitney-instrument-analysis/  mw_gt_dijk_grp1.txt  mw_gt_dijk_grp1-PARSED  3  0

#Group (i.e., iteration) #2:
#_______________________
python  graphtool-results-parser.py  mann-whitney-instrument-analysis/  mw_gt_astar_grp2.txt  mw_gt_astar_grp2-PARSED  1  0
python  graphtool-results-parser.py  mann-whitney-instrument-analysis/  mw_gt_bellford_grp2.txt  mw_gt_bellford_grp2-PARSED  2  0
python  graphtool-results-parser.py  mann-whitney-instrument-analysis/  mw_gt_dijk_grp2.txt  mw_gt_dijk_grp2-PARSED  3  0
echo "Completed parsing GRAPH-TOOL raw output files." 
sleep 2s


###########################################
#STEP 5: Parse the NETWORKX raw output files to get the actual NETWORKX results.
echo "STEP 5: Parsing NETWORKX raw output files..."

#Group (i.e., iteration) #1:
#_______________________
python  networkx-results-parser.py  mann-whitney-instrument-analysis/  mw_nx_astar_grp1.txt  mw_nx_astar_grp1-PARSED  1  0
python  networkx-results-parser.py  mann-whitney-instrument-analysis/  mw_nx_bellford_grp1.txt  mw_nx_bellford_grp1-PARSED  2  0
python  networkx-results-parser.py  mann-whitney-instrument-analysis/  mw_nx_dijk_grp1.txt  mw_nx_dijk_grp1-PARSED  3  0

#Group (i.e., iteration) #2:
#_______________________
python  networkx-results-parser.py  mann-whitney-instrument-analysis/  mw_nx_astar_grp2.txt  mw_nx_astar_grp2-PARSED  1  0
python  networkx-results-parser.py  mann-whitney-instrument-analysis/  mw_nx_bellford_grp2.txt  mw_nx_bellford_grp2-PARSED  2  0
python  networkx-results-parser.py  mann-whitney-instrument-analysis/  mw_nx_dijk_grp2.txt  mw_nx_dijk_grp2-PARSED  3  0
echo "Completed parsing NETWORKX raw output files." 
sleep 2s


###########################################
#Done with test data generation:
echo "Test data generation complete!"
sleep 2s
date
