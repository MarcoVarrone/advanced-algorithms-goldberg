try:
    from itertools import izip
except:
    import sys
    sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
    sys.path.append("/anaconda3/lib/python2.7/site-packages")

from io import StringIO
import cProfile, pstats
import test_triangulation as t
import graph_tool.all as gt
from numpy.random import seed, random, random_integers
from scipy.linalg import norm
from max_flow import Goldberg
import math

file = open("temporal_complexity.log", "w")

for i in [10, 30, 60, 80, 100, 150, 200, 250]:
    title = '- Parte grafo con ' + str(i) + ' nodi.'
    print(title)
    file.write(title)
    g = t.create_graph_triangulation(i)
    g.save("flow-random.xml.gz")
    gt.graph_draw(g, edge_pen_width=gt.prop_to_size(g.ep.cap, mi=0, ma=3, power=1),
                      output="flow-random.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)
    cap = g.ep.cap
    source = 1
    sink = 2
    src, tgt = g.vertex(source), g.vertex(sink)
    solver = Goldberg(graph=g)

    pr = cProfile.Profile()
    pr.enable()

    solution = solver.get_max_flow(src, tgt)
    #res = gt.push_relabel_max_flow(g, src, tgt, cap)

    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    file.write(s.getvalue())

file.close()

