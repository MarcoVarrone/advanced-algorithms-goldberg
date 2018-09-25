import graph_tool.all as gt
import math
from time import sleep
from memory_profiler import profile


class Goldberg:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.get_vertices())
        self.source = None
        self.sink = None

        self.height = self.graph.new_vertex_property("int", 0)
        self.excess = self.graph.new_vertex_property("int", 0)
        self.res = self.graph.new_edge_property("int", 0)
        self.real = self.graph.new_edge_property("bool", True)
        self.capacity = self.graph.ep.cap

        self.graph.vp.height = self.height
        self.graph.vp.excess = self.excess
        self.actives = set()

        self.i = 0

    def get_max_flow(self, source, sink):
        self.source = source
        self.sink = sink
        self.init(source)
        #self.__print_residuals()

        active = self.get_active_vertex()
        while active:
            if not self.push(active):
                self.relabel(active)
            active = self.get_active_vertex()

        return self.excess[sink]

    def __print_residuals(self):
        labels = self.graph.new_vertex_property("string")
        for vertex in self.graph.vertices():
            labels[vertex] = str(self.graph.vertex_index[vertex]) + "(" + str(self.height[vertex]) + "," + str(
                self.excess[vertex]) + ")"

        gt.graph_draw(self.graph, edge_pen_width=gt.prop_to_size(self.res, mi=1, ma=5, power=1),
                      output="cf/cf_residuals" + str(self.i) + ".pdf", vertex_text=labels, edge_text=self.res)
        print("Print graph "+str(self.i))
        self.i += 1

    def push(self, vertex):
        success = False
        #print("Chosen vertex:" + str(vertex))
        for edge in list(vertex.out_edges()):
            #print("Edge:"+str(edge))
            if self.height[edge.source()] != self.height[edge.target()] + 1:
                continue

            success = True
            delta = min(self.excess[vertex], self.res[edge])
            self.send_flow(vertex, edge.target(), delta)
            #print("Pushing "+str(delta)+" along "+str(edge))
            #self.__print_residuals()

            if self.excess[vertex] == 0:
                break
        return success

    def relabel(self, vertex):
        self.height[vertex] = self.get_min_distance(vertex) + 1
        #print("Relabeling vertex " + str(vertex) + " to distance " + str(self.height[vertex]))
        #self.__print_residuals()

    def get_min_distance(self, vertex):
        min_h = float('inf')
        for edge in vertex.out_edges():
            if self.height[edge.target()] < min_h:
                min_h = self.height[edge.target()]
        return min_h

    def send_flow(self, source, target, value):
        edge = self.graph.edge(source, target)
        real = self.real[edge]
        reverse_edge = None
        for e in self.graph.edge(target, source, all_edges=True):
            if self.real[e] != real:
                reverse_edge = e

        self.increase_res(self.graph.edge(source, target), -value)
        if not reverse_edge:
            reverse_edge = self.graph.add_edge(target, source)
            self.real[reverse_edge] = not real
        self.increase_res(reverse_edge, value)
        self.set_excess(target, self.excess[target] + value)
        self.set_excess(source, self.excess[source] - value)

    def increase_res(self, edge, value):
        self.res[edge] += value
        if self.res[edge] <= 0:
            #print("Deleted edge " + str(edge))
            self.graph.remove_edge(edge)

    def init(self, source):
        self.height[source] = self.n
        for edge in self.graph.edges():
            self.res[edge] = self.capacity[edge]

        for edge in list(source.out_edges()):
            #print("Send flow edge: " + str(edge))
            self.send_flow(edge.source(), edge.target(), self.capacity[edge])

    def get_active_vertex(self):
        if len(self.actives) == 0:
            return False

        # Get an element from the set without popping it
        for v in self.actives:
            return v

    def set_excess(self, vertex, value):

        self.excess[vertex] = value
        if vertex == self.sink or vertex == self.source:
            return
        if value > 0:
            if vertex not in self.actives:
                self.actives.add(vertex)
        else:
            self.actives.discard(vertex)

