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
        self.i = 0

        self.distance = self.graph.new_vertex_property("int", 0)
        self.excess = self.graph.new_vertex_property("int", 0)
        self.flow = self.graph.new_edge_property("int", 0)
        self.capacity = self.graph.ep.cap
        self.labels = self.graph.new_edge_property("string", "")

        self.graph.vp.distance = self.distance
        self.graph.vp.excess = self.excess
        self.graph.ep.flow = self.flow
        self.actives = set()
        self.temp_edges = list()

    def get_max_flow(self, source, sink):
        # Initialization
        self.distance[source] = self.n
        self.source = source
        self.sink = sink
        source_edges = source.out_edges()

        i = 0
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

    def push(self, vertex):
        #sleep(1)
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
            print("Pushing " + str(delta) + " from " + str(edge.source()) + " to " + str(edge.target()))
            print("----- Capacities edge: "+str(self.capacity[edge]))
            print("----- Flow "+str(self.flow[edge]))
            print("----- Excess source: "+str(self.excess[vertex])+ " target: "+str(self.excess[edge.target()]))
            for e in self.graph.edges():
                self.labels[e] = str(self.flow[e]) + "/" + str(self.capacity[e])
            #gt.graph_draw(self.graph, edge_pen_width=gt.prop_to_size(self.labels, mi=1, ma=1, power=1),
            #              output="graph_iteration"+str(self.i)+".pdf", vertex_text=self.graph.vertex_index, edge_text=self.labels)
            print("Print graph "+str(self.i))
            self.i += 1
            if self.excess[vertex] == 0:
                break
        return success

    def relabel(self, vertex):
        #sleep(1)
        min_dist = self.get_min_distance(vertex)
        if min_dist is not False:
            self.distance[vertex] = self.get_min_distance(vertex) + 1
        else:
            self.actives.discard(vertex)
        print("Relabeling " + str(vertex) + " to dist " + str(self.distance[vertex]))

    def get_min_distance(self, vertex):
        print("Sto calcolando la minima distanza di " + str(vertex) + " con eccesso " + str(self.excess[vertex]))
        min = float('inf')
        for e in vertex.out_edges():
            print(str(e) + " ha flow " + str(self.flow[e]) + " e capacità " + str(self.capacity[e]))
            if self.flow[e] == self.capacity[e]:
                continue

            v = e.target()
            if self.distance[v] < min:
                min = self.distance[v]
        if min == float('inf'):
            min = False
        return min

    def send_flow(self, source, target, delta):
        edge = self.graph.edge(source, target)
        if edge not in self.temp_edges:
            self.flow[self.graph.edge(source, target)] += delta
            reverse_edge = self.graph.edge(target, source)
            if not reverse_edge:
                reverse_edge = self.graph.add_edge(target, source)
                self.temp_edges.append(reverse_edge)
            self.capacity[reverse_edge] = self.capacity[self.graph.edge(source, target)]
        else:
            self.flow[self.graph.edge(source, target)] -= delta
        #reverse_edge = self.graph.edge(target, source, add_missing=True)

        #self.flow[reverse_edge] -= delta
        #self.flow[self.graph.edge(target, source)] -= delta
        self.set_excess(source, self.excess[source] - delta)
        self.set_excess(target, self.excess[target] + delta)

    def get_reverse_edge(self, edge):
        return self.graph.edge(edge.target(), edge.source())

    def get_active_vertex(self):
        if len(self.actives) == 0:
            return False

        return next(iter(self.actives))

    def set_excess(self, vertex, value):
        self.excess[vertex] = value
        if vertex == self.sink or vertex == self.source:
            return
        if value > 0 and vertex.out_degree() > 0:
            if vertex not in self.actives:
                self.actives.add(vertex)
        else:
            self.actives.discard(vertex)

    #getter in order to print in main.py the graph
    def get_flow(self):
        return self.flow
