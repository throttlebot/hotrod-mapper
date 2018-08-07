import networkx as nx
import sys, time, json, math

def shortest_path(g, s, e):
    print("Start {}. End: {}".format(s, e))
    t = time.clock()

    closedSet = {}
    openSet = {n: True for n in g.nodes()}
    cameFrom = {}
    gScore = {n: sys.maxint for n in g.nodes()}
    gScore[s] = 0
    fScore = {n: sys.maxint for n in g.nodes()}
    nodes = g.nodes(data=True)
    fScore[s] = heuristic(nodes[s], nodes[e])

    while len(openSet):
        current = smallest(openSet, fScore)
        if current == e:
            print("Time Taken: {}".format(time.clock() - t))
            print("Distance: {}".format(gScore[current]))
            path = reconstruct_path(cameFrom, current)
            print("Path: {}".format(path))
            return g, reconstruct_path(cameFrom, current)
        openSet.pop(current)
        closedSet[current] = True

        neighbors, g, nodes = neighbor(g, current, nodes)
        for n in [n for n in neighbors]:
            if n in closedSet:
                continue

            edge = (current, n) if (current, n) in g.edges else (n, current)
            tentativeScore = gScore[current] + g.edges[edge]["weight"]

            if n not in openSet:
                openSet[n] = True
            elif tentativeScore >= gScore[n]:
                continue

            cameFrom[n] = current
            gScore[n] = tentativeScore
            fScore[n] = tentativeScore + heuristic(nodes[n], nodes[e])

def neighbor(g, n, nodes):
    change = False
    if nodes[n]["edge"]:
        for extension in nodes[n]["edge_list"]:
            if extension["neighbor"] not in g.nodes:
                g = download_and_merge(g, extension["graph"])
                change = True
    if change:
        nodes = g.nodes(data=True)
    return g.neighbors(n), g, nodes

def download_and_merge(g, gid):
    new_g = download(gid)
    new_ret = nx.compose(g, new_g)
    for n in g.nodes(data=True):
        if n[1]["edge"]:
            for e in n[1]["edge_list"]:
                if e["neighbor"] in new_ret.nodes:
                    if new_ret.node[e["neighbor"]]["level"] == 3 or n[1]["level"] == 3:
                        new_ret.add_edge(e["neighbor"], n[0], weight=3)
                    elif new_ret.node[e["neighbor"]]["level"] == 2 or n[1]["level"] == 2:
                        new_ret.add_edge(e["neighbor"], n[0], weight=2)
                    else:
                        new_ret.add_edge(e["neighbor"], n[0], weight=1)
    return new_ret

def download(gid):
    f = open("graph/graph-{}.json".format(gid), "r")
    data = f.read()
    f.close()
    return nx.node_link_graph(json.loads(data))

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path

def smallest(openSet, fScore):
    return sorted(openSet.keys(), key=lambda x: fScore[x])[0]

def heuristic(xv, yv):
    return 1.5 * (abs(xv["x"] - yv["x"]) * 10 + abs(xv["y"] - yv["y"]) * 10)

