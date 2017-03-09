1a. To generate 1000 small (200x200) grid maps, with p = 1.0% (i.e., p=0.01), connection depth of 2, and stratify 125 per each of 12 groups:
 . run_algorithm_instrument_graph_gen.sh -o 'graphs_200x200' -c 1000 -d 200 -k 2  -p 0.01 -n 'small_200x200_k2_p01_' -r 125


1b. To generate 1000 large (1000x1000) grid maps, with p = 2.0% (i.e., p=0.02), connection depth of 2, and stratify 125 per each of 12 groups:
 . run_algorithm_instrument_graph_gen.sh -o 'graphs_1000x1000' -c 1000 -d 1000 -k 2  -p 0.02 -n 'large_1000x1000_k2_p02_' -r 125


2. To collect the data:
 . run_algorithm_instrument_data_collection.sh 


3. To collate the CSV files:
 . run_algorithm_instrument_csv_collation.sh 


==================================================================
misc calcs:
 
200 * 2 = 400
1000* 2 = 2000

400 * .05 = 20
2000* .05 = 100

400 * .025 = 10
2000* .025 = 50

400 * .0025 = 1
2000* .0025 = 5

400 * .015 = 6
2000* .020 = 40

. run_algorithm_instrument_graph_gen.sh -o 'graphs_1000x1000' -c 750 -d 1000 -k 2  -p 0.0025 -n 'large_1000x1000_k2_p0025_' -r 125

. run_algorithm_instrument_graph_gen.sh -o 'graphs_200x200' -c 1000 -d 200 -k 2  -p 0.015 -n 'small_200x200_k2_p015_' -r 125
