import unittest
from qwirkle.game_logic.board import Position


class TestNeighbours(unittest.TestCase):
    def test_neighbours(self):
        pos = Position(0, 0)
        neighbours = pos.neighbour_positions()
        expected = set([Position(1, 0),
                        Position(-1, 0),
                        Position(0, 1),
                        Position(0, -1)])
        self.assertSetEqual(expected, set(neighbours))
