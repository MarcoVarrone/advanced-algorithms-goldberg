#!/usr/bin/env python -W ignore::DeprecationWarning
from numpy.random import randint
from max_flow_residuals import Goldberg
import graph_tool.all as gt
from generation.Triangulation import Triangulation
import pytest

def get_real_max_flow(graph, source, target):
    cap = graph.ep.cap
    res = gt.push_relabel_max_flow(graph, source, target, cap)
    res.a = cap.a - res.a  # the actual flow
    return sum(res[e] for e in target.in_edges())

sizes = [10, 25, 50, 75, 100, 150]

@pytest.mark.parametrize('n', sizes)
def test_max_flow_triangulation_simple(n):
    seed_number = randint(1, 1000)
    generator = Triangulation(n, type="simple", directed=False, seed_number=seed_number)
    graph, source, target = generator.generate()
    solver = Goldberg(graph)
    max_flow = solver.get_max_flow(source, target)
    generator = Triangulation(n, type="simple", directed=False, seed_number=seed_number)
    graph, source, target = generator.generate()
    assert max_flow == get_real_max_flow(graph, source, target)

