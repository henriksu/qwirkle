from copy import copy
from qwirkle.tile import Color, Shape


class Hand():
    CAPACITY = 6

    def __init__(self, tiles):
        self.tiles = tiles

    @classmethod
    def init_from(cls, bag):
        tiles = bag.draw_tiles(cls.CAPACITY)
        return cls(tiles)

    def exchange_tiles(self, tiles, bag):
        # TODO: Consider 'exchange' -> 'swap'
        self.validate_choice(tiles)
        new_tiles = bag.exchange_tiles(tiles)
        self.remove_old_tiles_from_hand(tiles)
        self.tiles.extend(new_tiles)

    def validate_choice(self, chosen_tiles):
        n = len(chosen_tiles)
        if n == 0:
            # TODO. SHould this be moved elsewhere?
            raise NonMoveError('A move without any tile was attempted.')
        tmp = copy(self.tiles)
        try:
            for tile in chosen_tiles:
                tmp.remove(tile)
        except ValueError:
            raise MissingTileError('A player can only use tiles on his hand.')
            # TODO: List the illegal tiles in error message.
            # TODO: Consider proper algorithm for checking
            # multiset subsetness.

    def fill_from(self, bag):
        n = self.CAPACITY - len(self.tiles)
        new_tiles = bag.draw_tiles(n)
        self.tiles.extend(new_tiles)

    def is_empty(self):
        return len(self.tiles) == 0

    def remove_old_tiles_from_hand(self, old_tiles):
        old_tiles = copy(old_tiles)
        for tile in old_tiles:
            self.tiles.remove(tile)

    def starting_score(self):
        return max(self.starting_score_color(),
                   self.starting_score_shape())

    def starting_score_color(self):
        # TODO: Check that the counting eliminates duplicates.
        # TODO: Suboptimal number of iterations.
        # Consider using bins instead.
        scores = map(self.color_score, Color)
        return max(scores)

    def color_score(self, color):
        common = filter(lambda t: t.color == color, self.tiles)
        return len(set(common))

    def starting_score_shape(self):
        scores = map(self.shape_score, Shape)
        return max(scores)

    def shape_score(self, shape):
        common = filter(lambda t: t.shape == shape, self.tiles)
        return len(set(common))


class NonMoveError(ValueError):
    pass


class MissingTileError(ValueError):
    pass
