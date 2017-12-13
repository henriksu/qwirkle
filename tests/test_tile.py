import unittest
from qwirkle.tile import Tile, Color, Shape


class TileTest(unittest.TestCase):
    def test_init(self):
        self.make_one_with_each()
    
    def test_string_representation(self):
        tiles = self.make_one_with_each()
        strings = [str(tile) for tile in tiles]
        expected = ['red circle',
                    'orange x',
                    'yellow diamond',
                    'green square',
                    'blue star',
                    'purple cross']
        self.assertListEqual(expected, strings)

    def make_one_with_each(self):
        result = [
            Tile(Color.RED, Shape.CIRCLE),
            Tile(Color.ORANGE, Shape.X),
            Tile(Color.YELLOW, Shape.DIAMOND),
            Tile(Color.GREEN, Shape.SQUARE),
            Tile(Color.BLUE, Shape.STAR),
            Tile(Color.PURPLE, Shape.CROSS)]
        return result
    
    def test_equal(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.X)
        self.assertEqual(tile1, tile2)
    
    def test_unequal_color(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.GREEN, Shape.X)
        self.assertNotEqual(tile1, tile2)

    def test_unequal_shape(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.STAR)
        self.assertNotEqual(tile1, tile2)

    def test_unequal_color_and_shape(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.BLUE, Shape.STAR)
        self.assertNotEqual(tile1, tile2)

    def test_set(self):
        tile1 = Tile(Color.RED, Shape.X)
        tile2 = Tile(Color.RED, Shape.X)
        s = set([tile1, tile2])
        self.assertEqual(1, len(s))
