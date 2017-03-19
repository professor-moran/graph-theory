#!/bin/sh

# Created: 2017-01-21
#
# (c) Michael Moran
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
# GRAPH-TOOL pathfinding -- assumes the "*.graphml" graph files already exist.
#
echo
echo "STEP 1: Generating GRAPH-TOOL data for Wilcoxon pairs test (within-group, using Group1 files for input):"
echo

<<COMMENT

# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool A*)"
date
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] Graph-Tool: A* (grp 1)"
echo '.'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1a.txt
sleep 4s
echo '..'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1b.txt
sleep 4s
echo '...'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1c.txt
sleep 4s
echo '....'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1d.txt
sleep 4s
echo '.....'
python  graphtool-pathfinding.py  graphtool-astar_grp1  1  0  0  0  >  wlcx_gt_astar_grp1e.txt
sleep 4s


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Bellman-Ford)"
date
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] Graph-Tool: Bellman-Ford (grp 1)"
echo '.'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1a.txt
sleep 4s
echo '..'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1b.txt
sleep 4s
echo '...'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1c.txt
sleep 4s
echo '....'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1d.txt
sleep 4s
echo '.....'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp1  2  0  0  0  >  wlcx_gt_bellford_grp1e.txt
sleep 4s

COMMENT


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Dijkstra)"
date
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] Graph-Tool: Dijkstra (grp 1)"
echo '.'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1a.txt
sleep 4s
echo '..'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1b.txt
sleep 4s
echo '...'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1c.txt
sleep 4s
echo '....'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1d.txt
sleep 4s
echo '.....'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp1  3  0  0  0  >  wlcx_gt_dijk_grp1e.txt
sleep 4s


###########################################
echo
echo "STEP 2: Generating GRAPH-TOOL data for Wilcoxon pairs test (within-group, using Group2 files for input):"
echo
<<COMMENT

# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool A*)"
date
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] Graph-Tool: A* (grp 2)"
echo '.'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  wlcx_gt_astar_grp2a.txt
sleep 4s
echo '..'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  wlcx_gt_astar_grp2b.txt
sleep 4s
echo '...'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  wlcx_gt_astar_grp2c.txt
sleep 4s
echo '....'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  wlcx_gt_astar_grp2d.txt
sleep 4s
echo '.....'
python  graphtool-pathfinding.py  graphtool-astar_grp2  1  0  0  0  >  wlcx_gt_astar_grp2e.txt
sleep 4s


# Warm up the Python virtual machine (Graph-Tool).
echo "Warming up Graph-Tool... (for Graph-Tool Bellman-Ford)"
date
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] Graph-Tool: Bellman-Ford (grp 2)"
echo '.'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  wlcx_gt_bellford_grp2a.txt
sleep 4s
echo '..'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  wlcx_gt_bellford_grp2b.txt
sleep 4s
echo '...'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  wlcx_gt_bellford_grp2c.txt
sleep 4s
echo '....'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  wlcx_gt_bellford_grp2d.txt
sleep 4s
echo '.....'
python  graphtool-pathfinding.py  graphtool-bellmanford_grp2  2  0  0  0  >  wlcx_gt_bellford_grp2e.txt
sleep 4s


COMMENT

# Warm up the Python virtual machine (Graph-Tool).
#echo "Warming up Graph-Tool... (for Graph-Tool Dijkstra)"
date
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] Graph-Tool: Dijkstra (grp 2)"
echo '.'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  wlcx_gt_dijk_grp2a.txt
sleep 4s
echo '..'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  wlcx_gt_dijk_grp2b.txt
sleep 4s
echo '...'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  wlcx_gt_dijk_grp2c.txt
sleep 4s
echo '....'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  wlcx_gt_dijk_grp2d.txt
sleep 4s
echo '.....'
python  graphtool-pathfinding.py  graphtool-dijkstra_grp2  3  0  0  0  >  wlcx_gt_dijk_grp2e.txt
sleep 4s



<<COMMENT

###########################################
# NetworkX pathfinding assumes the "*.csv" graph files already exist.
#
echo
echo "STEP 3: Generating NETWORKX data for Wilcoxon pairs test (within-group, using Group1 files for input):"
echo
# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX A*)"
date
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] NetworkX: A* (grp 1):"
echo '.'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1a.txt
sleep 4s
echo '..'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1b.txt
sleep 4s
echo '...'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1c.txt
sleep 4s
echo '....'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1d.txt
sleep 4s
echo '.....'
python  networkx-pathfinding.py  networkx-astar_grp1  1  0  0  0  >  wlcx_nx_astar_grp1e.txt
sleep 4s

# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Bellman-Ford)"
date
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] NetworkX: Bellman-Ford (grp 1)"
echo '.'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1a.txt
sleep 4s
echo '..'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1b.txt
sleep 4s
echo '...'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1c.txt
sleep 4s
echo '....'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1d.txt
sleep 4s
echo '.....'
python  networkx-pathfinding.py  networkx-bellmanford_grp1  2  0  0  0  >  wlcx_nx_bellford_grp1e.txt
sleep 4s

# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Dijkstra)"
date
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] NetworkX: Dijkstra (grp 1)"
echo '.'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1a.txt
sleep 4s
echo '..'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1b.txt
sleep 4s
echo '...'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1c.txt
sleep 4s
echo '....'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1d.txt
sleep 4s
echo '.....'
python  networkx-pathfinding.py  networkx-dijkstra_grp1  3  0  0  0  >  wlcx_nx_dijk_grp1e.txt
sleep 4s



###########################################
echo
echo "STEP 4: Generating NETWORKX data for Wilcoxon pairs test (within-group, using Group2 files for input):"
echo
# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX A*)"
date
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] NetworkX: A* (grp 2):"
echo '.'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  wlcx_nx_astar_grp2a.txt
sleep 4s
echo '..'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  wlcx_nx_astar_grp2b.txt
sleep 4s
echo '...'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  wlcx_nx_astar_grp2c.txt
sleep 4s
echo '....'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  wlcx_nx_astar_grp2d.txt
sleep 4s
echo '.....'
python  networkx-pathfinding.py  networkx-astar_grp2  1  0  0  0  >  wlcx_nx_astar_grp2e.txt
sleep 4s

# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Bellman-Ford)"
date
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] NetworkX: Bellman-Ford (grp 2)"
echo '.'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  wlcx_nx_bellford_grp2a.txt
sleep 4s
echo '..'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  wlcx_nx_bellford_grp2b.txt
sleep 4s
echo '...'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  wlcx_nx_bellford_grp2c.txt
sleep 4s
echo '....'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  wlcx_nx_bellford_grp2d.txt
sleep 4s
echo '.....'
python  networkx-pathfinding.py  networkx-bellmanford_grp2  2  0  0  0  >  wlcx_nx_bellford_grp2e.txt
sleep 4s

# Warm up the Python virtual machine (NetworkX).
echo "Warming up NetworkX... (for NetworkX Dijkstra)"
date
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  /dev/null
sleep 4s
echo "Warmup complete."
date
echo "[Wilcoxon] NetworkX: Dijkstra (grp 2)"
echo '.'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  wlcx_nx_dijk_grp2a.txt
sleep 4s
echo '..'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  wlcx_nx_dijk_grp2b.txt
sleep 4s
echo '...'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  wlcx_nx_dijk_grp2c.txt
sleep 4s
echo '....'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  wlcx_nx_dijk_grp2d.txt
sleep 4s
echo '.....'
python  networkx-pathfinding.py  networkx-dijkstra_grp2  3  0  0  0  >  wlcx_nx_dijk_grp2e.txt
sleep 4s



###########################################
# Move all raw output files generated above to a summary results folder for simplicity.
echo
echo "STEP 5: Moving raw output files to summary folders."
date

# Prepare the Wilcoxon data files:
rm -rf instrument-analysis-graphtool-wilcoxon
mkdir  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1d.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp1e.txt  instrument-analysis-graphtool-wilcoxon


mv  wlcx_gt_bellford_grp1a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1d.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp1e.txt  instrument-analysis-graphtool-wilcoxon


COMMENT

mv  wlcx_gt_dijk_grp1a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1d.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp1e.txt  instrument-analysis-graphtool-wilcoxon
echo "Moved Wilcoxon Graph-Tool data (grp 1) to folder: 'instrument-analysis-graphtool-wilcoxon'"
date
sleep 2s

<<COMMENT

mv  wlcx_gt_astar_grp2a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp2b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp2c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp2d.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_astar_grp2e.txt  instrument-analysis-graphtool-wilcoxon


mv  wlcx_gt_bellford_grp2a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp2b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp2c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp2d.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_bellford_grp2e.txt  instrument-analysis-graphtool-wilcoxon


COMMENT

mv  wlcx_gt_dijk_grp2a.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp2b.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp2c.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp2d.txt  instrument-analysis-graphtool-wilcoxon
mv  wlcx_gt_dijk_grp2e.txt  instrument-analysis-graphtool-wilcoxon
echo "Moved Wilcoxon Graph-Tool data (grp 2) to folder: 'instrument-analysis-graphtool-wilcoxon'"
date
sleep 2s


<<COMMENT
rm -rf instrument-analysis-networkx-wilcoxon
mkdir  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1d.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp1e.txt  instrument-analysis-networkx-wilcoxon

mv  wlcx_nx_bellford_grp1a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1d.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp1e.txt  instrument-analysis-networkx-wilcoxon

mv  wlcx_nx_dijk_grp1a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1d.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp1e.txt  instrument-analysis-networkx-wilcoxon
echo "Moved Wilcoxon NetworkX data (grp 1) to folder: 'instrument-analysis-networkx-wilcoxon'"
date
sleep 2s

mv  wlcx_nx_astar_grp2a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp2b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp2c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp2d.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_astar_grp2e.txt  instrument-analysis-networkx-wilcoxon

mv  wlcx_nx_bellford_grp2a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp2b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp2c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp2d.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_bellford_grp2e.txt  instrument-analysis-networkx-wilcoxon

mv  wlcx_nx_dijk_grp2a.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp2b.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp2c.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp2d.txt  instrument-analysis-networkx-wilcoxon
mv  wlcx_nx_dijk_grp2e.txt  instrument-analysis-networkx-wilcoxon
echo "Moved Wilcoxon NetworkX data (grp 2) to folder: 'instrument-analysis-networkx-wilcoxon'"
date
sleep 2s



###########################################
echo
echo "STEP 6: Parsing GRAPH-TOOL Wilcoxon raw output files (grp 1)..."
date
echo "A* grp1"
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1a.txt  wlcx_gt_astar_grp1a-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1b.txt  wlcx_gt_astar_grp1b-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1c.txt  wlcx_gt_astar_grp1c-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1d.txt  wlcx_gt_astar_grp1d-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1e.txt  wlcx_gt_astar_grp1e-PARSED  1  0
sleep 2s


echo "Bellman-Ford grp1"
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1a.txt  wlcx_gt_bellford_grp1a-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1b.txt  wlcx_gt_bellford_grp1b-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1c.txt  wlcx_gt_bellford_grp1c-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1d.txt  wlcx_gt_bellford_grp1d-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1e.txt  wlcx_gt_bellford_grp1e-PARSED  2  0
sleep 2s


COMMENT

echo "Dijkstra grp1"
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1a.txt  wlcx_gt_dijk_grp1a-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1b.txt  wlcx_gt_dijk_grp1b-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1c.txt  wlcx_gt_dijk_grp1c-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1d.txt  wlcx_gt_dijk_grp1d-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1e.txt  wlcx_gt_dijk_grp1e-PARSED  3  0
sleep 2s
echo "Completed parsing GRAPH-TOOL Wilcoxon raw output files (grp 1)."
date
sleep 2s



###########################################
echo
echo "STEP 7: Parsing GRAPH-TOOL Wilcoxon raw output files (grp 2)..."
date


<<COMMENT
echo "A* grp2"
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2a.txt  wlcx_gt_astar_grp2a-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2b.txt  wlcx_gt_astar_grp2b-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2c.txt  wlcx_gt_astar_grp2c-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2d.txt  wlcx_gt_astar_grp2d-PARSED  1  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2e.txt  wlcx_gt_astar_grp2e-PARSED  1  0
sleep 2s


echo "Bellman-Ford grp2"
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2a.txt  wlcx_gt_bellford_grp2a-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2b.txt  wlcx_gt_bellford_grp2b-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2c.txt  wlcx_gt_bellford_grp2c-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2d.txt  wlcx_gt_bellford_grp2d-PARSED  2  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2e.txt  wlcx_gt_bellford_grp2e-PARSED  2  0
sleep 2s


COMMENT


echo "Dijkstra grp2"
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2a.txt  wlcx_gt_dijk_grp2a-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2b.txt  wlcx_gt_dijk_grp2b-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2c.txt  wlcx_gt_dijk_grp2c-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2d.txt  wlcx_gt_dijk_grp2d-PARSED  3  0
python  graphtool-results-parser.py  instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2e.txt  wlcx_gt_dijk_grp2e-PARSED  3  0
sleep 2s
echo "Completed parsing GRAPH-TOOL Wilcoxon raw output files (grp 2)."
date
sleep 2s


<<COMMENT

###########################################
echo
echo "STEP 8: Parsing NETWORKX Wilcoxon raw output files (grp 1)..."
date
echo "A* grp1"
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1a.txt  wlcx_nx_astar_grp1a-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1b.txt  wlcx_nx_astar_grp1b-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1c.txt  wlcx_nx_astar_grp1c-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1d.txt  wlcx_nx_astar_grp1d-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1e.txt  wlcx_nx_astar_grp1e-PARSED  1  0
sleep 2s

echo "Bellman-Ford grp1"
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1a.txt  wlcx_nx_bellford_grp1a-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1b.txt  wlcx_nx_bellford_grp1b-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1c.txt  wlcx_nx_bellford_grp1c-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1d.txt  wlcx_nx_bellford_grp1d-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1e.txt  wlcx_nx_bellford_grp1e-PARSED  2  0
sleep 2s

echo "Dijkstra grp1"
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1a.txt  wlcx_nx_dijk_grp1a-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1b.txt  wlcx_nx_dijk_grp1b-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1c.txt  wlcx_nx_dijk_grp1c-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1d.txt  wlcx_nx_dijk_grp1d-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1e.txt  wlcx_nx_dijk_grp1e-PARSED  3  0
sleep 2s
echo "Completed parsing NETWORKX Wilcoxon raw output files (grp 1)."
date
sleep 2s



###########################################
echo
echo "STEP 9: Parsing NETWORKX Wilcoxon raw output files (grp 2)..."
date
echo "A* grp2"
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2a.txt  wlcx_nx_astar_grp2a-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2b.txt  wlcx_nx_astar_grp2b-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2c.txt  wlcx_nx_astar_grp2c-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2d.txt  wlcx_nx_astar_grp2d-PARSED  1  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2e.txt  wlcx_nx_astar_grp2e-PARSED  1  0
sleep 2s

echo "Bellman-Ford grp2"
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2a.txt  wlcx_nx_bellford_grp2a-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2b.txt  wlcx_nx_bellford_grp2b-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2c.txt  wlcx_nx_bellford_grp2c-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2d.txt  wlcx_nx_bellford_grp2d-PARSED  2  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2e.txt  wlcx_nx_bellford_grp2e-PARSED  2  0
sleep 2s

echo "Dijkstra grp2"
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2a.txt  wlcx_nx_dijk_grp2a-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2b.txt  wlcx_nx_dijk_grp2b-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2c.txt  wlcx_nx_dijk_grp2c-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2d.txt  wlcx_nx_dijk_grp2d-PARSED  3  0
sleep 1s
python  networkx-results-parser.py  instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2e.txt  wlcx_nx_dijk_grp2e-PARSED  3  0
sleep 2s
echo "Completed parsing NETWORKX Wilcoxon raw output files (grp 2)."
date
sleep 2s


COMMENT


###########################################
#Done with test data collection:
echo
echo "Raw test data collection and parsing complete!"
date
echo
