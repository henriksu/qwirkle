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
        for tile in old_tiles:
            self.tiles.remove(tile)

    def starting_score(self):
        return max(self.starting_score_color(),
                   self.starting_score_shape())

    def starting_score_color(self):
        # TODO: Check that the counting eliminates duplicates.
        # TODO: Suboptimal number of iterations.
        # Consider using bins instead.
        max_score = 0
        for color in Color:
            common = filter(lambda t: t.color == color,
                            self.tiles)
            score = len(set(common))
            max_score = max(max_score, score)
        return max_score

    def starting_score_shape(self):
        max_score = 0
        for shape in Shape:
            common = filter(lambda t: t.shape == shape,
                            self.tiles)
            score = len(set(common))
            max_score = max(max_score, score)
        return max_score


class NonMoveError(ValueError):
    pass


class MissingTileError(ValueError):
    pass
