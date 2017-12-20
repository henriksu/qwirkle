import random
from qwirkle.tile import Color, Shape, Tile


class Bag():
    def __init__(self, tiles):
        self.tiles = tiles

    @classmethod
    def make_default(cls, seed=None):
        bag = []
        for color in Color:
            for shape in Shape:
                bag.extend(3 * [Tile(color, shape)])
        random.seed(seed)
        random.shuffle(bag)
        return cls(bag)

    def exchange_tiles(self, old_tiles):
        n = len(old_tiles)
        self.validate_supply(n)
        new_tiles = self.draw_tiles(n)
        self.insert(old_tiles)
        return new_tiles

    def validate_supply(self, n):
        if len(self.tiles) < n:
            # TODO: Reconsider name, the bag is not quite empty.
            raise EmptyBagError()

    def insert(self, old_tiles):
        self.tiles.extend(old_tiles)
        random.shuffle(self.tiles)

    def draw_tiles(self, number):
        # If number > len(self.tiles),
        # the remaining tiles are returned.
        result = self.tiles[:number]
        self.tiles = self.tiles[number:]
        return result


class EmptyBagError(ValueError):
    pass
