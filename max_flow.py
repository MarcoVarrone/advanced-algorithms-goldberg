import graph_tool.all as gt
import math
from time import sleep
from memory_profiler import profile

class Goldberg:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.get_vertices())

        self.distance = self.graph.new_vertex_property("double", 0)
        self.excess = self.graph.new_vertex_property("double", 0)
        self.flow = self.graph.new_edge_property("double", 0)
        self.capacity = self.graph.ep.cap

        self.graph.vp.distance = self.distance
        self.graph.vp.excess = self.excess
        self.graph.ep.flow = self.flow

    @profile(precision=5)
    def get_max_flow(self, source, sink):
        # Initialization
        self.distance[source] = self.n
        self.source = source
        source_edges = source.out_edges()

        for edge in source_edges:
            self.flow[edge] = self.capacity[edge]
            self.excess[edge.target()] = self.capacity[edge]

        active = self.get_active_vertex(sink)
        while active:
            if not self.push(active):
                self.relabel(active)
            active = self.get_active_vertex(sink)

        max_flow = 0
        for e in sink.in_edges():
            max_flow += self.flow[e]
        return max_flow

    def push(self, vertex):
        success = False
        out_edges = vertex.out_edges()

        for edge in out_edges:
            if self.distance[edge.source()] != self.distance[edge.target()] + 1 or \
                    self.capacity[edge] == self.flow[edge]:
                continue
            success = True
            delta = min([
                self.excess[vertex],
                self.capacity[edge] - self.flow[edge]])
            self.send_flow(edge.source(), edge.target(), delta)
            #print("Pushing " + str(delta) + " from " + str(edge.source()) + " to " + str(edge.target()))
            if self.excess[vertex] == 0:
                break
        return success

    def relabel(self, vertex):
        self.distance[vertex] = self.get_min_distance(vertex) + 1
        #print("Relabeling " + str(vertex) + " to dist " + str(self.distance[vertex]))

    def get_min_distance(self, vertex):
        min = float('inf')
        for e in vertex.out_edges():
            if self.flow[e] == self.capacity[e]:
                continue

            v = e.target()
            if self.distance[v] < min:
                min = self.distance[v]
        return min

    def send_flow(self, source, target, delta):
        self.flow[self.graph.edge(source, target)] += delta
        self.flow[self.graph.edge(target, source)] -= delta

        self.excess[source] -= delta
        self.excess[target] += delta

    def get_reverse_edge(self, edge):
        return self.graph.edge(edge.target(), edge.source())

    def get_active_vertex(self, sink):
        for v in self.graph.vertices():
            if self.excess[v] > 0 and v != sink and v != self.source:
                return v
        return False
