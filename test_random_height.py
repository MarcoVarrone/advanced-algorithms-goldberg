from numpy.random import randint
from max_flow_height import GoldbergWave
import graph_tool.all as gt
from generation.Random import Random
import pytest


def get_real_max_flow(graph, source, target):
    cap = graph.ep.cap
    res = gt.push_relabel_max_flow(graph, source, target, cap)
    res.a = cap.a - res.a  # the actual flow
    return sum(res[e] for e in target.in_edges())


sizes = [(10, 50), (25, 150), (50, 300), (75, 100), (100, 500)]


@pytest.mark.parametrize('size', sizes)
def test_max_flow_scale_random_undirected(size):
    seed_number = randint(1, 1000)
    generator = Random(size[0], size[1], directed=False, seed_number=seed_number)
    graph, source, target = generator.generate()
    solver = GoldbergWave(graph)
    max_flow = solver.get_max_flow(source, target)

    generator = Random(size[0], size[1], directed=False, seed_number=seed_number)
    graph, source, target = generator.generate()
    res = gt.push_relabel_max_flow(graph, source, target, graph.ep.cap)
    res.a = graph.ep.cap.a - res.a  # the actual flow
    gt_max_flow = sum(res[e] for e in target.in_edges())
    assert max_flow == gt_max_flow


@pytest.mark.parametrize('size', sizes)
def test_max_flow_random_directed(size):
    seed_number = randint(1, 1000)
    generator = Random(size[0], size[1], directed=True, seed_number=seed_number)
    graph, source, target = generator.generate()
    solver = GoldbergWave(graph)
    max_flow = solver.get_max_flow(source, target)

    generator = Random(size[0], size[1], directed=True, seed_number=seed_number)
    graph, source, target = generator.generate()
    res = gt.push_relabel_max_flow(graph, source, target, graph.ep.cap)
    res.a = graph.ep.cap.a - res.a  # the actual flow
    gt_max_flow = sum(res[e] for e in target.in_edges())
    assert max_flow == gt_max_flow
