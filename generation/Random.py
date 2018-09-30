import graph_tool.all as gt
from numpy.random import seed, randint
from generation.Generator import Generator


class Random(Generator):
    def __init__(self, n, m, seed_number=None, directed=True):
        self.__validate(n, m, seed_number, directed)
        super().__init__(n, seed_number, directed)
        self.m = m

    def __validate(self, n, m, seed_number, directed):
        super().validate(n, seed_number, directed)
        if not isinstance(m, int):
            raise ValueError("The number of edges must be an integer.")

    def restore_number_edges(self, graph, source, sink, capacity):
        while len(graph.get_edges()) < self.m:
            s = randint(0, self.n)
            t = randint(0, self.n)
            if s == t or s == sink or t == source:
                continue
            if graph.edge(s, t):
                continue

            edge = graph.add_edge(s, t)
            # The capacity will be defined randomly
            cap = randint(1, 15)
            capacity[edge] = cap
            if not self.directed:
                reverse_edge = graph.edge(t, s, add_missing=True)
                capacity[reverse_edge] = cap

        while len(graph.get_edges()) > self.m:
            e = randint(0, len(graph.get_edges()))
            edge = gt.find_edge(graph, graph.edge_index, e)
            if not edge:
                continue
            edge = edge[0]
            s = edge.source()
            t = edge.target()
            if s == t or s == source or t == sink:
                continue

            if edge:
                graph.remove_edge(edge)

                if not self.directed:
                    graph.remove_edge(graph.edge(t, s))

        return graph

    def generate(self):
        g = gt.Graph()
        g.add_vertex(self.n)
        capacity = g.new_edge_property("int")
        g.ep.cap = capacity
        # insert some random links
        for s, t in zip(randint(0, self.n, self.m), randint(0, self.n, self.m)):
            if s == t:
                continue
            if g.edge(s, t):
                continue
            edge = g.add_edge(s, t)

            # The capacity will be defined randomly
            cap = randint(1, 15)
            capacity[edge] = cap
            if not self.directed:
                reverse_edge = g.edge(t, s, add_missing=True)
                capacity[reverse_edge] = cap

        source = super().get_source(g)
        sink = super().get_sink(g)

        return g, source, sink
