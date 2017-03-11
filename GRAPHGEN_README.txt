Remember that the count parameter 'c' represents the number of graphs generated PER graph analysis framework,
and since there are 2 frameworks, the input value for 'c' should be multiplied by 2, which 
indicates that (c * 2) graphs will be generated after running the graph_gen shell script.


1a. To generate 1000 small (200x200) grid maps per graph analysis framework, with p = 2.0% (i.e., p=0.02), connection depth of 2, and stratify 150 per each of 12 groups:
 . run_algorithm_instrument_graph_gen.sh -o 'graphs_200x200' -c 1000 -d 200 -k 2  -p 0.02 -n 'small_200x200_k2_p02_' -r 150


1b. To generate 1000 large (1000x1000) grid maps per graph analysis framework, with p = 1.0% (i.e., p=0.01), connection depth of 2, and stratify 150 per each of 12 groups:
 . run_algorithm_instrument_graph_gen.sh -o 'graphs_1000x1000' -c 1000 -d 1000 -k 2  -p 0.01 -n 'large_1000x1000_k2_p01_' -r 150


2. To collect the data:
 . run_algorithm_instrument_data_collection.sh 


3. To collate the CSV files:
 . run_algorithm_instrument_csv_collation.sh 


==================================================================
misc calcs:
 
200 * 2 = 400   graphs total (half from each of the 2 graph analysis frameworks)
1000* 2 = 2000  graphs total (half from each of the 2 graph analysis frameworks)

400 * .01 = 4   this means avg 4 rewired connections in a 200x200 map with network depth 2, and rewire percentage of 1%.
2000* .01 = 20  this means avg 20 rewired connections in a 1000x1000 map with network depth 2, and rewire percentage = 1%.

400 * .02 = 8   this means avg 8 rewired connections in a 200x200 map with network depth 2, and rewire percentage of 2%.
2000* .02 = 40  this means avg 20 rewired connections in a 1000x1000 map with network depth 2, and rewire percentage = 2%.

400 * .0025 = 1  i.e., 1 avg rewired connections in a 200x200 map with network depth 2, and rewire percentage of 0.25%.
2000* .0025 = 5  i.e., 5 avg rewired connections in a 1000x1000 map with network depth 2, and rewire percentage of 0.25%.

. run_algorithm_instrument_graph_gen.sh -o 'graphs_1000x1000' -c 1000 -d 1000 -k 2  -p 0.01 -n 'large_1000x1000_k2_p01_' -r 150

. run_algorithm_instrument_graph_gen.sh -o 'graphs_200x200'  -c 1000  -d 200  -k 2  -p 0.02  -n 'small_200x200_k2_p02_'  -r 150
