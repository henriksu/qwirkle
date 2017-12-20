#!/usr/bin/env python
# encoding: utf-8
import unittest
from qwirkle.game import Board
from qwirkle.tile import Tile, Color, Shape

class TestBoard(unittest.TestCase):
    def test_init(self):
        Board()

class TestOneTileOnEmptyBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.tile = Tile(Color.RED, Shape.X)

    def test_one_tile_in_cener(self):
        move = ((0, 0), self.tile)
        result = self.board.is_allowed([move])
        self.assertTrue(result)

    def test_one_tile_above_off_center(self):
        move = ((0, 1), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)

    def test_one_tile_right_off_center(self):
        move = ((1, 0), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)
        
    def test_one_tile_above_right_off_center(self):
        move = ((1, 1), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)

    def test_one_tile_belove_left_off_center(self):
        move = ((-1, -1), self.tile)
        result = self.board.is_allowed([move])
        self.assertFalse(result)

class TestTwoCompatibleTilesOnEmptyBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.tile1 = Tile(Color.RED, Shape.X)
        self.tile2 = Tile(Color.RED, Shape.DIAMOND)
    
    def test_origin_right(self):
        move = [((0, 0), self.tile1),
                ((1, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)
    
    def test_origin_left(self):
        move = [((-1, 0), self.tile1),
                ((0, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)

    def test_origin_down(self):
        move = [((0, 0), self.tile1),
                ((0, -1), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)

    def test_origin_up(self):
        move = [((0, 1), self.tile1),
                ((0, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertTrue(result)
        
    def test_origin_diagonal(self):
        move = [((1, 1), self.tile1),
                ((0, 0), self.tile2)]
        result = self.board.is_allowed(move)
        self.assertFalse(result)

        
        
class TestIncompatibleTilesOneEmptyBoard(unittest.TestCase):
    def test_different_color_and_shape(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.GREEN, Shape.CIRCLE)
        move = [((0,0),tile1),
                ((0,1),tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)
    
    def test_duplicate_position(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.DIAMOND)
        move = [((0, 0), tile1),
                ((0, 0), tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)

    def test_non_contiguous(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        move = [((0,0),tile1),
                ((0,2),tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)

    def test_non_contiguous2(self):
        board = Board()
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        move = [((0,0),tile1),
                ((2,0),tile2)]
        result = board.is_allowed(move)
        self.assertFalse(result)
    
class TestSecondMoveFromOneTile(unittest.TestCase):
    def setUp(self):
        tile = Tile(Color.RED, Shape.X)
        self.board = Board([((0,0),tile)])
        
    def test_add_red_horizontally(self):
        tile = Tile(Color.RED, Shape.CIRCLE)
        result = self.board.is_allowed([((1,0), tile)])
        self.assertTrue(result)

    def test_add_x_horizontally(self):
        tile = Tile(Color.GREEN, Shape.X)
        result = self.board.is_allowed([((1,0), tile)])
        self.assertTrue(result)

    def test_add_red_vertically(self):
        tile = Tile(Color.RED, Shape.CIRCLE)
        result = self.board.is_allowed([((0,1), tile)])
        self.assertTrue(result)

    def test_add_x_vertically(self):
        tile = Tile(Color.GREEN, Shape.X)
        result = self.board.is_allowed([((0,1), tile)])
        self.assertTrue(result)
    
    def test_add_two_horizontally(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CROSS)
        result = self.board.is_allowed([((1,0), tile1),
                                        ((2,0), tile2)])
        self.assertTrue(result)

    def test_add_two_horizontally2(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CROSS)
        result = self.board.is_allowed([((1,0), tile1),
                                        ((-1,0), tile2)])
        self.assertTrue(result)

    def test_add_two_vertically(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CROSS)
        result = self.board.is_allowed([((0,1), tile1),
                                        ((0,2), tile2)])
        self.assertTrue(result)

    def test_add_two_vertically2(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CROSS)
        result = self.board.is_allowed([((0,1), tile1),
                                        ((0,-1), tile2)])
        self.assertTrue(result)
        
    def test_add_two_in_different_direction(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        tile2 = Tile(Color.RED, Shape.CROSS)
        result = self.board.is_allowed([((0,1), tile1),
                                        ((1, 0), tile2)])
        self.assertFalse(result)

    def test_add_one_diagonally(self):
        tile1 = Tile(Color.RED, Shape.CIRCLE)
        result = self.board.is_allowed([((1,1), tile1)])
        self.assertFalse(result)

    def test_add_one_illegal(self):
        tile1 = Tile(Color.GREEN, Shape.CIRCLE)
        result = self.board.is_allowed([((1,0), tile1)])
        self.assertFalse(result)

    def test_add_one_identical(self):
        tile1 = Tile(Color.RED, Shape.X)
        result = self.board.is_allowed([((1,0), tile1)])
        self.assertFalse(result)

class TestSecondMoveFromTwoTiles(unittest.TestCase):
    def setUp(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.CIRCLE)
        self.board = Board([((0,0),tile1),
                            ((1,0), tile2)])

    
    
if __name__ == '__main__':
    unittest.main()

