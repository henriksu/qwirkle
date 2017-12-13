from enum import Enum


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
    
    def __eq__(self, other):
        return self.color == other.color and \
            self.shape == other.shape
            
    def __hash__(self):
        return hash(self.color) ^ hash(self.shape)
