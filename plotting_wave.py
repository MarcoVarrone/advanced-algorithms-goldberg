import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DIFFERENT_NODES = 4
SAMPLES = 15

#plotting Goldberg implementation
file = open("temporal_complexity_data_wave_4 edges for each vertex", "r")
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
    #average case
    #seconds += [sum(local_seconds) / float(len(local_seconds))]
    #max case
    seconds += [max(local_seconds)]
    first_iteration = True


print(nodes)
print(edges)
print(seconds)
complexity = []

for i in range(0, DIFFERENT_NODES):
    complexity += [seconds[0]/float(nodes[0]) ** 3 * float(nodes[i]) ** 3]

f = plt.figure()
plt.xlabel('graph size')
plt.ylabel('time')
plt.title("Temporal complexity Wave implementation")
red_patch = mpatches.Patch(color='red', label='Empirical')
blu_patch = mpatches.Patch(color='blue', label='Theoretical')
plt.legend(handles=[red_patch, blu_patch])
plt.plot(nodes, seconds, 'r')
plt.plot(nodes, complexity, 'b')
plt.show()


f.savefig("temporal_complexity_data_wave_max_case.pdf", bbox_inches='tight')
