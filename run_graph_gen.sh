#!/bin/sh

# Created: 2017-01-22
#
# The purpose of this script is to automate the raw graph file creation process.
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
echo "run_graph_gen.sh -f {folder name: str} -c {count: int} -d {dimension: int} -k {cluster depth: int} -p {randomization factor: float} -n {filename prefix: str}"
echo
echo "Examples:"
echo ". run_graph_gen.sh -f 'graphs_100'  -c 2000  -d 100  -k 2  -p 0.05  -n 'small_100x100_k2_p05_'"
echo ". run_graph_gen.sh -f 'graphs_1000'  -c 2000  -d 1000  -k 2  -p 0.0025  -n 'large_1000x1000_k2_p0025_'"
echo

while [[ $# -gt 1 ]]
do
    key="$1"

    case $key in

        -f|--folder)
        FOLDER="$2"
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
        
        *)
         # unknown option
        ;;

    esac
    shift # past argument or value

done


echo Running with the following inputs:
echo
#echo Folder name = "${FOLDER}"
#echo Files to generate = "${COUNT}"
echo Folder name = $FOLDER
echo Files to generate = $COUNT
echo Map dimensions [2D grid cell map] = $DIMENSION x $DIMENSION
echo Clustering depth = $K
echo Randomization coefficient = $P
echo Output filename prefix = $N
echo


echo Done!
