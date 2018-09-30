# Advanced Algorithms Project - Push Relabel algorithm
This repository contains the code related to the implementation of the 
Goldberg's algorithm, also called Push-Relabel algorithm.<br />
Three versions of the algorithm are implemented:
* Generic algorithm: the active vertices (with excess > 0) are selected randomly
* Heighest label preflow: the active vertices are selected based on which has the larget height
* Wave implementation (Lift-to-front): when a vertex is relabeled, 
it is placed at the beginning of the ordered active node list <br>

## Requirements
### Execution
The following packages are required for the execution of the algorithm:
* Python 3.x
* [graph-tool](https://graph-tool.skewed.de/): for building and manipulating graphs
* [numpy](http://www.numpy.org/): for handling vertex and edge matrices
and random numbers generation
* [argparse](https://docs.python.org/3/library/argparse.html): for passing arguments to main script
* [Cython](http://cython.org/): for improving runtime performance by compiling Python code into C code

### Testing
The following packages are required for the execution of the test routines:
* [pytest](https://docs.pytest.org/en/latest/): for running unit tests
* [cProfile](https://docs.python.org/3/library/profile.html) and [pstats](https://docs.python.org/3.6/library/profile.html): for performing time complexity analysis
* [memory_profiler](https://pypi.org/project/memory_profiler/): for performing space complexity analysis
* [matplotlib](https://matplotlib.org/): for plotting complexity test results

## Execution
### Compilation
The three files corresponding to the different implementations must be first compiled.<br>
It is sufficient to execute `python setup.py build_ext --inplace`

### Execution
The algorithm can be executed by calling `python main.py`
followed by the possible arguments:<br>
**-h --help** show help message and exit <br>
**-g --graph {random, scale-free, simple, delaunay}** select the type of graph to generate <br>
**-n --nodes <NODES>** declare the number of nodes in the graph <br>
**-m --edges <EDGES>** declare the number of edges in the graph (available only for random graph) <br>
**-s --seed <SEED>** set the seed number for the graph generation <br>
**-d --directed** set the graph as directed (Default) <br>
**-u --undirected** set the graph as undirected <br>
**-a --algorithm {generic,height,wave}** select the algorithm to compute the maximum flow (Default: generic) <br>
**-c --compare** if used, the maximum flow value will be compared with the one resulting from the graph-tool library 

### Unit tests
To perform unit testing it sufficient to call `pytest --disable-pytest-warnings`.<br>
The following tests will be executed:
![tests](https://image.ibb.co/eBeW1z/Cattura.png)

test_source_sinks.py checks if the created graphs have one and only one source and one and only one sink.<br>
The other tests check if the maximum flow returned by the implementation is correct by comparing it
with the value returned by graph-tool.

### Complexity analysis
