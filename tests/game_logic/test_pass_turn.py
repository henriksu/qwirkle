import unittest
from qwirkle.game_logic.game import PassTurn, Player, IllegalPass
from qwirkle.game_logic.hand import Hand
from qwirkle.game_logic.bag import Bag
from qwirkle.game_logic.tile import Tile, Shape, Color


class TestPassTurn(unittest.TestCase):
    def test_passing_turn(self):
        tiles = [Tile(Color.RED, Shape.CIRCLE)]
        hand = Hand(tiles)
        player = Player(hand)
        bag = Bag([])
        board = MockBoard(moves=[], possible_moves=[1, 2, 3])
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
        board = MockBoard(moves=['Unseen or unwanted move'], possible_moves=[1, 2, 3])
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
        board = MockBoard(moves=[], possible_moves=[1, 2, 3])
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
        board = MockBoard(moves=['unwanted move'], possible_moves=[1, 2, 3])
        turn = PassTurn(player, bag, board)
        with self.assertRaises(IllegalPass):
            turn.execute()
        points = player.total_score()
        self.assertEqual(0, points)
        self.assertListEqual(tiles, player.hand.tiles)


class MockBoard():
    def __init__(self, moves, possible_moves):
        self.moves = moves
        self.possible_moves = possible_moves

    def legal_single_piece_moves(self, hand):
        return self.moves

    def legal_positions_with_exhaustion(self):
        return self.possible_moves
