import math
from collections import defaultdict
from heapq import heappush, heappop

import pathfinder


def shortest_path_tree(graph):
    """
    Computes the minimal distance in a graph.
    :param graph: The graph to compute the minimal distance.
    :return: An array with the indices of places to visit.
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
        for next_node in adj[node]:
            if dist + 1 < distance[next_node]:
                distance[next_node] = dist + 1
                parent[next_node] = node
                heappush(q, (dist + 1, next_node))

    return parent


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
    treasure_map = pathfinder.TreasureMap()
    treasure_map.start = graph.start
    treasure_map.roads = set()
    # Because walking is bidirectional...
    for (u, v) in graph.roads:
        treasure_map.roads.add((u, v))
        treasure_map.roads.add((v, u))

    parent = shortest_path_tree(graph)
    ret = backtrace(graph.treasure, parent)
    # The graph is connected...
    assert (ret[0] == graph.start)
    return ret


def states_shortest_path(graph):
    """
    Computes minimal path in a graph with different states.
    :param graph: The graph to process.
    :return: An array with the indices of places to visit.
    """
    treasure_map = pathfinder.TreasureMap()
    treasure_map.start = (graph.start, 0)

    adj = defaultdict(set)
    for (u, v) in graph.roads:
        for it in range(3):
            adj[(u, it)].add((v, (it + 1) % 3))
            adj[(v, it)].add((u, (it + 1) % 3))
    for adj_nodes in adj.values():
        for dragon in graph.dragons:
            if (dragon, 0) in adj_nodes:
                adj_nodes.remove((dragon, 0))

    treasure_map.roads = [(node, adj_node)
                          for node, adj_nodes in adj.items()
                          for adj_node in adj_nodes]

    parent = shortest_path_tree(treasure_map)
    solutions = []
    for it in range(3):
        ret = backtrace((graph.treasure, it), parent)
        # The graph is connected...
        if ret[0] == (graph.start, 0):
            solutions.append([item[0] for item in ret])

    return min(solutions, key=lambda solution: len(solution))


def restricted_shortest_path(graph):
    """
    Computes the minimal path in a residual graph G - p, where p is the minimal path.
    :param graph: The graph to process.
    :return: An array with the indices of places to visit.
    """
    nodes = bidirectional_shortest_path(graph)

    treasure_map = pathfinder.TreasureMap()
    treasure_map.start = graph.start
    roads = set(graph.roads)
    for i in range(len(nodes) - 1):
        edge = (nodes[i], nodes[i + 1])
        if edge in roads:
            roads.remove(edge)
    treasure_map.roads = []
    for (u, v) in roads:
        treasure_map.roads.append((u, v))
        treasure_map.roads.append((v, u))

    parent = shortest_path_tree(treasure_map)
    ret = backtrace(graph.treasure, parent)
    # The graph is connected...
    assert (ret[0] == graph.start)
    return ret
