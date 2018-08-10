import networkx as nx
import random, json
from shortest_path import *
from multiprocessing import Pool
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def new_square(id, size=100):
    G = nx.Graph()

    # create nodes
    base = id * size * size
    for x in range(0, size, 1):
        for y in range(0, size, 1):
            xrand = (random.random() - 0.5) * 0.5
            yrand = (random.random() - 0.5) * 0.5
            G.add_node(base, x=0.1*(x + 0), y=0.1*(y + 0), level=1)
            base += 1

    # create edges
    for n_id, data in G.nodes(data=True):
        if (n_id + 1) % size != 0 and n_id + 1 < (id + 1) * size * size:
            G.add_edge(n_id, n_id + 1, weight=1)
        if n_id + size < (id + 1) * size * size:
            G.add_edge(n_id, n_id + size, weight=1)

    return G

def congest(G, size=100):
    # populate congestion
    congestion_points = range(size*size)
    random.shuffle(congestion_points)
    congestion_points = congestion_points[:20]
    for cp in congestion_points:
        G.add_node(cp, level=3)
    new_congestions = []

    while len(congestion_points) > 0:
        cp = congestion_points.pop()
        for n in G.neighbors(cp):
            if G.node[n]["level"] == 1:
                if random.random() < 0.57:
                    G.add_node(n, level=3)
                    congestion_points.append(n)
                else:
                    G.add_node(n, level=2)
                    new_congestions.append(n)

    while len(new_congestions) > 0:
        cp = new_congestions.pop()
        for n in G.neighbors(cp):
            if G.node[n]["level"] == 1:
                if random.random() < 0.47:
                    G.add_node(n, level=2)
                    new_congestions.append(n)

    for e in G.edges(data=True):
        if G.node[e[0]]["level"] == 3 or G.node[e[1]]["level"] == 3:
            G.add_edge(e[0], e[1], weight=3)
        elif G.node[e[0]]["level"] == 2 or G.node[e[1]]["level"] == 2:
            G.add_edge(e[0], e[1], weight=2)
        else:
            G.add_edge(e[0], e[1], weight=1)

    return G

def color_by_level(level):
    if level == 3:
        return "red"
    elif level == 2:
        return "orange"
    elif level == 1:
        return "yellow"
    else:
        exit(1)

def color_shortest(g):
    assert len(g.nodes) > 1
    path = shortest_path(g, list(g.nodes().keys())[0], list(g.nodes().keys())[-1])
    g.add_path(path, color="blue")
    g.add_nodes_from(path, color="blue")

def color_shortest_test():
    s1 = random.randrange(0, 400)
    s2 = random.randrange(0, 400)

    g1 = download(s1)
    g2 = download(s2)
    g = download_and_merge(g1, s2)

    start = random.choice([n for n in g1.nodes()])
    end = random.choice([n for n in g2.nodes()])

    g = download_and_merge(download(0), 399)

    g, path = shortest_path(g, 0, 200 * 200 - 1)
    g.add_path(path, color="blue")
    g.add_nodes_from(path, color="blue")
    draw_graph(g)

def draw_graph(g, labels=False):
    node_pos = {n[0]: (n[1]["x"], n[1]["y"]) if ("x" in n[1] and "y" in n[1]) else (0, 0) for n in g.nodes(data=True)}
    node_color_map = [n[1]["color"] if "color" in n[1] else color_by_level(n[1]["level"]) for n in g.nodes(data=True)]
    edge_color_map = [e[2]["color"] if "color" in e[2] else color_by_level(e[2]["weight"]) for e in g.edges(data=True)]
    nx.draw(g, pos=node_pos, node_size=10, node_color=node_color_map, edge_color=edge_color_map,
            with_labels=labels, font_size=8)
    plt.show()

def in_range(node, graph_id, size=10, interval_per_square=1):
    x = node[1]["x"]
    y = node[1]["y"]

    lx = (graph_id % size) * interval_per_square
    ly = (graph_id // size) * interval_per_square

    tx = lx + interval_per_square
    ty = ly + interval_per_square

    return x >= lx and x < tx and y >= ly and y < ty

def split_graph(G, squares_per_side=100, interval=1):
    total_nodes = len(G)
    graphs = []
    missed_connections = []
    node_to_id = {}
    for id in range(squares_per_side * squares_per_side):
        print(id)
        g = nx.Graph()
        g.add_nodes_from([n for n in G.nodes(data=True) if in_range(n, id, squares_per_side, interval)])
        G.add_nodes_from([n for n in G.nodes(data=True) if in_range(n, id, squares_per_side, interval)], color="blue")
        for n in g.nodes():
            node_to_id[n] = id
        for e in G.edges(data=True):
            if e[0] in g.node and e[1] in g.node:
                g.add_edges_from([e])
            elif (e[0] in g.node or e[1] in g.node) and e not in missed_connections:
                missed_connections.append(e)
        graphs.append(g)

    for id in range(squares_per_side * squares_per_side):
        print(id)
        g = graphs[id]
        for n in g.nodes():
            if len([_ for _ in g.neighbors(n)]) < 4:
                edge_list = []
                for e in missed_connections:
                    if e[0] == n:
                        edge_list.append({"neighbor": e[1], "graph": node_to_id[e[1]]})
                    elif e[1] == n:
                        edge_list.append({"neighbor": e[0], "graph": node_to_id[e[0]]})
                if len(edge_list):
                    g.add_node(n, edge=True, edge_list=edge_list)
                else:
                    g.add_node(n, edge=False)
            else:
                g.add_node(n, edge=False)

    return graphs

def graph_to_json(graph):


    return json.dumps(nx.node_link_data(graph))

def save_graph(g, gid):
    json_data = graph_to_json(g)
    f = open("graph/graph-{}.json".format(gid), "w")
    f.write(json_data)
    f.close()
    print("Created graph", gid)

def download_json_graph(path):
    json_data = json.loads(requests.get(path).content)
    return nx.node_link_graph(json_data)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "graph":
        g = new_square(0, 200)
        g = congest(g, 200)
        draw_graph(g)
        splits = split_graph(g, 20)
        for gid in range(0, 400):
            save_graph(splits[gid], gid)
        splits_low_res = split_graph(g, 5, 4)
        for gid in range(0, 25):
            save_graph(splits_low_res[gid], "low-res-{}".format(gid))
    else:
        color_shortest_test()


