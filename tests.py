import unittest

from pathfinder import TreasureMap
from solver import bidirectional_shortest_path, states_shortest_path, restricted_shortest_path


class BidirectionalShortestPathTest(unittest.TestCase):

    def test_single(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 0
        map.roads = []
        self.assertEqual(bidirectional_shortest_path(map), [0])

    def test_shortest(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 2
        map.roads = [(0, 1), (1, 2), (0, 2)]
        self.assertEqual(bidirectional_shortest_path(map), [0, 2])

    def test_bidirectional(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 2
        map.roads = [(0, 1), (2, 1)]
        self.assertEqual(bidirectional_shortest_path(map), [0, 1, 2])

    def test_graph_disconnected(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 3
        map.roads = [(0, 1), (2, 3)]
        self.assertRaises(AssertionError, bidirectional_shortest_path, map)


class StatesShortestPathTest(unittest.TestCase):

    def test_dragon_finished_sneezing_at_start_of_journey(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 3
        map.roads = [(0, 1), (1, 2), (2, 3)]
        map.dragons = [0]
        self.assertEqual(states_shortest_path(map), [0, 1, 2, 3])

    def test_avoid_dragon_by_jumping_back(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 3
        map.roads = [(0, 1), (1, 2), (2, 3)]
        map.dragons = [3]
        self.assertEqual(states_shortest_path(map), [0, 1, 0, 1, 2, 3])

    def test_graph_disconnected(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 3
        map.roads = [(0, 1), (2, 3)]
        self.assertRaises(AssertionError, states_shortest_path, map)


class RestrictedShortestPathTest(unittest.TestCase):

    def test_single(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 0
        map.roads = []
        self.assertEqual(restricted_shortest_path(map), [0])

    def test_no_alternative_route(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 2
        map.roads = [(0, 1), (1, 2)]
        self.assertRaises(AssertionError, restricted_shortest_path, map)

    def test_avoid_paths(self):
        map = TreasureMap()
        map.start = 0
        map.treasure = 4
        map.roads = [(0, 1), (1, 4), (0, 2), (2, 1), (1, 3), (3, 4)]
        self.assertEqual(restricted_shortest_path(map), [0, 2, 1, 3, 4])
