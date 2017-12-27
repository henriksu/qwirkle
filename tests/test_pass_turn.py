import unittest
from qwirkle.game import PassTurn, Player, IllegalPass
from qwirkle.hand import Hand
from qwirkle.bag import Bag
from qwirkle.tile import Tile, Shape, Color


class TestPassTurn(unittest.TestCase):
    def test_passing_turn(self):
        tiles = [Tile(Color.RED, Shape.CIRCLE)]
        hand = Hand(tiles)
        player = Player(hand)
        bag = Bag([])
        board = MockBoard(moves=[])
        turn = PassTurn(player, bag, board)
        turn.execute()
        points = player.total_score()
        self.assertEqual(0, points)
        tiles = [Tile(Color.RED, Shape.CIRCLE)]
        self.assertListEqual(tiles, player.hand.tiles)


class TestIllegalPassTurn(unittest.TestCase):
    def test_illegal_attempt_at_passing_legel_move(self):
        tiles = [Tile(Color.RED, Shape.CIRCLE)]
        hand = Hand(tiles)
        player = Player(hand)
        bag = Bag([])
        board = MockBoard(moves=['Unseen or unwanted move'])
        turn = PassTurn(player, bag, board)
        with self.assertRaises(IllegalPass):
            turn.execute()
        points = player.total_score()
        self.assertEqual(0, points)
        self.assertListEqual(tiles, player.hand.tiles)

    def test_illegal_attempt_at_passing_nonempty_bag(self):
        tiles = [Tile(Color.RED, Shape.CIRCLE)]
        hand = Hand(tiles)
        player = Player(hand)
        bag = Bag(['Tile in bag'])
        board = MockBoard(moves=[])
        turn = PassTurn(player, bag, board)
        with self.assertRaises(IllegalPass):
            turn.execute()
        points = player.total_score()
        self.assertEqual(0, points)
        self.assertListEqual(tiles, player.hand.tiles)

    def test_illegal_attempt_at_passing_both(self):
        tiles = [Tile(Color.RED, Shape.CIRCLE)]
        hand = Hand(tiles)
        player = Player(hand)
        bag = Bag(['Tile in bag'])
        board = MockBoard(moves=['unwanted move'])
        turn = PassTurn(player, bag, board)
        with self.assertRaises(IllegalPass):
            turn.execute()
        points = player.total_score()
        self.assertEqual(0, points)
        self.assertListEqual(tiles, player.hand.tiles)


class MockBoard():
    def __init__(self, moves):
        self.moves = moves

    def legal_moves(self, hand):
        return self.moves
