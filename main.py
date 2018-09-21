import graph_tool.all as gt
from numpy.random import seed, random, random_integers
from scipy.linalg import norm
from max_flow import Goldberg
import math

# Number of nodes
N = 50
# Number of edges
M = 200

'''def create_graph(N, M):
    g = Graph()
    g.set_directed(True)
    # Create a graph of
    g.add_vertex(N)
    # insert some random links
    for s, t in zip(randint(0, N, M), randint(0, N, M)):
        g.add_edge(g.vertex(s), g.vertex(t))

    capacity = g.new_edge_property("double")
    for e in g.edges():
        capacity[e] = min(1.0 / norm(pos[e.target()].a - pos[e.source()].a), 10)
    g.edge_properties["capacity"] = capacity
    return g'''


def create_graph1():
    gt.seed_rng(42)
    seed(42)
    points = random((M, 2))
    points[0] = [0, 0]
    points[1] = [1, 1]
    g, pos = gt.triangulation(points, type="simple")
    g.set_directed(True)
    edges = list(g.edges())
    # reciprocate edges
    for e in edges:
        g.add_edge(e.target(), e.source())

    # The capacity will be defined as the inverse euclidean distance
    capacity = g.new_edge_property("int")
    for e in g.edges():
        #print(min(math.ceil(1.0 / norm(pos[e.target()].a - pos[e.source()].a)), 10))
        capacity[e] = min(math.ceil(1.0 / norm(pos[e.target()].a - pos[e.source()].a)), 10)
    g.ep.cap = capacity
    g.vp.pos = pos
    g.save("flow-example2.xml.gz")
    gt.graph_draw(g, pos=pos, edge_pen_width=gt.prop_to_size(capacity, mi=0, ma=3, power=1),
                  output="flow-example2.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)

def create_graph2():
    gt.seed_rng(42)
    seed(42)
    g = gt.Graph(directed=True)
    for i in range(4):
        g.add_vertex()
    e1= g.add_edge(g.vertex(0), g.vertex(1))
    e2= g.add_edge(g.vertex(0), g.vertex(2))
    e3=g.add_edge(g.vertex(1), g.vertex(2))
    e4=g.add_edge(g.vertex(1), g.vertex(3))
    e5=g.add_edge(g.vertex(2), g.vertex(3))
    e6=g.add_edge(g.vertex(1), g.vertex(0))
    e7=g.add_edge(g.vertex(2), g.vertex(0))
    e8=g.add_edge(g.vertex(2), g.vertex(1))
    e9=g.add_edge(g.vertex(3), g.vertex(1))
    e10=g.add_edge(g.vertex(3), g.vertex(2))

    # The capacity will be defined as the inverse euclidean distance
    capacity = g.new_edge_property("int")
    capacity[e1] = 2
    capacity[e6] = 2
    capacity[e2] = 4
    capacity[e7] = 4
    capacity[e3] = 3
    capacity[e8] = 3
    capacity[e4] = 1
    capacity[e9] = 1
    capacity[e5] = 5
    capacity[e10] = 5
    g.ep.cap = capacity
    g.save("flow-example3.xml.gz")
    gt.graph_draw(g, edge_pen_width=gt.prop_to_size(capacity, mi=0, ma=3, power=1),
                  output="flow-example3.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)


create_graph1()
g = gt.load_graph("flow-example2.xml.gz")
cap = g.ep.cap
#for e in g.edges():
#    print(e)
#    print(g.ep.cap[e])
src, tgt = g.vertex(0), g.vertex(3)
solver = Goldberg(graph=g)
print(solver.get_max_flow(src, tgt))

res = gt.push_relabel_max_flow(g, src, tgt, cap)
res.a = cap.a - res.a  # the actual flow
max_flow = sum(res[e] for e in tgt.in_edges())
print(max_flow)