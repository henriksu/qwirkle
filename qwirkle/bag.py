import copy
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
        return bag

    def exchange_tiles(self, old_tiles):
        n = len(old_tiles)
        self.validate_supply(n)
        new_tiles = self._draw_tiles(n)
        self.insert(old_tiles)
        return new_tiles

    def validate_supply(self, n):
        if len(self.tiles) < n:
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


class Hand():
    CAPACITY = 6

    def __init__(self, tiles):
        self.tiles = tiles
    
    @classmethod
    def init_from(cls, bag):
        tiles = bag.draw_tiles(cls.CAPASITY)
        return cls(tiles)
    
    def exchange_tiles(self, tiles, bag):
        self.validate_choice(tiles)
        new_tiles = bag.exchange_tiles(tiles)
        self._remove_old_tiles_from_hand(tiles)
        self.tiles.extend(new_tiles)

    def validate_choice(self, chosen_tiles):
        n = len(chosen_tiles)
        if n == 0:
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

    def _remove_old_tiles_from_hand(self, old_tiles):
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


class EmptyBagError(ValueError):
    pass


class NonMoveError(ValueError):
    pass


class MissingTileError(ValueError):
    pass
