import graph_tool.all as gt
import math
from time import sleep

class WaveImplementation:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.get_vertices())
        self.source = None
        self.sink = None

        self.distance = self.graph.new_vertex_property("int", 0)
        self.excess = self.graph.new_vertex_property("int", 0)
        self.flow = self.graph.new_edge_property("int", 0)
        self.capacity = self.graph.ep.cap

        self.graph.vp.distance = self.distance
        self.graph.vp.excess = self.excess
        self.graph.ep.flow = self.flow

        #list containing all vertices
        self.l = []
        #used when there will be a discharging of a vertex
        self.neighbors = self.graph.new_vertex_property("object")
        #the current vertex taken from neighbours for discharging
        self.current = self.graph.new_vertex_property("object")

        #foreach vertex -> insert his neighbours in the list property neighbours
        for v in self.graph.get_vertices():
            self.neighbors[v] = []
            for neighbour in self.graph.vertex(v).out_neighbors():
                self.neighbors[v] += [neighbour]


    def get_max_flow(self, source, sink):
        self.init(source, sink)

        # pop from l the first vertex to process
        vertex = self.l.pop(0)
        while vertex is not None:
            old_height = self.distance[vertex]
            self.discharge(vertex)
            #if discharge has changed the height of vertex, push in l
            if self.distance[vertex] > old_height:
                self.l += [vertex]

            if len(self.l) > 0:
                vertex = self.l.pop(0)
            else:
                vertex = None

        #algorithm terminated
        max_flow = 0
        for e in sink.in_edges():
            max_flow += self.flow[e]
        return max_flow

    def init(self, source, sink):
        self.distance[source] = self.n
        self.source = source
        self.sink = sink

        # l initially contains all vertices except source and target
        for vertex in self.graph.get_vertices():
            if self.graph.vertex(vertex) != source and self.graph.vertex(vertex) != sink:
                self.l += [vertex]
                # current vertex is the first in the neighbors list
                self.current[vertex] = self.neighbors[vertex][0]

        source_edges = source.out_edges()
        for edge in source_edges:
            self.flow[edge] = self.capacity[edge]
            self.set_excess(edge.target(), self.capacity[edge])

    def discharge(self, vertex):
        #while the vertex is an overflowing vertex
        v = self.current[vertex]
        while self.excess[vertex] > 0:
            print("Il vertice " + str(vertex) + " ha eccesso " + str(self.excess[vertex]) + " con distanza " + str(self.distance[vertex]))
            if v is None:
                print("Non avendo più vicini, procedo al relabeling")
                self.relabel(vertex)
                for neighbour in self.graph.vertex(vertex).out_neighbors():
                    self.neighbors[vertex] += [neighbour]
                v = self.neighbors[vertex].pop(0)
            elif self.distance[vertex] == self.distance[v] + 1 and self.capacity[self.graph.edge(vertex, v)] - self.flow[self.graph.edge(vertex, v)] > 0:
                print("Pusho da " + str(vertex) + " a " + str(v))
                self.push(vertex, v)
            else:
                #if there are other neighbors, check them
                if(len(self.neighbors[vertex]) > 0):
                    print("Il vertice corrente ha altri vicini, prendo il prossimo!")
                    v = self.neighbors[vertex].pop(0)
                else:
                    print("Non ci sono più vicini!")
                    v = None

    def push(self, source, target):
        delta = min([
                self.excess[source],
                self.capacity[self.graph.edge(source, target)] - self.flow[self.graph.edge(source, target)]])

        self.send_flow(source, target, delta)

    def relabel(self, vertex):
        self.distance[vertex] = self.get_min_distance(vertex) + 1
        print("Il vertice " + str(vertex) + " ora ha distanza " + str(self.distance[vertex]))

    def get_min_distance(self, vertex):
        min = float('inf')
        for e in self.graph.vertex(vertex).out_edges():
            v = e.target()
            if self.distance[v] < min:
                min = self.distance[v]
        return min

    def send_flow(self, source, target, delta):
        self.flow[self.graph.edge(source, target)] += delta
        #self.flow[self.graph.edge(target, source)] -= delta
        self.set_excess(source, self.excess[source] - delta)
        self.set_excess(target, self.excess[target] + delta)

    def set_excess(self, vertex, value):
        self.excess[vertex] = value