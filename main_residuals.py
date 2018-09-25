import sys

sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
sys.path.append("/anaconda3/lib/python2.7/site-packages")

import graph_tool.all as gt
from numpy.random import seed, random, random_integers, randint
from scipy.linalg import norm
from scipy.stats import poisson
from max_flow_residuals import Goldberg
from wave_implementation import WaveImplementation
import numpy as np
import math
from generation.Triangulation import Triangulation
from generation.Wikipedia import Wikipedia
from generation.Random import Random

# Number of nodes
N = 50
# Number of edges
M = 10


def create_graph():
    g = gt.Graph()
    s = g.add_vertex()
    v = g.add_vertex()
    w = g.add_vertex()
    t = g.add_vertex()

    e1 = g.add_edge(s, v)
    e2 = g.add_edge(s, w)
    e3 = g.add_edge(v, w)
    e4 = g.add_edge(w, v)
    e5 = g.add_edge(v, t)
    e6 = g.add_edge(w, t)

    capacity = g.new_edge_property("int", 0)
    capacity[e1] = 1
    capacity[e2] = 100
    capacity[e3] = 100
    capacity[e4] = 1
    capacity[e5] = 100
    capacity[e6] = 1
    g.ep.cap = capacity
    return g


def create_reverse_edges(self, graph):
    edges = list(graph.edges())
    temp_edges = list()
    # reciprocate edges
    if not self.directed:
        for e in edges:
            if not graph.edge(e.target(), e.source()):
                new_edge = graph.add_edge(e.target(), e.source())
                temp_edges.append(new_edge)
    return graph


'''#seed_number = randint(1, 1000)
# generator = Random(10, 40, directed=True, seed_number=seed_number)
seed_number = 386
generator = Triangulation(50, type="delaunay", directed=True, seed_number=seed_number)
# generator = Wikipedia()
g, source, target = generator.generate()
print("Source: " + str(source) + " target " + str(target))

gt.graph_draw(g, edge_pen_width=gt.prop_to_size(g.ep.cap, mi=1, ma=5, power=1),
              output="cf/cf_capacities.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)'''
#seed_number = randint(1, 1000)
seed_number = 14
generator = Triangulation(50, type="delaunay", directed=True, seed_number=seed_number)
g, source, target = generator.generate()

gt.graph_draw(g, edge_pen_width=gt.prop_to_size(g.ep.cap, mi=1, ma=5, power=1),
              output="cf/cf_capacities.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)

# source = g.vertex(0)
# target = g.vertex(3)
solver = Goldberg(g)
solution = solver.get_max_flow(source, target)
print("Il max flow trovato da Golberg è:", solution)

labels = g.new_vertex_property("string")
for vertex in g.vertices():
    labels[vertex] = str(g.vertex_index[vertex]) + "(" + str(g.vp.height[vertex]) + "," + str(
        g.vp.excess[vertex]) + ")"

gt.graph_draw(g, edge_pen_width=gt.prop_to_size(g.ep.residual, mi=1, ma=5, power=1),
              output="cf/max-flow-our-solution.pdf", vertex_text=labels, edge_text=g.ep.residual)

generator = Triangulation(50, type="delaunay", directed=True, seed_number=seed_number)
g, source, target = generator.generate()
cap = g.ep.cap
res = gt.push_relabel_max_flow(g, source, target, cap)
res.a = cap.a - res.a  # the actual flow
max_flow = sum(res[e] for e in target.in_edges())
print("Il max flow trovato da GraphTool è:", max_flow)

gt.graph_draw(g, edge_pen_width=gt.prop_to_size(res, mi=1, ma=5, power=1),
              output="cf/max-flow-library-solution.pdf", vertex_text=g.vertex_index, edge_text=res)


