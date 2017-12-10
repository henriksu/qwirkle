from enum import Enum
import random

class Color(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    PURPLE = 6


class Shape(Enum):
    CIRCLE = 1
    X = 2
    DIAMOND = 3
    SQUARE = 4
    STAR = 5
    CROSS = 6


class Tile():
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape

    def __str__(self):
        color = self.color.name.lower()
        shape = self.shape.name.lower()
        return ' '.join([color, shape])



class Board():
    def __init__(self):
        pass

class Game():
    def __init__(self, players, seed=None):
       self.bag = self._make_bag(seed)
       self.hand = players * [None]
       for player in range(players):
           self.hand[player] = self._draw_tiles(6)  # Each player starts with 6 tiles.

    def get_tiles(self, player):
        return self.hand[player]

    def _make_bag(self, seed):
        bag = []
        for color in Color:
            for shape in Shape:
                bag.extend(3 * [Tile(color, shape)])
        random.seed(seed)
        random.shuffle(bag) 
        return bag

    def _draw_tiles(self, number):
        # Look into how this should be done if there are not enough tiles.
        result = self.bag[:number]
        self.bag = self.bag[number:]
        return result

    def turn(self, moves):
        pass
        # Check if move or exchange ad dispatch correspiondingly. 
        #
        #

    def make_move(self, tiles):
        # Check current players hand
        # Check that the move is allowed.
        # Calculate points.
        # Draw new tiles.
        # Check if hand is empty and give bonus if first player doing this.
        # Add points to score board.
        pass

    def exchange_tiles(self, tiles):
        # Check the tile to loose are on the current players hand (rules says at least one must be exchanged).
        # Check that the required number can be drawn (not too few tiles left), or throw.
        # Draw new tiles.
        # Reinsert the old ones and shuffle.
        pass

