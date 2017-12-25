#!/usr/bin/env python
# encoding: utf-8
import unittest
from qwirkle.game import Board
from qwirkle.tile import Tile, Color, Shape
from qwirkle.board import Position


class TestBoard(unittest.TestCase):
    def test_init(self):
        Board()


class TestOneTileOnEmptyBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.tile = Tile(Color.RED, Shape.X)

    def test_one_tile_in_cener(self):
        move = (Position(0, 0), self.tile)
        result = self.board.is_allowed([move])
        self.assertTrue(result)

    def test_one_tile_above_off_center(self):
        move = (Position(0, 1), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)

    def test_one_tile_right_off_center(self):
        move = (Position(1, 0), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)

    def test_one_tile_above_right_off_center(self):
        move = (Position(1, 1), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)

    def test_one_tile_belove_left_off_center(self):
        move = (Position(-1, -1), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)


class TestTwoCompatibleTilesOnEmptyBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.tile1 = Tile(Color.RED, Shape.X)
        self.tile2 = Tile(Color.RED, Shape.DIAMOND)

    def test_origin_right(self):
        move = [(Position(0, 0), self.tile1),
                (Position(1, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)

    def test_origin_left(self):
        move = [(Position(-1, 0), self.tile1),
                (Position(0, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)

    def test_origin_down(self):
        move = [(Position(0, 0), self.tile1),
                (Position(0, -1), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)

    def test_origin_up(self):
        move = [(Position(0, 1), self.tile1),
                (Position(0, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)

    def test_origin_diagonal(self):
        move = [(Position(1, 1), self.tile1),
                (Position(0, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertFalse(result)


class TestIncompatibleTilesOneEmptyBoard(unittest.TestCase):
    def test_different_color_and_shape(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.GREEN, Shape.CIRCLE)
        move = [(Position(0, 0), tile1),
                (Position(0, 1), tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)

    def test_duplicate_position(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.DIAMOND)
        move = [(Position(0, 0), tile1),
                (Position(0, 0), tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)

    def test_non_contiguous(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        move = [(Position(0, 0), tile1),
                (Position(0, 2), tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)

    def test_non_contiguous2(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        move = [(Position(0, 0), tile1),
                (Position(2, 0), tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)


class TestSecondMoveFromOneTile(unittest.TestCase):
    def setUp(self):
        tile = Tile(Color.RED, Shape.X)
        self.board = Board([(Position(0, 0), tile)])

    def test_add_red_horizontally(self):
        tile = Tile(Color.RED, Shape.CIRCLE)
        result = self.board.is_allowed([(Position(1, 0), tile)])
        self.assertTrue(result)

    def test_add_x_horizontally(self):
        tile = Tile(Color.GREEN, Shape.X)
        result = self.board.is_allowed([(Position(1, 0), tile)])
        self.assertTrue(result)

    def test_add_red_vertically(self):
        tile = Tile(Color.RED, Shape.CIRCLE)
        result = self.board.is_allowed([(Position(0, 1), tile)])
        self.assertTrue(result)

    def test_add_x_vertically(self):
        tile = Tile(Color.GREEN, Shape.X)
        result = self.board.is_allowed([(Position(0, 1), tile)])
        self.assertTrue(result)

    def test_add_two_horizontally(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(1, 0), tile1),
                                        (Position(2, 0), tile2)])
        self.assertTrue(result)

    def test_add_two_horizontally2(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(1, 0), tile1),
                                        (Position(-1, 0), tile2)])
        self.assertTrue(result)

    def test_add_two_vertically(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(0, 1), tile1),
                                        (Position(0, 2), tile2)])
        self.assertTrue(result)

    def test_add_two_vertically2(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(0, 1), tile1),
                                        (Position(0, -1), tile2)])
        self.assertTrue(result)

    def test_add_two_in_different_direction(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(0, 1), tile1),
                                        (Position(1, 0), tile2)])
        self.assertFalse(result)

    def test_add_one_diagonally(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        result = self.board.is_allowed([(Position(1, 1), tile1)])
        self.assertFalse(result)

    def test_add_one_illegal(self):
        tile1 = Tile(Color.GREEN, Shape.CIRCLE)
        result = self.board.is_allowed([(Position(1, 0), tile1)])
        self.assertFalse(result)

    def test_add_one_identical(self):
        tile1 = Tile(Color.RED, Shape.X)
        result = self.board.is_allowed([(Position(1, 0), tile1)])
        self.assertFalse(result)


class TestLineSpecificIndexes(unittest.TestCase):
    def setUp(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        tile3 = Tile(Color.RED, Shape.SQUARE)
        tile4 = Tile(Color.RED, Shape.CLOVER)
        tile5 = Tile(Color.GREEN, Shape.CLOVER)
        tile6 = Tile(Color.ORANGE, Shape.CLOVER)
        tile7 = Tile(Color.YELLOW, Shape.CLOVER)
        self.board = Board([(Position(0, 0), tile1),
                            (Position(1, 0), tile2),
                            (Position(2, 0), tile3),
                            (Position(3, 0), tile4),
                            (Position(3, 1), tile5),
                            (Position(3, 2), tile6),
                            (Position(3, 3), tile7)])

    def test_column_one_tile(self):
        tile1 = Tile(Color.YELLOW, Shape.X)
        result = self.board.is_allowed([(Position(0, 1), tile1)])
        self.assertTrue(result)

    def test_row_one_tile(self):
        tile1 = Tile(Color.YELLOW, Shape.X)
        result = self.board.is_allowed([(Position(2, 3), tile1)])
        self.assertTrue(result)

    def test_column_two_tiles(self):
        tile1 = Tile(Color.YELLOW, Shape.X)
        tile2 = Tile(Color.ORANGE, Shape.X)
        result = self.board.is_allowed([(Position(0, 1), tile1),
                                        (Position(0, 2), tile2)])
        self.assertTrue(result)

    def test_row_two_tiles(self):
        tile1 = Tile(Color.YELLOW, Shape.X)
        tile2 = Tile(Color.YELLOW, Shape.CIRCLE)
        result = self.board.is_allowed([(Position(2, 3), tile1),
                                        (Position(1, 3), tile2)])
        self.assertTrue(result)


class TestRowStrikes(unittest.TestCase):
    def setUp(self):
        tile = Tile(Color.RED, Shape.X)
        self.board = Board([(Position(0, 0), tile)])

    def test_legal_multi_tile_row(self):
        tile1 = Tile(Color.RED, Shape.DIAMOND)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(1, 0), tile1),
                                        (Position(2, 0), tile2)])
        self.assertTrue(result)

    def test_illegal_multi_tile_row2(self):
        tile1 = Tile(Color.GREEN, Shape.DIAMOND)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(0, 1), tile1),
                                        (Position(1, 1), tile2)])
        self.assertFalse(result)

    def test_illegal_multi_tile_row1(self):
        tile1 = Tile(Color.GREEN, Shape.DIAMOND)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        result = self.board.is_allowed([(Position(1, 0), tile1),
                                        (Position(2, 0), tile2)])
        self.assertFalse(result)


class TestMakeMove(unittest.TestCase):
    def test_valid_move(self):
        tile1 = Tile(Color.RED, Shape.X)
        board = Board([(Position(0, 0), tile1)])
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        score = board.make_move([(Position(0, 1), tile2)])
        self.assertEqual(2, score)
        tiles = board.tiles
        expected = [(Position(0, 0), tile1),
                    (Position(0, 1), tile2)]
        self.assertListEqual(expected, tiles)

    def test_illegal_move(self):
        tile1 = Tile(Color.RED, Shape.X)
        board = Board([(Position(0, 0), tile1)])
        tile2 = Tile(Color.GREEN, Shape.CIRCLE)
        with self.assertRaises(ValueError):
            board.make_move([(Position(0, 1), tile2)])
        tiles = board.tiles
        expected = [Position(Position(0, 0), tile1)]
        self.assertListEqual(expected, tiles)

    def test_qwirkle_score(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CLOVER)
        tile3 = Tile(Color.RED, Shape.DIAMOND)
        tile4 = Tile(Color.RED, Shape.SQUARE)
        tile5 = Tile(Color.RED, Shape.STAR)
        tile6 = Tile(Color.RED, Shape.X)
        board = Board()
        move = [(Position(0, 0), tile1),
                (Position(1, 0), tile2),
                (Position(2, 0), tile3),
                (Position(3, 0), tile4),
                (Position(4, 0), tile5),
                (Position(5, 0), tile6)]
        score = board.make_move(move)
        self.assertEqual(12, score)


if __name__ == '__main__':
    unittest.main()
