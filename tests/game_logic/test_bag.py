import random
import pytest
from qwirkle.game_logic.tile import Tile, Color, Shape
from qwirkle.game_logic.bag import Bag, EmptyBagError


def test_init():
    bag = Bag.make_default()
    assert len(bag.tiles) == 108
    tiles = bag.tiles
    remove_three(tiles, Tile(Color.RED, Shape.CIRCLE))
    remove_three(tiles, Tile(Color.RED, Shape.X))
    remove_three(tiles, Tile(Color.RED, Shape.DIAMOND))
    remove_three(tiles, Tile(Color.RED, Shape.SQUARE))
    remove_three(tiles, Tile(Color.RED, Shape.STAR))
    remove_three(tiles, Tile(Color.RED, Shape.CLOVER))

    remove_three(tiles, Tile(Color.ORANGE, Shape.CIRCLE))
    remove_three(tiles, Tile(Color.ORANGE, Shape.X))
    remove_three(tiles, Tile(Color.ORANGE, Shape.DIAMOND))
    remove_three(tiles, Tile(Color.ORANGE, Shape.SQUARE))
    remove_three(tiles, Tile(Color.ORANGE, Shape.STAR))
    remove_three(tiles, Tile(Color.ORANGE, Shape.CLOVER))

    remove_three(tiles, Tile(Color.YELLOW, Shape.CIRCLE))
    remove_three(tiles, Tile(Color.YELLOW, Shape.X))
    remove_three(tiles, Tile(Color.YELLOW, Shape.DIAMOND))
    remove_three(tiles, Tile(Color.YELLOW, Shape.SQUARE))
    remove_three(tiles, Tile(Color.YELLOW, Shape.STAR))
    remove_three(tiles, Tile(Color.YELLOW, Shape.CLOVER))

    remove_three(tiles, Tile(Color.GREEN, Shape.CIRCLE))
    remove_three(tiles, Tile(Color.GREEN, Shape.X))
    remove_three(tiles, Tile(Color.GREEN, Shape.DIAMOND))
    remove_three(tiles, Tile(Color.GREEN, Shape.SQUARE))
    remove_three(tiles, Tile(Color.GREEN, Shape.STAR))
    remove_three(tiles, Tile(Color.GREEN, Shape.CLOVER))

    remove_three(tiles, Tile(Color.BLUE, Shape.CIRCLE))
    remove_three(tiles, Tile(Color.BLUE, Shape.X))
    remove_three(tiles, Tile(Color.BLUE, Shape.DIAMOND))
    remove_three(tiles, Tile(Color.BLUE, Shape.SQUARE))
    remove_three(tiles, Tile(Color.BLUE, Shape.STAR))
    remove_three(tiles, Tile(Color.BLUE, Shape.CLOVER))

    remove_three(tiles, Tile(Color.PURPLE, Shape.CIRCLE))
    remove_three(tiles, Tile(Color.PURPLE, Shape.X))
    remove_three(tiles, Tile(Color.PURPLE, Shape.DIAMOND))
    remove_three(tiles, Tile(Color.PURPLE, Shape.SQUARE))
    remove_three(tiles, Tile(Color.PURPLE, Shape.STAR))
    remove_three(tiles, Tile(Color.PURPLE, Shape.CLOVER))

    assert not tiles


def remove_three(tiles, tile):
    tiles.remove(tile)
    tiles.remove(tile)
    tiles.remove(tile)


def test_draw_zero():
    bag = Bag.make_default()
    tiles = bag.draw_tiles(0)
    assert not tiles


def test_draw_one():
    bag = Bag.make_default(seed=0)
    result = bag.draw_tiles(1)
    expected = [Tile(Color.ORANGE, Shape.X)]
    assert expected == result
    assert len(bag.tiles) == 107


def test_draw_two():
    bag = Bag.make_default(seed=0)
    result = bag.draw_tiles(2)
    expected = [Tile(Color.ORANGE, Shape.X),
                Tile(Color.PURPLE, Shape.STAR)]
    assert expected == result
    assert len(bag.tiles) == 106


def test_draw_too_many():
    bag = Bag.make_default()
    bag.draw_tiles(10)
    result = bag.draw_tiles(105)
    assert len(result) == 98


def test_insert():
    random.seed(0)
    tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE),
                    Tile(Color.RED, Shape.CIRCLE),
                    ]
    bag = Bag(tiles_in_bag)
    tile = Tile(Color.RED, Shape.X)
    assert len(bag.tiles) == 2
    bag.insert([tile])
    assert len(bag.tiles) == 3
    assert bag.tiles[-1] != tile


def test_exchange_tile():
    tiles_in_bag = [Tile(Color.RED, Shape.STAR)]
    bag = Bag(tiles_in_bag)
    tile = Tile(Color.RED, Shape.X)
    assert len(bag.tiles) == 1
    returned_tile = bag.exchange_tiles([tile])
    assert len(bag.tiles) == 1
    assert bag.tiles[-1] == tile
    assert len(returned_tile) == 1
    assert Tile(Color.RED, Shape.STAR) == returned_tile[0]


def test_exchange_tiles():
    random.seed(0)
    tiles_in_bag = [Tile(Color.RED, Shape.CIRCLE),
                    Tile(Color.RED, Shape.CLOVER),
                    Tile(Color.RED, Shape.DIAMOND),
                    Tile(Color.RED, Shape.SQUARE),
                    Tile(Color.RED, Shape.STAR),
                    ]
    bag = Bag(tiles_in_bag)
    tile = Tile(Color.RED, Shape.X)
    assert len(bag.tiles) == 5
    returned_tile = bag.exchange_tiles([tile])
    assert len(bag.tiles) == 5
    assert bag.tiles[-1] != tile
    assert len(returned_tile) == 1
    assert Tile(Color.RED, Shape.CIRCLE) == returned_tile[0]


def test_cant_exchange_more_tiles_than_supply():
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
    assert len(bag.tiles) == 2
    with pytest.raises(EmptyBagError):
        bag.exchange_tiles(tiles)
    assert len(bag.tiles) == 2
    assert bag.tiles == tiles_in_bag


def test_is_empty():
    bag = Bag([])
    result = bag.is_empty()
    assert result


def test_is_not_empty():
    bag = Bag.make_default()
    result = bag.is_empty()
    assert not result
