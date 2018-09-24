import graph_tool.all as gt
from numpy.random import seed, random, randint
from generation.Generator import Generator
import math
from scipy.linalg import norm


class Triangulation(Generator):
    def __init__(self, n, seed=randint(1, 1000), directed=False, type="simple"):
        super().__init__(n, seed, directed)
        self.__validate(n, seed, directed, type)
        self.type = type

    def __validate(self, n, seed, directed, type):
        super().validate(n, seed, directed)
        if type != "simple" and type != "delaunay":
            raise ValueError("Invalid triangulation type.")

    def generate(self):
        temp_edges = list()
        gt.seed_rng(self.seed)
        seed(self.seed)
        points = random((self.n, 2))
        points[0] = [0, 0]
        points[1] = [1, 1]
        g, pos = gt.triangulation(points, type=self.type)
        g.set_directed(True)
        g, temp_edges = super().create_reverse_edges(g, self.directed)

        # The capacity will be defined as the inverse euclidean distance
        capacity = g.new_edge_property("int")
        for e in g.edges():
            capacity[e] = min(math.ceil(1.0 / norm(pos[e.target()].a - pos[e.source()].a)), 10)
        g.ep.cap = capacity
        g.vp.pos = pos
        return g, temp_edges
