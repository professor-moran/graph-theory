#!/bin/sh

# Created: 2017-02-19
#
# This script collates the data already generated, processed and put into 
# CSV files from either:
# (1) manually calling the Python script:  graphtool-results-parser.py
# (2) or manually calling the Python script: networkx-results-parser.py
# (3) or calling the automated shell script: run_algorithm_instrument_data_collection.sh
#
# NOTE: This script assumes the following directories exist in the same path as this
# current running script, and they contain relevant (PARSED) *.csv file output 
# (for Graph-Tool and NetworkX pathfinding algorithm output, respectively):
#
#   (1) instrument-analysis-graphtool-wilcoxon/
#   (2) instrument-analysis-networkx-wilcoxon/
#
# NOTE 2: This script assumes the following Python script, which does the actual
# combining of *.csv file output, exists in the same path as this current running script:
#
#   csv_combiner.py
#
###########################################


#ls -al

source activate 2.7
ls -al
date
echo "Starting collation of parsed algorithm data results (from Wilcoxon tests)."
sleep 2s
#cd /Volumes/ExtMacDrive1/edu/GRAPH_FILES


###########################################
# CLEANUP - remove existing files with the same names as the output files to be generated:
#
echo
echo "STEP 0: Pre-cleaning and initialization."
echo
rm ./instrument-analysis-graphtool-wilcoxon/wlcx_gt_astar_grp1abcde-COMBINED.csv
rm ./instrument-analysis-graphtool-wilcoxon/wlcx_gt_astar_grp2abcde-COMBINED.csv
rm ./instrument-analysis-graphtool-wilcoxon/wlcx_gt_bellford_grp1abcde-COMBINED.csv
rm ./instrument-analysis-graphtool-wilcoxon/wlcx_gt_bellford_grp2abcde-COMBINED.csv
rm ./instrument-analysis-graphtool-wilcoxon/wlcx_gt_dijk_grp1abcde-COMBINED.csv
rm ./instrument-analysis-graphtool-wilcoxon/wlcx_gt_dijk_grp2abcde-COMBINED.csv
sleep 5s
rm ./instrument-analysis-networkx-wilcoxon/wlcx_nx_astar_grp1abcde-COMBINED.csv
rm ./instrument-analysis-networkx-wilcoxon/wlcx_nx_astar_grp2abcde-COMBINED.csv
rm ./instrument-analysis-networkx-wilcoxon/wlcx_nx_bellford_grp1abcde-COMBINED.csv
rm ./instrument-analysis-networkx-wilcoxon/wlcx_nx_bellford_grp2abcde-COMBINED.csv
rm ./instrument-analysis-networkx-wilcoxon/wlcx_nx_dijk_grp1abcde-COMBINED.csv
rm ./instrument-analysis-networkx-wilcoxon/wlcx_nx_dijk_grp2abcde-COMBINED.csv
sleep 5s


###########################################
# GRAPH-TOOL - data file collation
#
echo
echo "STEP 1: Collating GRAPH-TOOL 'A*' algorithm data (for Group 1):"
echo
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1a-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1b-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1c-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1d-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1e-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp1abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 2: Collating GRAPH-TOOL 'Bellman-Ford' algorithm data (for Group 1):"
echo
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1a-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1b-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1c-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1d-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1e-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp1abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 3: Collating GRAPH-TOOL 'Dijkstra' algorithm data (for Group 1):"
echo
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1a-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1b-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1c-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1d-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1e-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp1abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 4: Collating GRAPH-TOOL 'A*' algorithm data (for Group 2):"
echo
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2a-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2b-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2c-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2d-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2e-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_astar_grp2abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 5: Collating GRAPH-TOOL 'Bellman-Ford' algorithm data (for Group 2):"
echo
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2a-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2b-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2c-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2d-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2e-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_bellford_grp2abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 6: Collating GRAPH-TOOL 'Dijkstra' algorithm data (for Group 2):"
echo
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2a-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2b-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2c-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2d-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2e-PARSED.csv  ./instrument-analysis-graphtool-wilcoxon/  wlcx_gt_dijk_grp2abcde-COMBINED.csv  e  0
sleep 2s


###########################################
# NETWORK-X - data file collation
#
echo
echo "STEP 7: Collating NETWORK-X 'A*' algorithm data (for Group 1):"
echo
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1a-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1b-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1c-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1d-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1e-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp1abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 8: Collating NETWORK-X 'Bellman-Ford' algorithm data (for Group 1):"
echo
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1a-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1b-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1c-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1d-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1e-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp1abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 9: Collating NETWORK-X 'Dijkstra' algorithm data (for Group 1):"
echo
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1a-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1b-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1c-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1d-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1e-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp1abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 10: Collating NETWORK-X 'A*' algorithm data (for Group 2):"
echo
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2a-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2b-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2c-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2d-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2e-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_astar_grp2abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 11: Collating NETWORK-X 'Bellman-Ford' algorithm data (for Group 2):"
echo
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2a-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2b-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2c-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2d-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2e-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_bellford_grp2abcde-COMBINED.csv  e  0
sleep 2s


echo
echo "STEP 12: Collating NETWORK-X 'Dijkstra' algorithm data (for Group 2):"
echo
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2a-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2abcde-COMBINED.csv  a  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2b-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2abcde-COMBINED.csv  b  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2c-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2abcde-COMBINED.csv  c  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2d-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2abcde-COMBINED.csv  d  0
python  csv_combiner.py  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2e-PARSED.csv  ./instrument-analysis-networkx-wilcoxon/  wlcx_nx_dijk_grp2abcde-COMBINED.csv  e  0
sleep 2s


###########################################
#Done with test data collation:
echo
echo "Data file collation complete!"
date
echo
