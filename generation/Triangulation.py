import graph_tool.all as gt
from numpy.random import seed, random, randint
from generation.Generator import Generator
import math
from scipy.linalg import norm

class Triangulation(Generator):
    def __init__(self, n, seed_number=None, directed=False, type="simple"):
        print("Creating triangulation graph with seed number " + str(seed_number))
        self.__validate(n, seed_number, directed, type)
        super().__init__(n, seed_number, directed)
        self.type = type

    def __validate(self, n, seed_number, directed, type):
        super().validate(n, seed_number, directed)
        if type != "simple" and type != "delaunay":
            raise ValueError("Invalid triangulation type.")

    def generate(self):

        points = random((self.n, 2))
        points[0] = [0, 0]
        points[1] = [1, 1]
        g, pos = gt.triangulation(points, type=self.type)
        g.set_directed(True)
        g = super().create_reverse_edges(g)



        # The capacity will be defined as the inverse euclidean distance
        capacity = g.new_edge_property("int")

        for e in g.edges():
            capacity[e] = min(math.ceil(1.0 / norm(pos[e.target()].a - pos[e.source()].a)), 10)
        g.ep.cap = capacity
        source = super().get_source(g)
        sink = super().get_sink(g)
        g.vp.pos = pos
        return g, source, sink
