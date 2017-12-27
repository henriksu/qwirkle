import unittest
from qwirkle.tile import Tile, Color, Shape
from qwirkle.hand import Hand
from qwirkle.board import Board, Position
from qwirkle.game import Player, BoardTurn, EndOfGame
from qwirkle.bag import Bag


class TestBoardTurn(unittest.TestCase):
    def test_early_play(self):
        tiles = [Tile(Color.RED, Shape.CLOVER),
                 Tile(Color.RED, Shape.DIAMOND),
                 Tile(Color.GREEN, Shape.SQUARE),
                 Tile(Color.PURPLE, Shape.SQUARE),
                 Tile(Color.YELLOW, Shape.STAR),
                 Tile(Color.PURPLE, Shape.STAR)]
        hand = Hand(tiles)
        player = Player(hand)
        board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
        bag = Bag([Tile(Color.GREEN, Shape.CIRCLE)])
        tiles_and_positions = [(Position(0, 1),
                               Tile(Color.RED, Shape.CLOVER))]
        turn = BoardTurn(board, player, bag, tiles_and_positions)
        turn.execute()
        self.assertEqual(2, player.total_score())
        expected_tiles_on_hand = [
            Tile(Color.RED, Shape.DIAMOND),
            Tile(Color.GREEN, Shape.SQUARE),
            Tile(Color.PURPLE, Shape.SQUARE),
            Tile(Color.YELLOW, Shape.STAR),
            Tile(Color.PURPLE, Shape.STAR),
            Tile(Color.GREEN, Shape.CIRCLE)]
        self.assertSetEqual(set(expected_tiles_on_hand),
                            set(player.hand.tiles))
        self.assertEqual(0, len(bag.tiles))

    def test_late_play(self):
        tiles = [Tile(Color.RED, Shape.CLOVER),
                 Tile(Color.RED, Shape.DIAMOND)]
        hand = Hand(tiles)
        player = Player(hand)
        board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
        bag = Bag([])
        tiles_and_positions = [(Position(0, 1),
                               Tile(Color.RED, Shape.CLOVER))]
        turn = BoardTurn(board, player, bag, tiles_and_positions)
        turn.execute()
        self.assertEqual(2, player.total_score())
        expected_tiles_on_hand = [
            Tile(Color.RED, Shape.DIAMOND)]
        self.assertSetEqual(set(expected_tiles_on_hand),
                            set(player.hand.tiles))
        self.assertEqual(0, len(bag.tiles))

    def test_last_play(self):
        tiles = [Tile(Color.RED, Shape.CLOVER)]
        hand = Hand(tiles)
        player = Player(hand, [1, 1])
        board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
        bag = Bag([])
        tiles_and_positions = [(Position(0, 1),
                               Tile(Color.RED, Shape.CLOVER))]
        turn = BoardTurn(board, player, bag, tiles_and_positions)
        with self.assertRaises(EndOfGame):
            turn.execute()
        self.assertEqual(2+6+2, player.total_score())
        expected_tiles_on_hand = []
        self.assertSetEqual(set(expected_tiles_on_hand),
                            set(player.hand.tiles))
        self.assertEqual(0, len(bag.tiles))
