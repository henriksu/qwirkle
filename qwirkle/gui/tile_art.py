import os
import pygame
from qwirkle.game_logic.tile import Color, Shape

# These indexes HAPPENS to be the same as the ones used in the Enums.
# They are repeated here, just in case one of them changes.
COLOR_IDXS = {
    Color.RED: 0,
    Color.ORANGE: 1,
    Color.YELLOW: 2,
    Color.GREEN: 3,
    Color.BLUE: 4,
    Color.PURPLE: 5}

SHAPE_IDXS = {
    Shape.CIRCLE: 0,
    Shape.X: 1,
    Shape.DIAMOND: 2,
    Shape.SQUARE: 3,
    Shape.STAR: 4,
    Shape.CLOVER: 5}


class TileDrawer():
    def __init__(self, box_size):
        self.box_size = box_size

        pwd = os.getcwd()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.system("cd " + dir_path)
        file_name = 'tile_map_{}.png'.format(self.box_size)
        self.image = pygame.image.load(file_name)
        os.chdir(pwd)

    def get_tile_surface(self, tile):
        color_index = COLOR_IDXS[tile.color]
        shape_index = SHAPE_IDXS[tile.shape]

        x = shape_index * self.box_size
        y = color_index * self.box_size

        rect = pygame.Rect((x, y), (self.box_size, self.box_size))
        return self.image.subsurface(rect)
