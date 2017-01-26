#!/bin/sh

# Created: 2017-01-22
#
# The purpose of this script is to automate the raw graph file creation process.
# It will also random stratify the graph samples into the appropriate 12 test
# folders needed for Mann-Whitney U-Test work (6 for GraphTool, and 6 for NetworkX).
# Rather than run the underlying Python scripts manually, this shell script
# will automate the process.
# For shell scripting help parsing space-separated command-line parameters, 
# see the following link:
#
# http://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
#
###########################################


echo
echo "Usage:"
echo "run_graph_gen.sh -f {folder name: str} -c {count: int} -d {dimension: int} -k {cluster depth: int} -p {randomization factor: float} -n {filename prefix: str} -r {number to random stratify: int}"
echo
echo "Examples:"
echo ". run_algorithm_instrument_graph_gen.sh -o 'graphs_100x100'  -c 24  -d 100  -k 2  -p 0.05  -n 'small_100x100_k2_p05_' -r 2"
echo ". run_algorithm_instrument_graph_gen.sh -o 'graphs_100x100'  -c 2500  -d 100  -k 2  -p 0.05  -n 'small_100x100_k2_p05_' -r 200"
echo ". run_algorithm_instrument_graph_gen.sh -o 'graphs_1000x1000'  -c 2000  -d 1000  -k 2  -p 0.0025  -n 'large_1000x1000_k2_p0025_' -r 100"
echo
echo "Make sure that (r * 6) <= c, since there are 6 groups (per graph analysis framework) c must be divided into"
echo

while [[ $# -gt 1 ]]
do
    key="$1"

    case $key in

        -o|--outfolder)
        OUTFOLDER="$2"
        shift # past argument
        ;;
        
        -c|--count)
        COUNT="$2"
        shift # past argument
        ;;
        
        -d|--dimension)
        DIMENSION="$2"
        shift # past argument
        ;;
        
        -k|--kdepth)
        K="$2"
        shift # past argument
        ;;
        
        -p|--prandom)
        P="$2"
        shift # past argument
        ;;
        
        -n|--nameprefix)
        N="$2"
        shift # past argument
        ;;
        
        -r|--randomstratify)
        NUMSTRATIFY="$2"
        shift # past argument
        ;;
        
        *)
         # unknown option
        ;;

    esac
    shift # past argument or value

done


source activate 2.7


echo Running with the following inputs:
echo
#echo Folder name = "${FOLDER}"
#echo Files to generate = "${COUNT}"
echo Output folder name = $OUTFOLDER
echo Files to generate = $COUNT
echo Map dimensions [2D grid cell map] = $DIMENSION x $DIMENSION
echo Clustering depth = $K
echo Randomization coefficient = $P
echo Output filename prefix = $N
echo Number to random stratify into each treatment group = $NUMSTRATIFY
echo


#Check for null or empty values. Exit if any of the inputs are null.
if [ -z "$OUTFOLDER" ]
then
      echo "OUTFOLDER is empty"
      exit 1

elif [ -z "$COUNT" ]
then
      echo "COUNT is empty"
      exit 1

elif [ -z "$DIMENSION" ]
then
      echo "DIMENSION is empty"
      exit 1

elif [ -z "$K" ]
then
      echo "K is empty"
      exit 1

elif [ -z "$P" ]
then
      echo "P is empty"
      exit 1

elif [ -z "$N" ]
then
      echo "N is empty"
      exit 1

elif [ -z "$NUMSTRATIFY" ]
then
      echo "NUMSTRATIFY is empty"
      exit 1
#else
#      echo "\$NUMSTRATIFY is NOT empty"
fi


#PART 1. Create main graph file output folder
echo "(Re)Creating folder: " $OUTFOLDER
rm -rf $OUTFOLDER
mkdir $OUTFOLDER


#<<"COMMENT"


#PART 2. Random generate the graph files
echo "Running Python script to generate " $COUNT " graphs."
python graph_generator.py $COUNT $DIMENSION $K $P $OUTFOLDER $N graphml 1 0


#PART 3. Create statistical treatment group folders.
echo "Creating statistic output folders."
rm -rf graphtool-astar_grp1
rm -rf graphtool-astar_grp2
rm -rf graphtool-bellmanford_grp1
rm -rf graphtool-bellmanford_grp2
rm -rf graphtool-dijkstra_grp1
rm -rf graphtool-dijkstra_grp2
rm -rf networkx-astar_grp1
rm -rf networkx-astar_grp2
rm -rf networkx-bellmanford_grp1
rm -rf networkx-bellmanford_grp2
rm -rf networkx-dijkstra_grp1
rm -rf networkx-dijkstra_grp2

mkdir graphtool-astar_grp1
mkdir graphtool-astar_grp2
mkdir graphtool-bellmanford_grp1
mkdir graphtool-bellmanford_grp2
mkdir graphtool-dijkstra_grp1
mkdir graphtool-dijkstra_grp2
mkdir networkx-astar_grp1
mkdir networkx-astar_grp2
mkdir networkx-bellmanford_grp1
mkdir networkx-bellmanford_grp2
mkdir networkx-dijkstra_grp1
mkdir networkx-dijkstra_grp2


#PART 4. Random stratification and assignment to target folders (GraphTool):
python  graph_rand_selector.py  $OUTFOLDER  graphtool-astar_grp1/  $NUMSTRATIFY  1  0
python  graph_rand_selector.py  $OUTFOLDER  graphtool-astar_grp2/  $NUMSTRATIFY  1  0
python  graph_rand_selector.py  $OUTFOLDER  graphtool-bellmanford_grp1/  $NUMSTRATIFY  1  0
python  graph_rand_selector.py  $OUTFOLDER  graphtool-bellmanford_grp2/  $NUMSTRATIFY  1  0
python  graph_rand_selector.py  $OUTFOLDER  graphtool-dijkstra_grp1/  $NUMSTRATIFY  1  0
python  graph_rand_selector.py  $OUTFOLDER  graphtool-dijkstra_grp2/  $NUMSTRATIFY  1  0


#PART 5. Random stratification and assignment to target folders (NetworkX):
python  graph_rand_selector.py  $OUTFOLDER  networkx-astar_grp1/  $NUMSTRATIFY  0  0
python  graph_rand_selector.py  $OUTFOLDER  networkx-astar_grp2/  $NUMSTRATIFY  0  0
python  graph_rand_selector.py  $OUTFOLDER  networkx-bellmanford_grp1/  $NUMSTRATIFY  0  0
python  graph_rand_selector.py  $OUTFOLDER  networkx-bellmanford_grp2/  $NUMSTRATIFY  0  0
python  graph_rand_selector.py  $OUTFOLDER  networkx-dijkstra_grp1/  $NUMSTRATIFY  0  0
python  graph_rand_selector.py  $OUTFOLDER  networkx-dijkstra_grp2/  $NUMSTRATIFY  0  0


#COMMENT

echo
echo Done!
