import math
from collections import defaultdict
from heapq import heappush, heappop

import pathfinder


def shortest_path_tree(graph):
    """
    Computes the shortest path tree of a graph.
    :param graph: The graph to process.
    :return: A mapping of node -> parent node.
    """
    adj = defaultdict(list)
    for (u, v) in graph.roads:
        adj[u].append(v)

    distance = defaultdict(lambda: math.inf)
    parent = defaultdict(lambda: None)
    distance[graph.start] = 0
    q = []
    heappush(q, (0, graph.start))
    while q:
        (dist, node) = heappop(q)

        if node == graph.treasure:
            return parent

        for next_node in adj[node]:
            if dist + 1 < distance[next_node]:
                distance[next_node] = dist + 1
                parent[next_node] = node
                heappush(q, (dist + 1, next_node))

    return parent


def getTreasure(graph, new_graph):

    treasurePAths = []
    for treasure in graph.treasure:
        other_graph = new_graph
        other_graph.treasure = treasure

        parent = shortest_path_tree(new_graph)

        ret = backtrace(treasure, parent)
        # The graph is connected...
        assert (ret[0] == graph.start)

        treasurePAths.append(ret)

    return min(treasurePAths, key=len)



def backtrace(node, parent):
    """
    :param node: The starting node
    :param parent: The parent of all nodes
    :return: A list in order of the visited nodes
    """
    return [] if node is None else backtrace(parent[node], parent) + [node]



def bidirectional_shortest_path(graph):
    """
    Computes the minimal path in a bidirectional graph.
    :param graph: The graph to process.
    :return: An array with the indices of places to visit.
    """
    new_graph = pathfinder.TreasureMap()
    new_graph.start = graph.start
    new_graph.roads = set()
    # Because walking is bidirectional...
    for (u, v) in graph.roads:
        new_graph.roads.add((u, v))
        new_graph.roads.add((v, u))

    return getTreasure(graph, new_graph)


def states_shortest_path(graph):
    """
    Computes minimal path in a graph with different states.
    :param graph: The graph to process.
    :return: An array with the indices of places to visit.
    """
    new_graph = pathfinder.TreasureMap()
    new_graph.start = (graph.start, 0)

    adj = defaultdict(set)
    for (u, v) in graph.roads:
        for it in range(3):
            adj[(u, it)].add((v, (it + 1) % 3))
            adj[(v, it)].add((u, (it + 1) % 3))
    for adj_nodes in adj.values():
        for dragon in graph.dragons:
            if (dragon, 0) in adj_nodes:
                adj_nodes.remove((dragon, 0))

    new_graph.roads = [(node, adj_node)
                       for node, adj_nodes in adj.items()
                       for adj_node in adj_nodes]

    parent = shortest_path_tree(new_graph)
    solutions = []
    for it in range(3):
        ret = backtrace((graph.treasure, it), parent)
        # The graph is connected...
        if ret[0] == (graph.start, 0):
            solutions.append([item[0] for item in ret])

    assert (solutions)
    return min(solutions, key=lambda solution: len(solution))


def restricted_shortest_path(graph):
    """
    Computes the minimal path in a residual graph G - p, where p is the minimal path.
    :param graph: The graph to process.
    :return: An array with the indices of places to visit.
    """
    nodes = bidirectional_shortest_path(graph)

    print(nodes)

    new_graph = pathfinder.TreasureMap()
    new_graph.start = graph.start
    roads = set(graph.roads)
    for i in range(len(nodes) - 1):
        edge = (nodes[i], nodes[i + 1])
        if edge in roads:
            roads.remove(edge)
    new_graph.roads = []
    for (u, v) in roads:
        new_graph.roads.append((u, v))
        new_graph.roads.append((v, u))


    return getTreasure(graph, new_graph)
