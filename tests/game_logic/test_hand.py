from copy import copy
import unittest
from qwirkle.game_logic.tile import Tile, Color, Shape
from qwirkle.game_logic.bag import Bag
from qwirkle.game_logic.hand import Hand, NonMoveError, MissingTileError


class TestHand(unittest.TestCase):
    def test_init(self):
        tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE),
                        Tile(Color.ORANGE, Shape.X),
                        Tile(Color.YELLOW, Shape.DIAMOND),
                        Tile(Color.GREEN, Shape.SQUARE),
                        Tile(Color.BLUE, Shape.STAR),
                        Tile(Color.PURPLE, Shape.CLOVER)]
        bag = Bag(tiles_in_bag)
        hand = Hand.init_from(bag)
        expected = set(tiles_in_bag)
        result = set(hand.tiles)
        self.assertSetEqual(expected, result)

    def test_exchange_all_tiles(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_in_hand)
        hand = Hand.init_from(bag)
        del bag
        tiles_for_bag = [Tile(Color.PURPLE, Shape.CIRCLE),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.ORANGE, Shape.DIAMOND),
                         Tile(Color.YELLOW, Shape.SQUARE),
                         Tile(Color.GREEN, Shape.STAR),
                         Tile(Color.BLUE, Shape.CLOVER), ]
        bag = Bag(tiles_for_bag)
        hand.exchange_tiles(copy(tiles_in_hand), bag)
        self.assertSetEqual(set(tiles_for_bag), set(hand.tiles))
        self.assertSetEqual(set(bag.tiles), set(tiles_in_hand))

    def test_exchange_one_tile(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_in_hand)
        hand = Hand.init_from(bag)
        del bag
        tiles_for_bag = [Tile(Color.PURPLE, Shape.CIRCLE)]
        bag = Bag(tiles_for_bag)
        hand.exchange_tiles([Tile(Color.RED, Shape.CIRCLE)], bag)
        expected_tiles_in_hand = tiles_in_hand[1:]
        expected_tiles_in_hand.append(Tile(Color.PURPLE, Shape.CIRCLE))
        self.assertSetEqual(set(expected_tiles_in_hand), set(hand.tiles))

        expected_tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE)]
        self.assertSetEqual(set(bag.tiles), set(expected_tiles_in_bag))

    def test_exchange_no_tile_raises(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_in_hand)
        hand = Hand.init_from(bag)
        del bag
        tiles_for_bag = [Tile(Color.PURPLE, Shape.CIRCLE)]
        bag = Bag(tiles_for_bag)
        with self.assertRaises(NonMoveError):
            hand.exchange_tiles([], bag)
        self.assertSetEqual(set(tiles_in_hand), set(hand.tiles))

        expected_tiles_in_bag = [Tile(Color.PURPLE, Shape.CIRCLE)]
        self.assertSetEqual(set(bag.tiles), set(expected_tiles_in_bag))

    def test_exchange_missing_tile_raises(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_in_hand)
        hand = Hand.init_from(bag)
        del bag
        tiles_for_bag = [Tile(Color.PURPLE, Shape.CIRCLE),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.ORANGE, Shape.DIAMOND),
                         Tile(Color.YELLOW, Shape.SQUARE),
                         Tile(Color.GREEN, Shape.STAR),
                         Tile(Color.BLUE, Shape.CLOVER), ]
        bag = Bag(tiles_for_bag)
        with self.assertRaises(MissingTileError):
            hand.exchange_tiles(2 * [Tile(Color.YELLOW, Shape.DIAMOND)], bag)
        self.assertSetEqual(set(tiles_in_hand), set(hand.tiles))
        self.assertSetEqual(set(bag.tiles), set(tiles_for_bag))

    def test_fill_empty_hand(self):
        tiles_for_hand = [Tile(Color.RED, Shape.CIRCLE),
                          Tile(Color.ORANGE, Shape.X),
                          Tile(Color.YELLOW, Shape.DIAMOND),
                          Tile(Color.GREEN, Shape.SQUARE),
                          Tile(Color.BLUE, Shape.STAR),
                          Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_for_hand)
        hand = Hand([])
        hand.fill_from(bag)
        self.assertEqual(len(hand.tiles), hand.CAPACITY)
        self.assertEqual(len(bag.tiles), 0)

    def test_fill_full_hand(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_in_hand)
        hand = Hand.init_from(bag)
        del bag
        tiles_for_bag = [Tile(Color.PURPLE, Shape.CIRCLE),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.ORANGE, Shape.DIAMOND),
                         Tile(Color.YELLOW, Shape.SQUARE),
                         Tile(Color.GREEN, Shape.STAR),
                         Tile(Color.BLUE, Shape.CLOVER), ]
        bag = Bag(tiles_for_bag)
        hand.fill_from(bag)
        self.assertSetEqual(set(hand.tiles), set(tiles_in_hand))
        self.assertEqual(6, len(bag.tiles))
        self.assertEqual(6, len(hand.tiles))

    def test_fill_partially_filled_hand(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND)]
        hand = Hand(tiles_in_hand)
        tiles_for_bag = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER), ]
        bag = Bag(tiles_for_bag)
        hand.fill_from(bag)
        self.assertSetEqual(set(tiles_in_hand), set(hand.tiles))
        self.assertEqual(hand.CAPACITY, len(hand.tiles))
        self.assertEqual(3, len(bag.tiles))

    def test_is_empty(self):
        hand = Hand([])
        self.assertTrue(hand.is_empty())

    def test_is_not_empty(self):
        hand = Hand([Tile(Color.RED, Shape.CIRCLE)])
        self.assertFalse(hand.is_empty())

    def test_worst_starting_score(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.DIAMOND),
                         Tile(Color.GREEN, Shape.SQUARE),
                         Tile(Color.BLUE, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(1, hand.starting_score())

    def test_best_starting_score_color(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.RED, Shape.DIAMOND),
                         Tile(Color.RED, Shape.SQUARE),
                         Tile(Color.RED, Shape.STAR),
                         Tile(Color.RED, Shape.CLOVER)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(6, hand.starting_score())

    def test_best_starting_score_shape(self):
        tiles_in_hand = [Tile(Color.RED, Shape.X),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.X),
                         Tile(Color.GREEN, Shape.X),
                         Tile(Color.BLUE, Shape.X),
                         Tile(Color.PURPLE, Shape.X)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(6, hand.starting_score())

    def test_starting_score_identical_tiles_color(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.RED, Shape.DIAMOND),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.RED, Shape.STAR),
                         Tile(Color.RED, Shape.CLOVER)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(5, hand.starting_score())

    def test_starting_score_identical_tiles_shape(self):
        tiles_in_hand = [Tile(Color.RED, Shape.X),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.X),
                         Tile(Color.GREEN, Shape.X),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.PURPLE, Shape.X)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(5, hand.starting_score())

    def test_starting_score_better_color(self):
        tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                         Tile(Color.RED, Shape.X),
                         Tile(Color.RED, Shape.DIAMOND),
                         Tile(Color.YELLOW, Shape.X),
                         Tile(Color.GREEN, Shape.STAR),
                         Tile(Color.PURPLE, Shape.CLOVER)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(3, hand.starting_score())

    def test_starting_score_better_shape(self):
        tiles_in_hand = [Tile(Color.RED, Shape.X),
                         Tile(Color.ORANGE, Shape.X),
                         Tile(Color.YELLOW, Shape.X),
                         Tile(Color.GREEN, Shape.STAR),
                         Tile(Color.RED, Shape.STAR),
                         Tile(Color.PURPLE, Shape.STAR)]
        hand = Hand(tiles_in_hand)
        self.assertEqual(3, hand.starting_score())
