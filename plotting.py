import matplotlib.pyplot as plt


#plotting Goldberg implementation
file = open("temporal_complexity_data", "r")
nodes = []
edges = []
seconds = []
result = []
for i in range(0, 9):
    for sample in range(0, 10):
        first = file.readline()

        overhead = len("- Parte grafo versione Goldberg con ")
        nodes += [first[overhead:overhead+3]]

        overhead = len("- Parte grafo versione Goldberg con 50 nodi e ")
        x = first[overhead:]
        x = x[1:x.find(" archi")]
        edges += [x]

        y = first[first.find("in"):]
        seconds += [y[3:y.find(" sec")]]
        for x in range(0, 19):
            file.readline()

print(nodes)
print(edges)
print(seconds)

for i in range(0, 9):
    result += [float(seconds[i]) / float(nodes[i]) ** 2 * float(edges[i])]

f = plt.figure()
plt.plot(seconds, result)
plt.show()

#f.savefig("temporal_complexity_plot.pdf", bbox_inches='tight')

