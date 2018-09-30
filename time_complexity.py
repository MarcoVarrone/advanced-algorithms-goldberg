import sys
sys.path.append("/usr/local/Cellar/graph-tool/2.27_1/lib/python3.7/site-packages")
sys.path.append("/anaconda3/lib/python2.7/site-packages")

import argparse
from io import StringIO
import cProfile, pstats
from numpy.random import randint
from max_flow_residuals import Goldberg
from max_flow_height import Goldberg as GoldbergHeight
from max_flow_wave import GoldbergWave
from generation.ScaleFree import ScaleFree
from generation.Triangulation import Triangulation
from generation.Random import Random
import datetime
import plotting


def main():
    args = parse_arguments()
    directed = args.directed
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d_%H-%M-%S")
    file = open("complexity_data/time_complexity_data_"+str(date)+".txt", "w")

    for idx, n in enumerate(args.nodes):
        for i in range(args.samples):
            seed_number = randint(1, 1000)
            generator = get_graph(args.graph, n, args.edges[idx], directed, seed_number)
            g, source, target = generator.generate()

            title = '- Time complexity: Goldberg '+str(args.algorithm)+' starts with '+str(args.graph)+' graph having ' + \
                    str(n) + ' nodes and ' + str(args.edges[idx]) + ' edges'
            print(title)
            file.write(title)
            solver = get_algorithm(args.algorithm, g)

            pr = cProfile.Profile()
            pr.enable()
            solver.get_max_flow(source, target)
            pr.disable()
            s = StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()

            file.write(s.getvalue())
    file.close()
    plotting.plot(len(args.nodes), args.samples, date, args.reduction)


def get_algorithm(algorithm, graph):
    if algorithm == 'generic':
        return Goldberg(graph)
    elif algorithm == 'height':
        return GoldbergHeight(graph)
    elif algorithm == 'wave':
        return GoldbergWave(graph)


def get_graph(graph_type, n, m, directed, seed_number):
    if graph_type == 'random':
        graph = Random(n, m, seed_number=seed_number, directed=directed)
    elif graph_type == 'scale-free':
        graph = ScaleFree(n, seed_number=seed_number, directed=directed)
    else:
        graph = Triangulation(n, type=graph_type, seed_number=seed_number, directed=directed)
    return graph


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--graph', type=str, choices=['random', 'scale-free', 'simple', 'delaunay'],
                        required=True)
    parser.add_argument('-n', '--nodes', type=int, required=True, nargs='+')
    parser.add_argument('-m', '--edges', type=int, nargs='+')
    parser.add_argument('-d', '--directed', dest='directed', action='store_true')
    parser.add_argument('-u', '--undirected', dest='directed', action='store_false')
    parser.add_argument('-a', '--algorithm', type=str, choices=['generic', 'wave'],
                        default='generic')
    parser.add_argument('-s', '--samples', type=int, required=True)
    parser.add_argument('-r', '--reduction', type=str, choices=['average', 'max'], default='average')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
