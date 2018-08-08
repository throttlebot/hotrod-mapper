import math
from shortest_path import *
from graph import *

def parent_square(x, y):
    fx = math.floor(x)
    fy = math.floor(y)
    return int(fy * 20 + fx)

def closest_node(x, y):
    ps = parent_square(x, y)
    g = download(ps)
    closest = []
    for n in g.nodes(data=True):
        z = n[1]["x"]
        w = n[1]["y"]
        d = dist(x, y, z, w)
        closest.append((n[0], d))
    closest = sorted(closest, key=lambda x: x[1])
    return g, closest[0][0]

def dist(x, y, z, w):
    return (x - z) ** 2 + (y - w) ** 2

def display(x, y, z, w):

    assert x >= 0
    assert y >= 0
    assert z >= 0
    assert w >= 0

    squares = []
    for y_axis in range(int(min(y, w)), int(math.ceil(max(y, w)))):
        for x_axis in range(int(min(x, z)), int(math.ceil(max(x, z)))):
            squares.append(parent_square(x_axis, y_axis))

    g = download_all(squares)
    return g


def route(x, y, z, w):
    g = display(x, y, z, w)
    start_sqaure, start_node = closest_node(x, y)
    end_square, end_node = closest_node(z, w)

    route_graph = nx.compose(start_sqaure, end_square)
    process_edges(route_graph)
    _, path = shortest_path(route_graph, start_node, end_node)
    g.add_path(path, color="blue")
    g.add_nodes_from(path, color="blue")
    return g

if __name__ == '__main__':
    draw_graph(route(10.2323, 15.3432, 19.61231, 19.2393), labels=False)