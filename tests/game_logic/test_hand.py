from copy import copy
from qwirkle.game_logic.tile import Tile, Color, Shape
from qwirkle.game_logic.bag import Bag
from qwirkle.game_logic.hand import Hand, NonMoveError, MissingTileError
import pytest


def test_init():
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
    assert expected == result


def test_exchange_all_tiles():
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
    assert set(tiles_for_bag) == set(hand.tiles)
    assert set(bag.tiles) == set(tiles_in_hand)


def test_exchange_one_tile():
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
    assert set(expected_tiles_in_hand) == set(hand.tiles)

    expected_tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE)]
    assert set(bag.tiles) == set(expected_tiles_in_bag)


def test_exchange_no_tile_raises():
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
    with pytest.raises(NonMoveError):
        hand.exchange_tiles([], bag)
    assert set(tiles_in_hand) == set(hand.tiles)

    expected_tiles_in_bag = [Tile(Color.PURPLE, Shape.CIRCLE)]
    assert set(bag.tiles) == set(expected_tiles_in_bag)


def test_exchange_missing_tile_raises():
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
    with pytest.raises(MissingTileError):
        hand.exchange_tiles(2 * [Tile(Color.YELLOW, Shape.DIAMOND)], bag)
    assert set(tiles_in_hand) == set(hand.tiles)
    assert set(bag.tiles) == set(tiles_for_bag)


def test_fill_empty_hand():
    tiles_for_hand = [Tile(Color.RED, Shape.CIRCLE),
                      Tile(Color.ORANGE, Shape.X),
                      Tile(Color.YELLOW, Shape.DIAMOND),
                      Tile(Color.GREEN, Shape.SQUARE),
                      Tile(Color.BLUE, Shape.STAR),
                      Tile(Color.PURPLE, Shape.CLOVER), ]
    bag = Bag(tiles_for_hand)
    hand = Hand([])
    hand.fill_from(bag)
    assert len(hand.tiles) == hand.CAPACITY
    assert not bag.tiles


def test_fill_full_hand():
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
    assert set(hand.tiles) == set(tiles_in_hand)
    assert len(bag.tiles) == 6
    assert len(hand.tiles) == 6


def test_fill_partially_filled_hand():
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
    assert set(tiles_in_hand) == set(hand.tiles)
    assert hand.CAPACITY == len(hand.tiles)
    assert len(bag.tiles) == 3


def test_is_empty():
    hand = Hand([])
    assert hand.is_empty()


def test_is_not_empty():
    hand = Hand([Tile(Color.RED, Shape.CIRCLE)])
    assert not hand.is_empty()


def test_worst_starting_score():
    tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                     Tile(Color.ORANGE, Shape.X),
                     Tile(Color.YELLOW, Shape.DIAMOND),
                     Tile(Color.GREEN, Shape.SQUARE),
                     Tile(Color.BLUE, Shape.STAR),
                     Tile(Color.PURPLE, Shape.CLOVER)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 1


def test_best_starting_score_color():
    tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                     Tile(Color.RED, Shape.X),
                     Tile(Color.RED, Shape.DIAMOND),
                     Tile(Color.RED, Shape.SQUARE),
                     Tile(Color.RED, Shape.STAR),
                     Tile(Color.RED, Shape.CLOVER)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 6


def test_best_starting_score_shape():
    tiles_in_hand = [Tile(Color.RED, Shape.X),
                     Tile(Color.ORANGE, Shape.X),
                     Tile(Color.YELLOW, Shape.X),
                     Tile(Color.GREEN, Shape.X),
                     Tile(Color.BLUE, Shape.X),
                     Tile(Color.PURPLE, Shape.X)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 6


def test_starting_score_identical_tiles_color():
    tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                     Tile(Color.RED, Shape.X),
                     Tile(Color.RED, Shape.DIAMOND),
                     Tile(Color.RED, Shape.X),
                     Tile(Color.RED, Shape.STAR),
                     Tile(Color.RED, Shape.CLOVER)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 5


def test_starting_score_identical_tiles_shape():
    tiles_in_hand = [Tile(Color.RED, Shape.X),
                     Tile(Color.ORANGE, Shape.X),
                     Tile(Color.YELLOW, Shape.X),
                     Tile(Color.GREEN, Shape.X),
                     Tile(Color.RED, Shape.X),
                     Tile(Color.PURPLE, Shape.X)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 5


def test_starting_score_better_color():
    tiles_in_hand = [Tile(Color.RED, Shape.CIRCLE),
                     Tile(Color.RED, Shape.X),
                     Tile(Color.RED, Shape.DIAMOND),
                     Tile(Color.YELLOW, Shape.X),
                     Tile(Color.GREEN, Shape.STAR),
                     Tile(Color.PURPLE, Shape.CLOVER)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 3


def test_starting_score_better_shape():
    tiles_in_hand = [Tile(Color.RED, Shape.X),
                     Tile(Color.ORANGE, Shape.X),
                     Tile(Color.YELLOW, Shape.X),
                     Tile(Color.GREEN, Shape.STAR),
                     Tile(Color.RED, Shape.STAR),
                     Tile(Color.PURPLE, Shape.STAR)]
    hand = Hand(tiles_in_hand)
    assert hand.starting_score() == 3
