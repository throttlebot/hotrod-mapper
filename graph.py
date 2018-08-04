import networkx as nx
import random, json, requests
from multiprocessing import Pool
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def new_graph(nodes):
    G = nx.Graph()
    G.add_nodes_from(range(0, nodes))
    weight = 0.2

    for x in range(0, nodes - 10):
        for y in range(x, x + 10):
            if random.random() < weight:
                G.add_edge(x, y, weight=random.randrange(1, 10))

    to_remove = []
    for n in G.nodes().keys():
        if nx.degree(G, n) == 0:
            to_remove.append(n)

    G.remove_nodes_from(to_remove)

    connect = nx.all_pairs_node_connectivity(G)
    for s, t in connect.items():
        if not all([p > 0 for p in t.values()]):
            return new_graph(nodes)
    print("Generated new graph.")
    return G

def color_shortest(g):
    assert len(g.nodes) > 1
    path = nx.shortest_path(g, list(g.nodes().keys())[0], list(g.nodes().keys())[-1], "weight")
    print(path, file=sys.stdout)
    g.add_path(path, color="red")
    g.add_nodes_from(path, color="red")

def save_to_buf(g, buf):
    node_color_map = [n[1]["color"] if "color" in n[1] else "yellow" for n in g.nodes(data=True)]
    edge_color_map = [e[2]["color"] if "color" in e[2] else "black" for e in g.edges(data=True)]
    nx.draw(g, node_color=node_color_map, edge_color=edge_color_map, node_size=150, font_size=7, with_labels=True)
    plt.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    plt.close()

def graph_to_json(graph):
    return json.dumps(nx.node_link_data(graph))

def create_and_save_graph(i):
    g = new_graph(100)
    json_data = graph_to_json(g)
    f = open("graph/graph-{}.json".format(i), "w")
    f.write(json_data)
    f.close()
    print("Created graph", i)

def download_json_graph(path):
    json_data = json.loads(requests.get(path).content)
    return nx.node_link_graph(json_data)

if __name__ == '__main__':
    p = Pool(4)
    print(p.map(create_and_save_graph, [i for i in range(100)]))
