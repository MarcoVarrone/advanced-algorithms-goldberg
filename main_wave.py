import sys
sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
sys.path.append("/anaconda3/lib/python2.7/site-packages")

import graph_tool.all as gt
from numpy.random import seed, random, random_integers
from scipy.linalg import norm
from scipy.stats import poisson
from max_flow_residuals import Goldberg
from max_flow_wave import GoldbergWave
import numpy as np
import math
from generation.Triangulation import Triangulation

# Number of nodes
N = 5
# Number of edges
M = 10

seed_number = 45
generator = Triangulation(N, directed=False, seed_number=seed_number)
g, src, tgt = generator.generate()

cap = g.ep.cap
gt.graph_draw(g, edge_pen_width=gt.prop_to_size(cap, mi=1, ma=1, power=1),
                  output="graph_to_solve.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)

# using GraphTool algorithm, find the solution to test and print the resulting graph
res = gt.push_relabel_max_flow(g, src, tgt, cap)
res.a = cap.a - res.a  # the actual flow
max_flow = sum(res[e] for e in tgt.in_edges())
print("Il max flow trovato da GraphTool è:", max_flow)
labels = g.new_edge_property("string")
for edge in g.edges():
    labels[edge] = str(res[edge]) + "/" + str(cap[edge])

gt.graph_draw(g, edge_pen_width=gt.prop_to_size(res, mi=1, ma=5, power=1),
              output="max-flow-library-solution.pdf", vertex_text=g.vertex_index, edge_text=labels)

# using WaveImplementation, find the solution to test and print the resulting graph
solver = GoldbergWave(graph=g)
solution = solver.get_max_flow(src, tgt)
print("Il max flow trovato da Wave è:", solution)

labels = g.new_vertex_property("string")
for vertex in g.vertices():
    labels[vertex] = str(g.vertex_index[vertex]) + "(" + str(g.vp.height[vertex]) + "," + str(
        g.vp.excess[vertex]) + ")"

gt.graph_draw(g, edge_pen_width=gt.prop_to_size(g.ep.residual, mi=1, ma=5, power=1),
              output="max-flow-wave-solution.pdf", vertex_text=labels, edge_text=g.ep.residual)