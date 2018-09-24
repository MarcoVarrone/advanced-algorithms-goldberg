from numpy.random import randint
from max_flow import Goldberg
import graph_tool.all as gt
from generation.Triangulation import Triangulation


def select_source_target(graph):
    n = len(graph.get_vertices())
    source = graph.vertex(randint(0, n - 1))
    target = None
    while target is None or source == target:
        target = graph.vertex(randint(0, n - 1))
    return source, target


def get_real_max_flow(graph, source, target):
    cap = graph.ep.cap
    res = gt.push_relabel_max_flow(graph, source, target, cap)
    res.a = cap.a - res.a  # the actual flow
    return sum(res[e] for e in target.in_edges())


# Tests
def test_max_flow_triangulation_simple_10():
    generator = Triangulation(10, type="simple")
    graph = generator.generate()
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_simple_25():
    generator = Triangulation(25, type="simple")
    graph = generator.generate()
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_simple_50():
    generator = Triangulation(50, type="simple")
    graph = generator.generate()
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_delaunay_10():
    generator = Triangulation(10, type="delaunay")
    graph = generator.generate()
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_delaunay_25():
    generator = Triangulation(25, type="delaunay")
    graph = generator.generate()
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)


def test_max_flow_triangulation_delaunay_50():
    generator = Triangulation(50, type="delaunay")
    graph = generator.generate()
    source, target = select_source_target(graph)
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    assert max_flow == get_real_max_flow(graph, source, target)
