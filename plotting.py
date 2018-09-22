import matplotlib.pyplot as plt

#on the x-axis, the time
x = [0.859, 3.472, 10.090, 16.498, 23.797, 35.260, 48.148, 64.775, 82.773, 103.826, 124.087, 147.381, 166.432, 184.415, 222.458, 267.618, 421.140]
#on the y-axis t/O(N^2 * M) where N and M are respectively the nodes and the edges of the considered grapgh
y = [50^2 * 276, 100^2 * 578, 150^2 * 874, 200^2 * 1172, 250^2 * 1472, 300^2 * 1774, 350^2 * 2074, 400^2 * 2374, 450^2 * 2672, 500^2 * 2972, 550^2 * 3272, 600^2 * 3570, 650^2 * 3870, 700^2 * 4172, 750^2 * 4474, 800^2 * 4772, 1000^2 * 5970]

for i in range(0, len(x)):
    y[i] = x[i] / y[i]


f = plt.figure()
plt.plot(x, y)
plt.show()

f.savefig("temporal_complexity_plot.pdf", bbox_inches='tight')