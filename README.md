Feb 10, 2017. 

This GitHub project contains Python source code used to randomly generate, stratify, and collect small-world graph data for comparative shortest path algorithm research for my doctoral study.

Steps to follow.

1. To randomly generate graph files, run this script:
    graph_generator.py

2. To randomly stratify the graph files into treatment group subdirectories, run this script:
    graph_rand_selector.py

3. To run GraphTool pathfinding algorithm tests on the graph files to generate raw data, run this script:
    graphtool-pathfinding.py

4. To collect the raw data from the aforementioned GraphTool pathfinding algorithms, run this script:
    graphtool-results-parser.py

5. To run NetworkX pathfinding algorithm tests on the graph files to generate raw data, run this script:
    networkx-pathfinding.py

6. To collect the raw data from the aforementioned NetworkX pathfinding algorithms, run this script:
    networkx-results-parser.py


Some utility scripts (which combine some of the aforementioned singular scripts) for the Wilcoxon validity/reliabilty testing:

* run_algorithm_instrument_graph_gen.sh

* run_algorithm_instrument_data_collection.sh


Caveats: 
I'm learning Python, so my Python code is probably not "Pythonic". However, the code works, so it achieves its goal.


Best regards,

Michael Moran
