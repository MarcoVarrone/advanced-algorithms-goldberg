import matplotlib.pyplot as plt

DIFFERENT_NODES = 4
SAMPLES = 10

#plotting Goldberg implementation
file = open("temporal_complexity_data_goldberg", "r")
nodes = []
edges = []
seconds = []
result = []
local_seconds = []
for i in range(0, DIFFERENT_NODES):

    local_seconds = []
    first_iteration = True
    for sample in range(0, SAMPLES):
        first = file.readline()

        overhead = len("- Parte grafo versione Goldberg con ")
        if first_iteration:
            nodes += [first[overhead:overhead+3]]

        overhead = len("- Parte grafo versione Goldberg con 50 nodi e ")
        x = first[overhead:]
        x = x[1:x.find(" archi")]
        if first_iteration:
            edges += [x]
            first_iteration = False

        y = first[first.find("in"):]
        local_seconds += [float(y[3:y.find(" sec")])]
        for x in range(0, 19):
            file.readline()
    seconds += [sum(local_seconds) / float(len(local_seconds))]
    first_iteration = True


print(nodes)
print(edges)
print(seconds)

for i in range(0, DIFFERENT_NODES):
    result += [float(seconds[i]) / float(nodes[i]) ** 2 * float(edges[i])]

f = plt.figure()
plt.plot(seconds, result)
plt.show()

#f.savefig("temporal_complexity_plot.pdf", bbox_inches='tight')
