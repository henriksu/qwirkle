import math
import pygame
from pygame import gfxdraw
from qwirkle.game_logic.tile import Color, Shape
from qwirkle.gui.color_palette import *

TILE_COLOR_CODE = {
    Color.RED: RED,
    Color.ORANGE: ORANGE,
    Color.YELLOW: YELLOW,
    Color.GREEN: GREEN,
    Color.BLUE: BLUE,
    Color.PURPLE: PURPLE}


class TileDrawer():
    def __init__(self, box_size):
        self.box_size = box_size

    def get_tile_surface(self, tile):
        color_code = TILE_COLOR_CODE[tile.color]
        shape_code = tile.shape

        tile_surface = pygame.Surface((self.box_size,self.box_size))
        pygame.draw.rect(tile_surface,BLACK, (0, 0, self.box_size, self.box_size))

        shapex = self.box_size/4
        shapey = self.box_size/4
        shapeSize = self.box_size/2

        if shape_code == Shape.CIRCLE:
            gfxdraw.aacircle(tile_surface, int(self.box_size/2), int(self.box_size/2), int(self.box_size/2.7),color_code)
            gfxdraw.filled_circle(tile_surface, int(self.box_size/2), int(self.box_size/2), int(self.box_size/2.7),color_code)
        elif shape_code == Shape.X:
            num_points = 4
            point_list = []
            center_x = self.box_size/2
            center_y = self.box_size/2
            for i in range(num_points * 2):
                    radius = self.box_size/1.8
                    if i % 2 == 0:
                            radius = radius / 3.2
                    ang = i * 3.14159 / num_points #+ 10 * 3.14159 / 60
                    x = center_x + int(math.cos(ang) * radius)
                    y = center_y + int(math.sin(ang) * radius)
                    point_list.append((x, y))
            gfxdraw.aapolygon(tile_surface, point_list, color_code)
            gfxdraw.filled_polygon(tile_surface, point_list, color_code)
    
    
    #        pygame.draw.line(DISPLAYSURF, color_code, (shapex, shapey), (shapex + shapeSize, shapey + shapeSize), 5)
    #        pygame.draw.line(DISPLAYSURF, color_code, (shapex, shapey + shapeSize), (shapex + shapeSize, shapey), 5)
    
        elif shape_code == Shape.DIAMOND:
            gfxdraw.aapolygon(tile_surface, ((shapex, shapey + self.box_size/4),
                                            (shapex + self.box_size/4, shapey),
                                            (shapex + self.box_size/2, shapey + self.box_size/4),
                                            (shapex + self.box_size/4, shapey + self.box_size/2)),
                                            color_code)
            gfxdraw.filled_polygon(tile_surface, ((shapex, shapey + self.box_size/4),
                                            (shapex + self.box_size/4, shapey),
                                            (shapex + self.box_size/2, shapey + self.box_size/4),
                                            (shapex + self.box_size/4, shapey + self.box_size/2)),
                                            color_code)
    
        elif shape_code == Shape.SQUARE:
            pygame.draw.rect(tile_surface,color_code, (shapex, shapey, shapeSize*1.15, shapeSize*1.15))
    
        elif shape_code == Shape.STAR:
            num_points = 8
            point_list = []
            center_x = self.box_size/2
            center_y = self.box_size/2
            for i in range(num_points * 2):
                    radius = self.box_size/2.5
                    if i % 2 == 1:
                            radius = radius / 2.5
                    ang = i * 3.14159 / num_points #+ 10 * 3.14159 / 60
                    x = center_x + int(math.cos(ang) * radius)
                    y = center_y + int(math.sin(ang) * radius)
                    point_list.append((x, y))
            gfxdraw.aapolygon(tile_surface, point_list, color_code)
            gfxdraw.filled_polygon(tile_surface, point_list, color_code)
    
        elif shape_code == Shape.CLOVER:
            gfxdraw.aacircle(tile_surface, int(shapex), int(shapey + self.box_size/4), int(self.box_size/6), color_code)
            gfxdraw.filled_circle(tile_surface, int(shapex), int(shapey + self.box_size/4), int(self.box_size/6), color_code)
    
            gfxdraw.aacircle(tile_surface, int(shapex + self.box_size/4), int(shapey), int(self.box_size/6), color_code)
            gfxdraw.filled_circle(tile_surface, int(shapex + self.box_size/4), int(shapey), int(self.box_size/6), color_code)
    
            gfxdraw.aacircle(tile_surface, int(shapex + self.box_size/2), int(shapey + self.box_size/4), int(self.box_size/6), color_code)
            gfxdraw.filled_circle(tile_surface, int(shapex + self.box_size/2), int(shapey + self.box_size/4), int(self.box_size/6), color_code)
    
            gfxdraw.aacircle(tile_surface, int(shapex + self.box_size/4), int(shapey + self.box_size/2), int(self.box_size/6), color_code)
            gfxdraw.filled_circle(tile_surface, int(shapex + self.box_size/4), int(shapey + self.box_size/2), int(self.box_size/6), color_code)
    
            gfxdraw.aacircle(tile_surface, int(shapex + self.box_size/4), int(shapey + self.box_size/4), int(self.box_size/6),color_code)
            gfxdraw.filled_circle(tile_surface, int(shapex + self.box_size/4), int(shapey + self.box_size/4), int(self.box_size/6),color_code)
        return tile_surface
