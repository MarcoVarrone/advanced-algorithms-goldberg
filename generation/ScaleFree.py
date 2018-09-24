import graph_tool.all as gt
from numpy.random import seed, random, randint
from generation.Generator import Generator


class ScaleFree(Generator):
    def __init__(self, n, seed=randint(1, 1000), directed=True):
        super().__init__(n, seed, directed)
        self.__validate(n, seed, directed)

    def __validate(self, n, seed, directed):
        super().validate(n, seed, directed)

    def generate(self):
        gt.seed_rng(self.seed)
        seed(self.seed)
        g = gt.price_network(self.n, directed=True)

        if not self.directed:
            g = super().set_undirected(g)

        # The capacity will be defined randomly
        capacity = g.new_edge_property("int")
        for e in g.edges():
            capacity[e] = randint(1, 10)
        g.ep.cap = capacity
        gt.graph_draw(g, edge_pen_width=gt.prop_to_size(capacity, mi=1, ma=1, power=1),
                      output="graph_scale_free.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)
        return g
