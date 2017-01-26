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
# NOTE: This script assumes the following directories exist in the same path as
# this script, and they contain relevant text graph files ("*.csv" for NetworkX, 
# and "*.graphml" for Graph-Tool): 
#
# graphtool-astar_grp1
# graphtool-astar_grp2
# graphtool-bellmanford_grp1
# graphtool-bellmanford_grp2
# graphtool-dijkstra_grp1
# graphtool-dijkstra_grp2
# networkx-astar_grp1
# networkx-astar_grp2
# networkx-bellmanford_grp1
# networkx-bellmanford_grp2
# networkx-dijkstra_grp1
# networkx-dijkstra_grp2
#
# See shell script 'run_algorithm_instrument_graph_gen.sh' for more details.
#
# Order of operations:
#
# #1. Run this first:       'run_algorithm_instrument_graph_gen.sh'
# #2. Then run this script: 'run_algorithm_instrument_data_collection.sh'
#
#
# For reference on useful Bash script pause commands, see:
# http://stackoverflow.com/questions/21620406/how-do-i-pause-my-shell-script-for-1-second-before-continuing
# e.g., 
#   sleep 5s (for pausing 5 seconds)
#   sleep 5m (for pausing 5 minutes)
#   read -p "Press ENTER to continue"
#
###########################################


#ls -al

source activate 2.7
ls -al
date
echo "Starting algorithm instrument raw data collection."
sleep 2s
#cd /Volumes/ExtMacDrive1/edu/GRAPH_FILES


###########################################
# GRAPH-TOOL pathfinding assumes the "*.graphml" graph files already exist.
#
echo
echo "STEP 1: Generating GRAPH-TOOL data for Wilcoxon pairs test (within-group, using Group1 files for input):"

# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool A*)"
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Wilcoxon] Graph-Tool: A*"
echo '.'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1_iter1c.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1_iter1d.txt
#sleep 1s


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Bellman-Ford)"
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Wilcoxon] Graph-Tool: Bellman-Ford"
echo '.'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1_iter1c.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1_iter1d.txt
#sleep 1s


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Dijkstra)"
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Wilcoxon] Graph-Tool: Dijkstra"
echo '.'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1_iter1c.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1_iter1d.txt
#sleep 1s



###########################################
# NetworkX pathfinding assumes the "*.csv" graph files already exist.
#
echo
echo "STEP 2: Generating NETWORKX data for Wilcoxon pairs test (within-group, using Group1 files for input):"

# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX A*)"
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Wilcoxon] NetworkX: A*"
echo '.'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1_iter1a.txt
#sleep 1s

echo '..'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1_iter1b.txt
#sleep 1s

echo '...'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1_iter1c.txt
#sleep 1s

echo '....'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1_iter1d.txt
#sleep 1s


# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Bellman-Ford)"
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Wilcoxon] NetworkX: Bellman-Ford"
echo '.'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1_iter1a.txt
#sleep 1s

echo '..'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1_iter1b.txt
#sleep 1s

echo '...'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1_iter1c.txt
#sleep 1s

echo '....'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1_iter1d.txt
#sleep 1s


# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Dijkstra)"
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Wilcoxon] NetworkX: Dijkstra"
echo '.'
python  graphtool-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1_iter1c.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1_iter1d.txt
#sleep 1s



###########################################
# GRAPH-TOOL pathfinding assumes the "*.graphml" graph files already exist.
#
echo
echo "STEP 3: Generating GRAPH-TOOL data for Mann-Whitney U-Test (between-groups, using groups 1 & 2 for input):"

# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool A*)"
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Mann-Whitney] Graph-Tool: A*"
echo '.'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  mw_gt_astar_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  mw_gt_astar_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  mw_gt_astar_grp2_iter2a.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  mw_gt_astar_grp2_iter2b.txt
#sleep 1s


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Bellman-Ford)"
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Mann-Whitney] Graph-Tool: Bellman-Ford"
echo '.'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  mw_gt_bellford_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  mw_gt_bellford_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  mw_gt_bellford_grp2_iter2a.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  mw_gt_bellford_grp2_iter2b.txt
#sleep 1s


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Dijkstra)"
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Mann-Whitney] Graph-Tool: Dijkstra"
echo '.'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  mw_gt_dijk_grp1_iter1a.txt
#sleep 1s

echo '..'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  mw_gt_dijk_grp1_iter1b.txt
#sleep 1s

echo '...'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  mw_gt_dijk_grp2_iter2a.txt
#sleep 1s

echo '....'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  mw_gt_dijk_grp2_iter2b.txt
#sleep 1s




###########################################
# NetworkX pathfinding assumes the "*.csv" graph files already exist.
#
echo
echo "STEP 4: Generating NETWORKX data data for Mann-Whitney U-Test (between-groups, using groups 1 & 2 for input):"

# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX A*)"
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Mann-Whitney] NetworkX: A*"
echo '.'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  mw_nx_astar_grp1_iter1a.txt
#sleep 1s

echo '..'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  mw_nx_astar_grp1_iter1b.txt
#sleep 1s

echo '...'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  mw_nx_astar_grp2_iter2a.txt
#sleep 1s

echo '....'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  mw_nx_astar_grp2_iter2b.txt
#sleep 1s


# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Bellman-Ford)"
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Mann-Whitney] NetworkX: Bellman-Ford"
echo '.'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  mw_nx_bellford_grp1_iter1a.txt
#sleep 1s

echo '..'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  mw_nx_bellford_grp1_iter1b.txt
#sleep 1s

echo '...'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  mw_nx_bellford_grp2_iter2a.txt
#sleep 1s

echo '....'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  mw_nx_bellford_grp2_iter2b.txt
#sleep 1s


# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Dijkstra)"
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
#python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
echo "Warmup complete."

echo "[Mann-Whitney] NetworkX: Dijkstra"
echo '.'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  mw_nx_dijk_grp1_iter1a.txt
#sleep 1s

echo '..'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  mw_nx_dijk_grp1_iter1b.txt
#sleep 1s

echo '...'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  mw_nx_dijk_grp2_iter2a.txt
#sleep 1s

echo '....'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  mw_nx_dijk_grp2_iter2b.txt
#sleep 1s




###########################################
# Move all raw output files generated above to a summary results folder for simplicity.
echo
echo "STEP 5: Moving raw output files to summary folders."

# Prepare the Wilcoxon data files:
rm -rf instrument-analysis-graphtool-wilcoxon
mkdir  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1_iter1a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1_iter1b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1_iter1c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1_iter1d.txt  instrument-analysis-graphtool-wilcoxon

mv  wlcx_gt_bellford_grp1_iter1a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1_iter1b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1_iter1c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1_iter1d.txt  instrument-analysis-graphtool-wilcoxon

mv  wlcx_gt_dijk_grp1_iter1a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1_iter1b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1_iter1c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1_iter1d.txt  instrument-analysis-graphtool-wilcoxon
echo "Moved Wilcoxon Graph-Tool data to folder: 'instrument-analysis-graphtool-wilcoxon'"
sleep 1s


rm -rf instrument-analysis-networkx-wilcoxon
mkdir  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1_iter1a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1_iter1b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1_iter1c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1_iter1d.txt  instrument-analysis-networkx-wilcoxon

mv  wlcx_nx_bellford_grp1_iter1a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1_iter1b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1_iter1c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1_iter1d.txt  instrument-analysis-networkx-wilcoxon

mv  wlcx_nx_dijk_grp1_iter1a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1_iter1b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1_iter1c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1_iter1d.txt  instrument-analysis-networkx-wilcoxon
echo "Moved Wilcoxon NetworkX data to folder: 'instrument-analysis-networkx-wilcoxon'"
sleep 1s


# Prepare the Mann-Whitney data files:
rm -rf instrument-analysis-graphtool-mann-whitney
mkdir  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_astar_grp1_iter1a.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_astar_grp1_iter1b.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_astar_grp2_iter2a.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_astar_grp2_iter2b.txt  instrument-analysis-graphtool-mann-whitney

mv  mw_gt_bellford_grp1_iter1a.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_bellford_grp1_iter1b.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_bellford_grp2_iter2a.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_bellford_grp2_iter2b.txt  instrument-analysis-graphtool-mann-whitney

mv  mw_gt_dijk_grp1_iter1a.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_dijk_grp1_iter1b.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_dijk_grp2_iter2a.txt  instrument-analysis-graphtool-mann-whitney
mv  mw_gt_dijk_grp2_iter2b.txt  instrument-analysis-graphtool-mann-whitney
echo "Moved Mann-Whitney Graph-Tool data to folder: 'instrument-analysis-graphtool-mann-whitney'"
sleep 1s


rm -rf instrument-analysis-networkx-mann-whitney
mkdir  instrument-analysis-networkx-mann-whitney
mv  mw_nx_astar_grp1_iter1a.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_astar_grp1_iter1b.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_astar_grp2_iter2a.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_astar_grp2_iter2b.txt  instrument-analysis-networkx-mann-whitney

mv  mw_nx_bellford_grp1_iter1a.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_bellford_grp1_iter1b.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_bellford_grp2_iter2a.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_bellford_grp2_iter2b.txt  instrument-analysis-networkx-mann-whitney

mv  mw_nx_dijk_grp1_iter1a.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_dijk_grp1_iter1b.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_dijk_grp2_iter2a.txt  instrument-analysis-networkx-mann-whitney
mv  mw_nx_dijk_grp2_iter2b.txt  instrument-analysis-networkx-mann-whitney
echo "Moved Mann-Whitney NetworkX data to folder: 'instrument-analysis-networkx-mann-whitney'"
sleep 1s



###########################################
echo
echo "STEP 6: Parsing GRAPH-TOOL Wilcoxon raw output files..."
#A* grp1
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1_iter1a.txt  wlcx_gt_astar_grp1_iter1a-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1_iter1b.txt  wlcx_gt_astar_grp1_iter1b-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1_iter1c.txt  wlcx_gt_astar_grp1_iter1c-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1_iter1d.txt  wlcx_gt_astar_grp1_iter1d-PARSED  1  0

#Bellman-Ford grp1
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1_iter1a.txt  wlcx_gt_bellford_grp1_iter1a-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1_iter1b.txt  wlcx_gt_bellford_grp1_iter1b-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1_iter1c.txt  wlcx_gt_bellford_grp1_iter1c-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1_iter1d.txt  wlcx_gt_bellford_grp1_iter1d-PARSED  2  0

#Dijkstra grp1
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1_iter1a.txt  wlcx_gt_dijk_grp1_iter1a-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1_iter1b.txt  wlcx_gt_dijk_grp1_iter1b-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1_iter1c.txt  wlcx_gt_dijk_grp1_iter1c-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1_iter1d.txt  wlcx_gt_dijk_grp1_iter1d-PARSED  3  0
echo "Completed parsing GRAPH-TOOL Wilcoxon raw output files." 
sleep 2s


###########################################
echo
echo "STEP 7: Parsing NETWORKX Wilcoxon raw output files..."
#A* grp1
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1_iter1a.txt  wlcx_nx_astar_grp1_iter1a-PARSED  1  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1_iter1b.txt  wlcx_nx_astar_grp1_iter1b-PARSED  1  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1_iter1c.txt  wlcx_nx_astar_grp1_iter1c-PARSED  1  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1_iter1d.txt  wlcx_nx_astar_grp1_iter1d-PARSED  1  0

#Bellman-Ford grp1
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1_iter1a.txt  wlcx_nx_bellford_grp1_iter1a-PARSED  2  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1_iter1b.txt  wlcx_nx_bellford_grp1_iter1b-PARSED  2  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1_iter1c.txt  wlcx_nx_bellford_grp1_iter1c-PARSED  2  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1_iter1d.txt  wlcx_nx_bellford_grp1_iter1d-PARSED  2  0

#Dijkstra grp1
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1_iter1a.txt  wlcx_nx_dijk_grp1_iter1a-PARSED  3  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1_iter1b.txt  wlcx_nx_dijk_grp1_iter1b-PARSED  3  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1_iter1c.txt  wlcx_nx_dijk_grp1_iter1c-PARSED  3  0
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1_iter1d.txt  wlcx_nx_dijk_grp1_iter1d-PARSED  3  0
echo "Completed parsing NETWORKX Wilcoxon raw output files." 
sleep 2s


###########################################
echo
echo "STEP 8: Parsing GRAPH-TOOL Mann-Whitney raw output files..."
#A* grp1
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_astar_grp1_iter1a.txt  mw_gt_astar_grp1_iter1a-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_astar_grp1_iter1b.txt  mw_gt_astar_grp1_iter1b-PARSED  1  0

#A* grp2
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_astar_grp2_iter2a.txt  mw_gt_astar_grp2_iter2a-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_astar_grp2_iter2b.txt  mw_gt_astar_grp2_iter2b-PARSED  1  0

#Bellman-Ford grp1
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_bellford_grp1_iter1a.txt  mw_gt_bellford_grp1_iter1a-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_bellford_grp1_iter1b.txt  mw_gt_bellford_grp1_iter1b-PARSED  2  0

#Bellman-Ford grp2
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_bellford_grp2_iter2a.txt  mw_gt_bellford_grp2_iter2a-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_bellford_grp2_iter2b.txt  mw_gt_bellford_grp2_iter2b-PARSED  2  0

#Dijkstra grp1
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_dijk_grp1_iter1a.txt  mw_gt_dijk_grp1_iter1a-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_dijk_grp1_iter1b.txt  mw_gt_dijk_grp1_iter1b-PARSED  3  0

#Dijkstra grp2
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_dijk_grp2_iter2a.txt  mw_gt_dijk_grp2_iter2a-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-mann-whitney/  mw_gt_dijk_grp2_iter2b.txt  mw_gt_dijk_grp2_iter2b-PARSED  3  0
echo "Completed parsing GRAPH-TOOL Mann-Whitney raw output files." 
sleep 2s


###########################################
echo
echo "STEP 9: Parsing NETWORKX Mann-Whitney raw output files..."
#A* grp1
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_astar_grp1_iter1a.txt  mw_nx_astar_grp1_iter1a-PARSED  1  0
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_astar_grp1_iter1b.txt  mw_nx_astar_grp1_iter1b-PARSED  1  0

#A* grp2
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_astar_grp2_iter2a.txt  mw_nx_astar_grp2_iter2a-PARSED  1  0
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_astar_grp2_iter2b.txt  mw_nx_astar_grp2_iter2b-PARSED  1  0

#Bellman-Ford grp1
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_bellford_grp1_iter1a.txt  mw_nx_bellford_grp1_iter1a-PARSED  2  0
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_bellford_grp1_iter1b.txt  mw_nx_bellford_grp1_iter1b-PARSED  2  0

#Bellman-Ford grp2
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_bellford_grp2_iter2a.txt  mw_nx_bellford_grp2_iter2a-PARSED  2  0
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_bellford_grp2_iter2b.txt  mw_nx_bellford_grp2_iter2b-PARSED  2  0

#Dijkstra grp1
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_dijk_grp1_iter1a.txt  mw_nx_dijk_grp1_iter1a-PARSED  3  0
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_dijk_grp1_iter1b.txt  mw_nx_dijk_grp1_iter1b-PARSED  3  0

#Dijkstra grp2
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_dijk_grp2_iter2a.txt  mw_nx_dijk_grp2_iter2a-PARSED  3  0
python  networkx-results-parser.py  instrument-analysis-networkx-mann-whitney/  mw_nx_dijk_grp2_iter2b.txt  mw_nx_dijk_grp2_iter2b-PARSED  3  0
echo "Completed parsing NETWORKX Mann-Whitney raw output files." 
sleep 2s


###########################################
#Done with test data collection:
echo
echo "Raw test data collection complete!"
date
