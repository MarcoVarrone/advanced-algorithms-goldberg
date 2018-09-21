import sys
sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
sys.path.append("/anaconda3/lib/python2.7/site-packages")

import test_triangulation as t
import graph_tool.all as gt
from numpy.random import seed, random, random_integers
from scipy.linalg import norm
from max_flow import Goldberg
import math
from memory_profiler import profile, memory_usage

file = open("spatial_complexity_data", "w")

for i in [50, 150, 250, 500]:
    g = t.create_graph_triangulation(i)

    title = '- Parte grafo con ' + str(i) + ' nodi e ' + str(len(g.get_edges())) + ' archi.\n'
    print(title)

    file.write(title)

    g.save("flow-random.xml.gz")
    gt.graph_draw(g, edge_pen_width=gt.prop_to_size(g.ep.cap, mi=0, ma=3, power=1),
                      output="flow-random.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)
    cap = g.ep.cap
    source = 1
    sink = 2
    src, tgt = g.vertex(source), g.vertex(sink )
    solver = Goldberg(graph=g)

    usage = memory_usage((solver.get_max_flow, (src, tgt)))
    file.write(str(usage) + "\n")

file.close()