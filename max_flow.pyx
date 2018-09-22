import graph_tool.all as gt
import math
from time import sleep
import numpy as np
cimport numpy as np

DTYPE = np.int

cdef class Goldberg:
    cdef graph, flow, capacity
    cdef np.ndarray distance, excess
    cdef np.int n, source, sink
    cdef set actives

    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.get_vertices())
        self.source = None
        self.sink = None

        self.distance = np.zeros(self.n, dtype=DTYPE)
        self.excess = np.zeros(self.n, dtype=DTYPE)
        self.flow = self.graph.new_edge_property("double", 0)
        self.capacity = self.graph.ep.cap

        self.actives = set()

    cpdef int get_max_flow(self, source, sink):
        # Initialization
        self.distance[source] = self.n
        self.source = source
        self.sink = sink
        source_edges = self.graph.vertex(source).out_edges()

        for edge in source_edges:
            self.flow[edge] = self.capacity[edge]
            self.set_excess(self.graph.vertex_index[edge.target()], self.capacity[edge])

        active_idx = self.get_active_vertex_idx()
        while active_idx is not False:
            if not self.push(active_idx):
                self.relabel(active_idx)
            active_idx = self.get_active_vertex_idx()

        max_flow = 0
        for e in self.graph.vertex(sink).in_edges():
            max_flow += self.flow[e]
        return max_flow

    cdef bint push(self, vertex_idx):
        success = False
        out_edges = self.graph.vertex(vertex_idx).out_edges()

        for edge in out_edges:
            if self.distance[vertex_idx] != self.distance[self.graph.vertex(edge.target())] + 1 or \
                    self.capacity[edge] == self.flow[edge]:
                continue
            success = True
            delta = min([
                self.excess[vertex_idx],
                self.capacity[edge] - self.flow[edge]])
            self.send_flow(vertex_idx, self.graph.vertex(edge.target()), delta)
            # print("Pushing " + str(delta) + " from " + str(edge.source()) + " to " + str(edge.target()))
            if self.excess[vertex_idx] == 0:
                break
        return success

    cdef relabel(self, vertex_idx):
        self.distance[vertex_idx] = self.get_min_distance(vertex_idx) + 1
        # print("Relabeling " + str(vertex) + " to dist " + str(self.distance[vertex]))

    cdef int get_min_distance(self, vertex_idx):
        min = float('inf')
        for e in self.graph.vertex(vertex_idx).out_edges():
            if self.flow[e] == self.capacity[e]:
                continue

            v = self.graph.vertex_index[e.target()]
            if self.distance[v] < min:
                min = self.distance[v]
        return min

    cdef send_flow(self, source_idx, target_idx, unsigned int delta):
        self.flow[self.graph.edge(source_idx, target_idx)] += delta
        self.flow[self.graph.edge(target_idx, source_idx)] -= delta
        self.set_excess(source_idx, self.excess[source_idx] - delta)
        self.set_excess(target_idx, self.excess[target_idx] + delta)

    cdef get_active_vertex_idx(self):
        if len(self.actives) == 0:
            return False

        # Get an element from the set without popping it
        for v in self.actives:
            return v

    cdef set_excess(self, vertex_idx, value):
        self.excess[vertex_idx] = value
        if vertex_idx == self.sink or vertex_idx == self.source:
            return
        if value > 0:
            if vertex_idx not in self.actives:
                self.actives.add(vertex_idx)
        else:
            self.actives.discard(vertex_idx)
