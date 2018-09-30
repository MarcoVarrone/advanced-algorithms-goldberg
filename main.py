import argparse
from generation.Triangulation import Triangulation
from generation.Random import Random
from generation.ScaleFree import ScaleFree
import graph_tool.all as gt
from max_flow_residuals import Goldberg
from max_flow_height import Goldberg as GoldbergHeight
from max_flow_wave import GoldbergWave
from numpy.random import randint


def main():
    args = parse_arguments()
    n = args.nodes
    m = args.edges
    seed_number = args.seed
    if seed_number is None:
        seed_number = randint(1000)
    directed = args.directed
    generator = get_graph(args.graph, n, m, directed, seed_number)
    g, source, target = generator.generate()

    print("Source " + str(source) + " Target " + str(target))
    gt.graph_draw(g, edge_pen_width=g.ep.cap,
                  output="graph_initial.pdf", vertex_text=g.vertex_index, edge_text=g.ep.cap)

    solver = get_algorithm(args.algorithm, g)
    solution = solver.get_max_flow(source, target)
    print("The maximum flow is " + str(solution))

    if args.compare:
        generator = get_graph(args.graph, n, m, directed, seed_number)
        g, source, target = generator.generate()
        cap = g.ep.cap
        res = gt.push_relabel_max_flow(g, source, target, cap)
        res.a = cap.a - res.a  # the actual flow
        max_flow = sum(res[e] for e in target.in_edges())

        print("The maximum flow of graph-tool is " + str(max_flow))

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
    parser.add_argument('-n', '--nodes', type=int, required=True)
    parser.add_argument('-m', '--edges', type=int)
    parser.add_argument('-s', '--seed', type=int)
    parser.add_argument('-d', '--directed', dest='directed', action='store_true')
    parser.add_argument('-u', '--undirected', dest='directed', action='store_false')
    parser.add_argument('-a', '--algorithm', type=str, choices=['generic', 'height', 'wave'],
                        default='generic')
    parser.add_argument('-c', '--compare', dest='compare', action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
