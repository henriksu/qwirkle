#!/usr/bin/env python
# encoding: utf-8
import unittest
from qwirkle.game import Board
from qwirkle.tile import Tile, Color, Shape
from qwirkle.board import Position


class TestExamples(unittest.TestCase):

    def test_example_a(self):
        board = Board()
        move = self.tiles[:3]
        score = board.make_move(move)
        self.assertEqual(3, score)

    def test_example_b(self):
        starting_position = self.tiles[:3]
        board = Board(starting_position)
        move = self.tiles[3:6]
        score = board.make_move(move)
        self.assertEqual(7, score)

    def test_example_c(self):
        starting_position = self.tiles[:6]
        board = Board(starting_position)
        move = self.tiles[6:7]
        score = board.make_move(move)
        self.assertEqual(4, score)

    def test_example_d(self):
        starting_position = self.tiles[:7]
        board = Board(starting_position)
        move = self.tiles[7:9]
        score = board.make_move(move)
        self.assertEqual(6, score)

    def test_example_e(self):
        starting_position = self.tiles[:9]
        board = Board(starting_position)
        move = self.tiles[9:11]
        score = board.make_move(move)
        self.assertEqual(7, score)

    def test_example_f(self):
        starting_position = self.tiles[:11]
        board = Board(starting_position)
        move = self.tiles[11:13]
        score = board.make_move(move)
        self.assertEqual(6, score)

    def test_example_g(self):
        starting_position = self.tiles[:13]
        board = Board(starting_position)
        move = self.tiles[13:15]
        score = board.make_move(move)
        self.assertEqual(3, score)

    def test_example_h(self):
        starting_position = self.tiles[:15]
        board = Board(starting_position)
        move = self.tiles[15:17]
        score = board.make_move(move)
        self.assertEqual(3, score)

    def test_example_i(self):
        starting_position = self.tiles[:17]
        board = Board(starting_position)
        move = self.tiles[17:19]
        score = board.make_move(move)
        self.assertEqual(10, score)

    def test_example_j(self):
        starting_position = self.tiles[:19]
        board = Board(starting_position)
        move = self.tiles[19:20]
        score = board.make_move(move)
        self.assertEqual(9, score)

    def test_example_k(self):
        starting_position = self.tiles[:20]
        board = Board(starting_position)
        move = self.tiles[20:23]
        score = board.make_move(move)
        self.assertEqual(18, score)

    def test_example_l(self):
        starting_position = self.tiles[:23]
        board = Board(starting_position)
        move = self.tiles[23:25]
        score = board.make_move(move)
        self.assertEqual(9, score)

    def test_all(self):
        # a
        board = Board()
        move = self.tiles[:3]
        score = board.make_move(move)
        self.assertEqual(3, score)
        # b
        move = self.tiles[3:6]
        score = board.make_move(move)
        self.assertEqual(7, score)
        # c
        move = self.tiles[6:7]
        score = board.make_move(move)
        self.assertEqual(4, score)
        # d
        move = self.tiles[7:9]
        score = board.make_move(move)
        self.assertEqual(6, score)
        # e
        move = self.tiles[9:11]
        score = board.make_move(move)
        self.assertEqual(7, score)
        # f
        move = self.tiles[11:13]
        score = board.make_move(move)
        self.assertEqual(6, score)
        # g
        move = self.tiles[13:15]
        score = board.make_move(move)
        self.assertEqual(3, score)
        # h
        move = self.tiles[15:17]
        score = board.make_move(move)
        self.assertEqual(3, score)
        # i
        move = self.tiles[17:19]
        score = board.make_move(move)
        self.assertEqual(10, score)
        # j
        move = self.tiles[19:20]
        score = board.make_move(move)
        self.assertEqual(9, score)
        # k
        move = self.tiles[20:23]
        score = board.make_move(move)
        self.assertEqual(18, score)
        # l
        move = self.tiles[23:25]
        score = board.make_move(move)
        self.assertEqual(9, score)

    @classmethod
    def setUpClass(cls):
        super(TestExamples, cls).setUpClass()
        pos1 = Position(0, 0)
        tile1 = Tile(Color.RED, Shape.CLOVER)
        pos2 = Position(0, -1)
        tile2 = Tile(Color.RED, Shape.DIAMOND)
        pos3 = Position(0, -2)
        tile3 = Tile(Color.RED, Shape.CIRCLE)
        pos4 = Position(0, -3)
        tile4 = Tile(Color.RED, Shape.SQUARE)
        pos5 = Position(1, -3)
        tile5 = Tile(Color.BLUE, Shape.SQUARE)
        pos6 = Position(2, -3)
        tile6 = Tile(Color.PURPLE, Shape.SQUARE)
        pos7 = Position(1, -2)
        tile7 = Tile(Color.BLUE, Shape.CIRCLE)
        pos8 = Position(-1, 0)
        tile8 = Tile(Color.GREEN, Shape.CLOVER)
        pos9 = Position(-1, -1)
        tile9 = Tile(Color.GREEN, Shape.DIAMOND)
        pos10 = Position(-1, 1)
        tile10 = Tile(Color.GREEN, Shape.STAR)
        pos11 = Position(-1, -2)
        tile11 = Tile(Color.GREEN, Shape.CIRCLE)
        pos12 = Position(3, -3)
        tile12 = Tile(Color.ORANGE, Shape.SQUARE)
        pos13 = Position(3, -4)
        tile13 = Tile(Color.RED, Shape.SQUARE)
        pos14 = Position(-3, 1)
        tile14 = Tile(Color.ORANGE, Shape.STAR)
        pos15 = Position(-2, 1)
        tile15 = Tile(Color.YELLOW, Shape.STAR)
        pos16 = Position(-3, 0)
        tile16 = Tile(Color.ORANGE, Shape.X)
        pos17 = Position(-3, -1)
        tile17 = Tile(Color.ORANGE, Shape.DIAMOND)
        pos18 = Position(-2, -1)
        tile18 = Tile(Color.YELLOW, Shape.DIAMOND)
        pos19 = Position(-2, -2)
        tile19 = Tile(Color.YELLOW, Shape.CIRCLE)
        pos20 = Position(0, 1)
        tile20 = Tile(Color.RED, Shape.STAR)
        pos21 = Position(-1, -4)
        tile21 = Tile(Color.ORANGE, Shape.X)
        pos22 = Position(0, -4)
        tile22 = Tile(Color.RED, Shape.X)
        pos23 = Position(1, -4)
        tile23 = Tile(Color.BLUE, Shape.X)
        pos24 = Position(4, -3)
        tile24 = Tile(Color.YELLOW, Shape.SQUARE)
        pos25 = Position(4, -4)
        tile25 = Tile(Color.BLUE, Shape.SQUARE)
        cls.tiles = [(pos1, tile1),
                     (pos2, tile2),
                     (pos3, tile3),
                     (pos4, tile4),
                     (pos5, tile5),
                     (pos6, tile6),
                     (pos7, tile7),
                     (pos8, tile8),
                     (pos9, tile9),
                     (pos10, tile10),
                     (pos11, tile11),
                     (pos12, tile12),
                     (pos13, tile13),
                     (pos14, tile14),
                     (pos15, tile15),
                     (pos16, tile16),
                     (pos17, tile17),
                     (pos18, tile18),
                     (pos19, tile19),
                     (pos20, tile20),
                     (pos21, tile21),
                     (pos22, tile22),
                     (pos23, tile23),
                     (pos24, tile24),
                     (pos25, tile25)]
