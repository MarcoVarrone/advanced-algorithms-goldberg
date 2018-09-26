import matplotlib.pyplot as plt

DIFFERENT_NODES = 4
SAMPLES = 15

#plotting Goldberg implementation
file = open("temporal_complexity_data_wave", "r")
nodes = []
edges = []
seconds = []
result = []
local_seconds = []
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
        file = file[file.find(" e " ) + len(" e "):]
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
    result += [float(seconds[i]) / float(nodes[i]) ** 3]

f = plt.figure()
plt.plot(seconds, result)
plt.show()

#f.savefig("temporal_complexity_plot.pdf", bbox_inches='tight')
