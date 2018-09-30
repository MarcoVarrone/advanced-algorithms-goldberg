from numpy.random import randint
import graph_tool.all as gt
from generation.Triangulation import Triangulation
from generation.ScaleFree import ScaleFree
from generation.Random import Random
import pytest


def has_unique_source(graph):
    count = 0
    source = None
    for vertex in graph.vertices():
        if vertex.in_degree() == 0:
            source = vertex
            count += 1
    print(count)
    return count == 1, source


def has_unique_sink(graph):
    count = 0
    sink = None
    for vertex in graph.vertices():
        if vertex.out_degree() == 0:
            sink = vertex
            count += 1
    print(count)
    return count == 1, sink


sizes = [10, 25, 50, 75, 100]
sizes_random = [(10, 50), (25, 150), (50, 300), (75, 100), (100, 500)]


@pytest.mark.parametrize('n', sizes)
def test_source_sink_triangulation_simple(n):
    seed_number = randint(1, 1000)
    generator = Triangulation(n, type="simple", directed=True, seed_number=seed_number)
    graph, source, sink = generator.generate()
    count_source, src = has_unique_source(graph)
    count_sink, snk = has_unique_sink(graph)
    assert count_source == 1
    assert count_sink == 1
    assert source == src
    assert sink == snk


@pytest.mark.parametrize('n', sizes)
def test_source_sink_triangulation_delaunay(n):
    seed_number = randint(1, 1000)
    generator = Triangulation(n, type="delaunay", directed=True, seed_number=seed_number)
    graph, source, sink = generator.generate()
    count_source, src = has_unique_source(graph)
    count_sink, snk = has_unique_sink(graph)
    assert count_source == 1
    assert count_sink == 1
    assert source == src
    assert sink == snk

@pytest.mark.parametrize('n', sizes)
def test_source_sink_scale_free(n):
    seed_number = randint(1, 1000)
    generator = ScaleFree(n, directed=True, seed_number=seed_number)
    graph, source, sink = generator.generate()
    count_source, src = has_unique_source(graph)
    count_sink, snk = has_unique_sink(graph)
    assert count_source == 1
    assert count_sink == 1
    assert source == src
    assert sink == snk

@pytest.mark.parametrize('size', sizes_random)
def test_source_sink_random(size):
    seed_number = randint(1, 1000)
    generator = Random(size[0], size[1], directed=True, seed_number=seed_number)
    graph, source, sink = generator.generate()
    count_source, src = has_unique_source(graph)
    count_sink, snk = has_unique_sink(graph)
    assert count_source == 1
    assert count_sink == 1
    assert source == src
    assert sink == snk
