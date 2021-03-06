from collections import namedtuple
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    PURPLE = auto()


class Shape(Enum):
    CIRCLE = auto()
    X = auto()
    DIAMOND = auto()
    SQUARE = auto()
    STAR = auto()
    CLOVER = auto()


class Tile(namedtuple('Tile', 'color shape')):
    def __str__(self):
        color = self.color.name.lower()
        shape = self.shape.name.lower()
        return ' '.join([color, shape])

    @classmethod
    def set_of_all_tiles(cls):
        tiles = set()
        for color in Color:
            for shape in Shape:
                tiles.add(cls(color, shape))
        return tiles

