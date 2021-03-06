import sys
sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
sys.path.append("/anaconda3/lib/python2.7/site-packages")

from io import StringIO
import cProfile, pstats
import graph_tool.all as gt
from numpy.random import seed, random, randint
from scipy.linalg import norm
from max_flow_residuals import Goldberg
import math
from generation.ScaleFree import ScaleFree
from generation.Triangulation import Triangulation
from generation.Random import Random

file = open("temporal_complexity_data_goldberg_4 edges for each vertex_10-90_nodes", "w")

for nodes in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
    for i in range(0, 35):
        #Goldberg version - using as graph generator Random
        seed_number = randint(1, 1000)
        generator = Random(nodes, nodes*4, directed=True, seed_number=seed_number)
        g, source, target = generator.generate()

        title = '- Parte grafo versione Goldberg con ' + str(nodes) + ' nodi e ' + str(len(g.get_edges())) + ' archi - Random.'
        print(title)
        file.write(title)
        solver = Goldberg(graph=g)

        pr = cProfile.Profile()
        pr.enable()
        solution = solver.get_max_flow(source, target)
        pr.disable()
        s = StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()

        file.write(s.getvalue())
file.close()