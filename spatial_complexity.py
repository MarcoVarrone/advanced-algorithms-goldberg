import sys
sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
sys.path.append("/anaconda3/lib/python2.7/site-packages")

import graph_tool.all as gt
from numpy.random import seed, random, randint
from scipy.linalg import norm
from max_flow_residuals import Goldberg
import math
from memory_profiler import profile, memory_usage
from generation.Triangulation import Triangulation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from generation.Random import Random

complexity = []
data = []
nodes = [50, 100, 150, 200, 250, 300, 350, 400]
edges = []
n_v = []
for i in range(0, len(nodes)):
    seed_number = randint(1, 1000)
    generator = Random(nodes[i], nodes[i] * 4, directed=True, seed_number=seed_number)
    g, source, target = generator.generate()
    edges += [str(len(g.get_edges()))]
    title = '- Parte grafo con ' + str(nodes[i]) + ' nodi e ' + edges[i] + ' archi.\n'
    print(title)
    solver = Goldberg(g)
    usage = memory_usage((solver.get_max_flow, (source, target)))
    data += [sum(usage)/len(usage)]
    print(data[i])

#for i in range(0, len(nodes)):
#    complexity += [(data[0]/float(nodes[0]))**(1/2) * float(nodes[i])**(1/2)]

for i in range(0, len(nodes)):
    n_v += [nodes[i] + int(edges[i])]

f = plt.figure()
plt.xlabel('Edge size')
plt.ylabel('Memory utilization')
plt.title("Spatial complexity Goldberg implementation")
red_patch = mpatches.Patch(color='red', label='Empirical')
plt.legend(handles=[red_patch])
plt.plot(edges, data, 'r')
plt.show()
f.savefig("complexity_graphs/spatial_complexity_data_goldberg_max_case.pdf", bbox_inches='tight')