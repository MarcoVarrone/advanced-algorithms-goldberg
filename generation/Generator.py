from numpy.random import randint


class Generator:
    def __init__(self, n, seed=randint(1, 1000), directed=False):
        self.n = n
        self.seed = seed
        self.directed = directed

    @staticmethod
    def validate(n, seed, directed):
        if not isinstance(n, int):
            raise ValueError("The number of nodes must be an integer.")
        if not isinstance(seed, int):
            raise ValueError("The seed must be an integer")
        if not isinstance(directed, bool):
            raise ValueError("The directed variable must be a boolean")

    @staticmethod
    def create_reverse_edges(graph, directed):
        edges = list(graph.edges())
        temp_edges = list()
        # reciprocate edges
        for e in edges:
            if not graph.edge(e.target(), e.source()):
                new_edge = graph.add_edge(e.target(), e.source())
                if not directed:
                    temp_edges.append(new_edge)
        return graph, temp_edges
