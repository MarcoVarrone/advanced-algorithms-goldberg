from numpy.random import seed, random, randint
from max_flow import Goldberg
import graph_tool.all as gt
import math
from scipy.linalg import norm


def create_graph_triangulation(m, seed_number=42, type="simple"):
    if type not in ("simple", "delaunay"):
        return
    gt.seed_rng(seed_number)
    seed(seed_number)
    points = random((m, 2))
    points[0] = [0, 0]
    points[1] = [1, 1]
    g, pos = gt.triangulation(points, type=type)
    g.set_directed(True)
    edges = list(g.edges())
    # reciprocate edges
    for e in edges:
        g.add_edge(e.target(), e.source())

    # The capacity will be defined as the inverse euclidean distance
    capacity = g.new_edge_property("int")
    for e in g.edges():
        capacity[e] = min(math.ceil(1.0 / norm(pos[e.target()].a - pos[e.source()].a)), 10)
    g.ep.cap = capacity
    g.vp.pos = pos
    return g


def select_source_target(graph):
    n = len(graph.get_vertices())
    source = randint(0, n - 1)
    target = None
    while target is None or source == target:
        target = randint(0, n - 1)
    return source, target


def get_real_max_flow(graph, source_idx, target_idx):
    cap = graph.ep.cap
    source = graph.vertex(source_idx)
    target = graph.vertex(target_idx)
    res = gt.push_relabel_max_flow(graph, source, target, cap)
    res.a = cap.a - res.a  # the actual flow
    return sum(res[e] for e in target.in_edges())


# Tests
def test_max_flow_triangulation_simple_10():
    graph = create_graph_triangulation(10, seed_number=randint(0, 1000), type="simple")
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_simple_25():
    graph = create_graph_triangulation(25, seed_number=randint(0, 1000), type="simple")
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_simple_50():
    graph = create_graph_triangulation(50, seed_number=randint(0, 1000), type="simple")
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_delaunay_10():
    graph = create_graph_triangulation(10, seed_number=randint(0, 1000), type="delaunay")
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_delaunay_25():
    graph = create_graph_triangulation(25, seed_number=randint(0, 1000), type="delaunay")
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_delaunay_50():
    graph = create_graph_triangulation(50, seed_number=randint(0, 1000), type="delaunay")
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)
