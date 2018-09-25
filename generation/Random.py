import graph_tool.all as gt
from numpy.random import seed, random, randint
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

    @staticmethod
    def select_source_target(graph):
        n = len(graph.get_vertices())
        source = graph.vertex(randint(0, n - 1))
        target = None
        while target is None or source == target:
            target = graph.vertex(randint(0, n - 1))
        return source, target

    def generate(self):
        g = gt.Graph()
        g.add_vertex(self.n)
        capacity = g.new_edge_property("int")
        # insert some random links
        for s, t in zip(randint(0, self.n, self.m), randint(0, self.n, self.m)):
            if s == t:
                continue
            if g.edge(s, t):
                continue
            edge = g.add_edge(s, t)
            reverse_edge = g.edge(t, s, add_missing=True)

            # The capacity will be defined randomly
            cap = randint(1, 15)
            capacity[edge] = cap
            capacity[reverse_edge] = cap

        source, sink = self.select_source_target(g)
        g.ep.cap = capacity
        return g, source, sink
