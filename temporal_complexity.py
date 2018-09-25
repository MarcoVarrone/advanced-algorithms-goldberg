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

file = open("temporal_complexity_data", "w")

for nodes in [150, 100 ,250, 300 ,350, 400 ,450, 500,550]:
    for i in range(0, 10):
        #Goldberg version - using as graph generator Triangulation
        seed_number = randint(1, 1000)
        generator = Triangulation(nodes, type="delaunay", directed=True, seed_number=seed_number)
        g, source, target = generator.generate()

        title = '- Parte grafo versione Goldberg con ' + str(nodes) + ' nodi e ' + str(len(g.get_edges())) + ' archi - Triangulation.'
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

        '''
        # Goldberg version - using as graph generator ScaleFree
        seed_number = randint(1, 1000)
        generator = ScaleFree(nodes, directed=True, seed_number=seed_number)
        g, source, target = generator.generate()
    
        title = '- Parte grafo versione Goldberg con ' + str(nodes) + ' nodi e ' + str(len(g.get_edges())) + ' archi - ScaleFree.'
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
        '''
file.close()

