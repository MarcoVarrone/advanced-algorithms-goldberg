import graph_tool.all as gt
from numpy.random import seed, random, randint
from generation.Generator import Generator


class ScaleFree(Generator):
    def __init__(self, n, seed_number=None, directed=True):
        self.__validate(n, seed_number, directed)
        super().__init__(n, seed_number, directed)

    def __validate(self, n, seed_number, directed):
        super().validate(n, seed_number, directed)

    def generate(self):
        g = gt.price_network(self.n, directed=True)

        g = super().create_reverse_edges(g)

        # The capacity will be defined randomly
        capacity = g.new_edge_property("int")
        for e in g.edges():
            capacity[e] = randint(1, 15)

        g.ep.cap = capacity
        source = super().get_source(g)
        sink = super().get_sink(g)
        return g, source, sink
