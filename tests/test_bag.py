import unittest
from qwirkle.tile import Tile, Color, Shape
from qwirkle.bag import Bag, EmptyBagError


class TestBag(unittest.TestCase):
    def test_init(self):
        bag = Bag.make_default()
        self.assertEqual(108, len(bag.tiles))
        tiles = bag.tiles
        self.remove_three(tiles, Tile(Color.RED, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.RED, Shape.X))
        self.remove_three(tiles, Tile(Color.RED, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.RED, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.RED, Shape.STAR))
        self.remove_three(tiles, Tile(Color.RED, Shape.CROSS))
    
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.X))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.STAR))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.CROSS))
    
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.X))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.STAR))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.CROSS))
    
        self.remove_three(tiles, Tile(Color.GREEN, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.X))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.STAR))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.CROSS))
    
        self.remove_three(tiles, Tile(Color.BLUE, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.X))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.STAR))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.CROSS))
    
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.X))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.STAR))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.CROSS))
    
        self.assertEqual(0, len(tiles))

    def remove_three(self, tiles, tile):
        tiles.remove(tile)
        tiles.remove(tile)
        tiles.remove(tile)
        
    def test_draw_zero(self):
        bag = Bag.make_default()
        tiles = bag.draw_tiles(0)
        self.assertEqual(0, len(tiles))
        
    def test_draw_one(self):
        bag = Bag.make_default(seed=0)
        result = bag.draw_tiles(1)
        expected = [Tile(Color.ORANGE, Shape.X)]
        self.assertListEqual(expected, result)
        self.assertEqual(107, len(bag.tiles))
    
    def test_draw_two(self):
        bag = Bag.make_default(seed=0)
        result = bag.draw_tiles(2)
        expected = [Tile(Color.ORANGE, Shape.X),
                    Tile(Color.PURPLE, Shape.STAR)]
        self.assertListEqual(expected, result)
        self.assertEqual(106, len(bag.tiles))
        
    def test_draw_too_many(self):
        bag = Bag.make_default()
        bag.draw_tiles(10)
        result = bag.draw_tiles(105)
        self.assertEqual(98, len(result))

    def test_insert(self):
        pass
        # length increases and inserted tiles does not
        # stay at the end (use seed to guarantee).
    
    def test_exchange_tiles(self):
        pass
        # happy path
        
    def test_cant_exchange_more_tiles_than_supply(self):
        pass
        # Test raises
        # with self.assertRaises(EmptyBagError):
        #     pass
