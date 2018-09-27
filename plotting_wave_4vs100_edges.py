import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DIFFERENT_NODES = 4
SAMPLES = 15

#plotting Goldberg implementation
file_100 = open("Complexity_data/temporal_complexity_data_wave_100 edges for each vertex", "r")
file = open("Complexity_data/temporal_complexity_data_wave_4 edges for each vertex", "r")

nodes = []
edges = []
seconds = []
seconds_100 = []
local_seconds = []
local_seconds_100 = []
file_100 = file_100.read()
file = file.read()

for i in range(0, DIFFERENT_NODES):
    local_seconds = []
    local_seconds_100 = []
    first_iteration = True
    for sample in range(0, SAMPLES):

        #to find the nodes
        file = file[file.find(" con ") + len(" con "):]
        file_100 = file_100[file_100.find(" con ") + len(" con "):]
        if first_iteration:
            nodes += [file[:3]]

        #to find the edges
        file = file[file.find(" e " ) + len(" e "):]
        file_100 = file_100[file_100.find(" e " ) + len(" e "):]
        x = file[0:file.find(" archi")]
        if first_iteration:
            edges += [x]
            first_iteration = False

        file = file[file.find("in"):]
        file_100 = file_100[file_100.find("in"):]
        local_seconds += [float(file[3:file.find(" sec")])]
        local_seconds_100 += [float(file_100[3:file_100.find((" sec"))])]
        #print(local_seconds_100)
        #print(local_seconds)
    seconds += [sum(local_seconds) / float(len(local_seconds))]
    seconds_100 += [sum(local_seconds_100) / float(len(local_seconds_100))]
    first_iteration = True

complexity = []
for i in range(0, DIFFERENT_NODES):
    complexity += [seconds_100[0]/float(nodes[0]) ** 3 * float(nodes[i]) ** 3]

print(nodes)
print(edges)
print(seconds)
print(seconds_100)

f = plt.figure()
plt.xlabel('graph size')
plt.ylabel('time')
plt.title("Temporal complexity Wave implementation")
red_patch = mpatches.Patch(color='red', label='4 edges per vertex')
blu_patch = mpatches.Patch(color='blue', label='100 edges per vertex')
green_patch = mpatches.Patch(color='green', label='Theoretical complexity')
plt.legend(handles=[green_patch, red_patch, blu_patch])
plt.plot(nodes, seconds, 'r')
plt.plot(nodes, seconds_100, 'b')
plt.plot(nodes, complexity, 'g')
plt.show()

#f.savefig("Complexity_graphs/temporal_complexity_wave_4 vs 10 edges_per_vertex.pdf", bbox_inches='tight')
