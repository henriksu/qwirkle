import unittest
from qwirkle.tile import Tile, Color, Shape
from qwirkle.bag import Bag, EmptyBagError
import random


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
        self.remove_three(tiles, Tile(Color.RED, Shape.CLOVER))

        self.remove_three(tiles, Tile(Color.ORANGE, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.X))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.STAR))
        self.remove_three(tiles, Tile(Color.ORANGE, Shape.CLOVER))

        self.remove_three(tiles, Tile(Color.YELLOW, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.X))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.STAR))
        self.remove_three(tiles, Tile(Color.YELLOW, Shape.CLOVER))

        self.remove_three(tiles, Tile(Color.GREEN, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.X))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.STAR))
        self.remove_three(tiles, Tile(Color.GREEN, Shape.CLOVER))

        self.remove_three(tiles, Tile(Color.BLUE, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.X))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.STAR))
        self.remove_three(tiles, Tile(Color.BLUE, Shape.CLOVER))

        self.remove_three(tiles, Tile(Color.PURPLE, Shape.CIRCLE))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.X))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.DIAMOND))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.SQUARE))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.STAR))
        self.remove_three(tiles, Tile(Color.PURPLE, Shape.CLOVER))

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
        random.seed(0)
        tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE),
                        Tile(Color.RED, Shape.CIRCLE),
                        ]
        bag = Bag(tiles_in_bag)
        tile = Tile(Color.RED, Shape.X)
        self.assertEqual(2, len(bag.tiles))
        bag.insert([tile])
        self.assertEqual(3, len(bag.tiles))
        self.assertNotEqual(bag.tiles[-1], tile)

    def test_exchange_tile(self):
        tiles_in_bag = [Tile(Color.RED, Shape.STAR)]
        bag = Bag(tiles_in_bag)
        tile = Tile(Color.RED, Shape.X)
        self.assertEqual(1, len(bag.tiles))
        returned_tile = bag.exchange_tiles([tile])
        self.assertEqual(1, len(bag.tiles))
        self.assertEqual(bag.tiles[-1], tile)
        self.assertEqual(1, len(returned_tile))
        self.assertEqual(Tile(Color.RED, Shape.STAR),
                         returned_tile[0])

    def test_exchange_tiles(self):
        random.seed(0)
        tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE),
                        Tile(Color.RED, Shape.CLOVER),
                        Tile(Color.RED, Shape.DIAMOND),
                        Tile(Color.RED, Shape.SQUARE),
                        Tile(Color.RED, Shape.STAR),
                        ]
        bag = Bag(tiles_in_bag)
        tile = Tile(Color.RED, Shape.X)
        self.assertEqual(5, len(bag.tiles))
        returned_tile = bag.exchange_tiles([tile])
        self.assertEqual(5, len(bag.tiles))
        self.assertNotEqual(bag.tiles[-1], tile)
        self.assertEqual(1, len(returned_tile))
        self.assertEqual(Tile(Color.RED, Shape.CIRCLE),
                         returned_tile[0])

    def test_cant_exchange_more_tiles_than_supply(self):
        random.seed(0)
        tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE),
                        Tile(Color.RED, Shape.CLOVER),
                        ]
        bag = Bag(tiles_in_bag)
        tiles = [
            Tile(Color.RED, Shape.DIAMOND),
            Tile(Color.RED, Shape.SQUARE),
            Tile(Color.RED, Shape.STAR),
        ]
        self.assertEqual(2, len(bag.tiles))
        with self.assertRaises(EmptyBagError):
            bag.exchange_tiles(tiles)
        self.assertEqual(2, len(bag.tiles))
        self.assertListEqual(bag.tiles, tiles_in_bag)
