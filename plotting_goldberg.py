import matplotlib.pyplot as plt

DIFFERENT_NODES = 9
SAMPLES = 35

#plotting Goldberg implementation
file = open("temporal_complexity_data_goldberg_4 edges for each vertex_10-90_nodes", "r")
nodes = []
edges = []
seconds = []
result = []
file = file.read()

for i in range(0, DIFFERENT_NODES): 
    local_seconds = []
    first_iteration = True
    for sample in range(0, SAMPLES):

        #to find the nodes
        file = file[file.find(" con ") + len(" con "):]
        if first_iteration:
            nodes += [file[:3]]

        #to find the edges
        file = file[file.find(" e ") + len(" e "):]
        x = file[0:file.find(" archi")]
        if first_iteration:
            edges += [x]
            first_iteration = False

        file = file[file.find("in"):]
        local_seconds += [float(file[3:file.find(" sec")])]
    seconds += [sum(local_seconds) / float(len(local_seconds))]
    first_iteration = True

print(nodes)
print(edges)
print(seconds)

for i in range(0, DIFFERENT_NODES):
    result += [float(seconds[i]) / float(nodes[i]) ** 2 * float(edges[i])]

f = plt.figure()

f = plt.figure()
plt.xlabel('time')
plt.ylabel('time/O(V^2 * E)')
plt.title("Temporal complexity Goldberg implementation")
plt.plot(seconds, result)
plt.show()



#f.savefig("temporal_complexity_plot_4_edges_per_vertex.pdf", bbox_inches='tight')
