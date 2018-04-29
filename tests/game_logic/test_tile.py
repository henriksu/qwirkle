from qwirkle.game_logic.tile import Tile, Color, Shape


def test_init():
    make_one_with_each()


def test_string_representation():
    tiles = make_one_with_each()
    strings = [str(tile) for tile in tiles]
    expected = ['red circle',
                'orange x',
                'yellow diamond',
                'green square',
                'blue star',
                'purple clover']
    assert expected == strings


def make_one_with_each():
    result = [
        Tile(Color.RED, Shape.CIRCLE),
        Tile(Color.ORANGE, Shape.X),
        Tile(Color.YELLOW, Shape.DIAMOND),
        Tile(Color.GREEN, Shape.SQUARE),
        Tile(Color.BLUE, Shape.STAR),
        Tile(Color.PURPLE, Shape.CLOVER)]
    return result


def test_equal():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.X)
    assert tile1 == tile2


def test_unequal_color():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.GREEN, Shape.X)
    assert tile1 != tile2


def test_unequal_shape():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.STAR)
    assert tile1 != tile2


def test_unequal_color_and_shape():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.BLUE, Shape.STAR)
    assert tile1 != tile2


def test_set():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.X)
    s = set([tile1, tile2])
    assert len(s) == 1
