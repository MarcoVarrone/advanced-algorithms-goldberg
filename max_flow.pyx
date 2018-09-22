import graph_tool.all as gt
import math
from time import sleep


cdef class Goldberg:
    cdef graph, distance, excess, flow, capacity, source, sink
    cdef int n
    cdef set actives

    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.get_vertices())
        self.source = None
        self.sink = None

        self.distance = self.graph.new_vertex_property("double", 0)
        self.excess = self.graph.new_vertex_property("double", 0)
        self.flow = self.graph.new_edge_property("double", 0)
        self.capacity = self.graph.ep.cap

        self.actives = set()

    cpdef int get_max_flow(self, source, sink):
        # Initialization
        self.distance[source] = self.n
        self.source = source
        self.sink = sink
        source_edges = source.out_edges()

        for edge in source_edges:
            self.flow[edge] = self.capacity[edge]
            self.set_excess(edge.target(), self.capacity[edge])

        active = self.get_active_vertex()
        while active:
            if not self.push(active):
                self.relabel(active)
            active = self.get_active_vertex()

        max_flow = 0
        for e in sink.in_edges():
            max_flow += self.flow[e]
        return max_flow

    cdef bint push(self, vertex):
        success = False
        out_edges = vertex.out_edges()

        for edge in out_edges:
            if self.distance[vertex] != self.distance[edge.target()] + 1 or \
                    self.capacity[edge] == self.flow[edge]:
                continue
            success = True
            delta = min([
                self.excess[vertex],
                self.capacity[edge] - self.flow[edge]])
            self.send_flow(vertex, edge.target(), delta)
            # print("Pushing " + str(delta) + " from " + str(edge.source()) + " to " + str(edge.target()))
            if self.excess[vertex] == 0:
                break
        return success

    cdef relabel(self, vertex):
        self.distance[vertex] = self.get_min_distance(vertex) + 1
        # print("Relabeling " + str(vertex) + " to dist " + str(self.distance[vertex]))

    cdef int get_min_distance(self, vertex):
        min = float('inf')
        for e in vertex.out_edges():
            if self.flow[e] == self.capacity[e]:
                continue

            v = e.target()
            if self.distance[v] < min:
                min = self.distance[v]
        return min

    cdef send_flow(self, source, target, unsigned int delta):
        self.flow[self.graph.edge(source, target)] += delta
        self.flow[self.graph.edge(target, source)] -= delta
        self.set_excess(source, self.excess[source] - delta)
        self.set_excess(target, self.excess[target] + delta)

    cdef get_active_vertex(self):
        if len(self.actives) == 0:
            return False

        # Get an element from the set without popping it
        for v in self.actives:
            return v

    cdef set_excess(self, vertex, value):
        self.excess[vertex] = value
        if vertex == self.sink or vertex == self.source:
            return
        if value > 0:
            if vertex not in self.actives:
                self.actives.add(vertex)
        else:
            self.actives.discard(vertex)
