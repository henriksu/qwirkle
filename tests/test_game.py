import unittest
from qwirkle.game import Game


class TestGame(unittest.TestCase):
    def test_make_game(self):
        game = Game(players=2)

class TestGameis(unittest.TestCase):
    def setUp(self):
        self.game = Game(players=2, seed=0)

    def test_racks(self):
        p1 = self.game.get_tiles(player=0)
        p1 = [str(tile) for tile in p1]
        p2 = self.game.get_tiles(player=1)
        p2 = [str(tile) for tile in p2]
        print(p1)
        print(p2)


if __name__ == '__main__':
    unittest.main()
