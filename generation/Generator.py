from numpy.random import randint, seed
import graph_tool.all as gt
from numpy import unique
import random


class Generator:
    def __init__(self, n, seed_number=None, directed=False):
        self.n = n
        self.seed_number = seed_number
        self.directed = directed
        if seed_number:
            gt.seed_rng(self.seed_number)
            seed(self.seed_number)

    @staticmethod
    def validate(n, seed_number, directed):
        if not isinstance(n, int):
            raise ValueError("The number of nodes must be an integer.")
        if not isinstance(seed_number, int) and seed_number is not None:
            raise ValueError("The seed_number must be an integer")
        if not isinstance(directed, bool):
            raise ValueError("The directed variable must be a boolean")

    def create_reverse_edges(self, graph):
        edges = list(graph.edges())
        # reciprocate edges
        if not self.directed:
            for e in edges:
                if not graph.edge(e.target(), e.source()):
                    new_edge = graph.add_edge(e.target(), e.source())
        return graph

    def get_source(self, graph):
        # List the number of vertices without inbound edges (sources)
        sources = list()
        for vertex in graph.vertices():
            if vertex.in_degree() == 0:
                sources.append(vertex)

        # If there are not candidate sources
        # Create one and randomly attach to other vertices
        if len(sources) == 0:
            source = graph.add_vertex()
            self.n += 1
            n_edges = randint(1, self.n / 2)
            source_neighbors = randint(self.n, size=n_edges)
            source_neighbors = set(unique(source_neighbors))
            source_neighbors.discard(source)
            self.__connect_source(graph, source, source_neighbors)
        # If there are more than one candidate source
        # Pick a random one and attach to the other candidates
        elif len(sources) > 1:
            source = sources[randint(len(sources)-1)]
            sources.remove(source)
            self.__connect_source(graph, source, sources)
        else:
            source = sources[0]
        return source

    @staticmethod
    def __connect_source(graph, source, source_neighbors):
        for vertex in source_neighbors:
            edge = graph.add_edge(source, vertex)
            capacity = randint(1, 15)
            graph.ep.cap[edge] = capacity

    def get_sink(self, graph):
        # List the number of vertices without outbound edges (sinks)
        sinks = list()
        for vertex in graph.vertices():
            if vertex.out_degree() == 0:
                sinks.append(vertex)

        # If there are not candidate sinks
        # Create one and randomly attach to other vertices
        if len(sinks) == 0:
            sink = graph.add_vertex()
            self.n += 1
            n_edges = randint(1, self.n / 2)
            sink_neighbors = randint(self.n, size=n_edges)
            sink_neighbors = set(unique(sink_neighbors))
            sink_neighbors.discard(sink)
            self.__connect_sink(graph, sink, sink_neighbors)
        # If there are more than one candidate sink
        # Pick a random one and attach to the other candidates
        elif len(sinks) > 1:
            sink = sinks[randint(len(sinks)-1)]
            sinks.remove(sink)
            self.__connect_sink(graph, sink, sinks)
        else:
            sink = sinks[0]
        return sink


    @staticmethod
    def __connect_sink(graph, sink, sinks):
        for vertex in sinks:
            edge = graph.add_edge(vertex, sink)
            capacity = randint(1, 15)
            graph.ep.cap[edge] = capacity
