from qwirkle.game_logic.tile import Color, Shape, Tile
from qwirkle.game_logic.board import Position


def make_tiles():
    pos1 = Position(0, 0)
    tile1 = Tile(Color.RED, Shape.CLOVER)
    pos2 = Position(0, -1)
    tile2 = Tile(Color.RED, Shape.DIAMOND)
    pos3 = Position(0, -2)
    tile3 = Tile(Color.RED, Shape.CIRCLE)
    pos4 = Position(0, -3)
    tile4 = Tile(Color.RED, Shape.SQUARE)
    pos5 = Position(1, -3)
    tile5 = Tile(Color.BLUE, Shape.SQUARE)
    pos6 = Position(2, -3)
    tile6 = Tile(Color.PURPLE, Shape.SQUARE)
    pos7 = Position(1, -2)
    tile7 = Tile(Color.BLUE, Shape.CIRCLE)
    pos8 = Position(-1, 0)
    tile8 = Tile(Color.GREEN, Shape.CLOVER)
    pos9 = Position(-1, -1)
    tile9 = Tile(Color.GREEN, Shape.DIAMOND)
    pos10 = Position(-1, 1)
    tile10 = Tile(Color.GREEN, Shape.STAR)
    pos11 = Position(-1, -2)
    tile11 = Tile(Color.GREEN, Shape.CIRCLE)
    pos12 = Position(3, -3)
    tile12 = Tile(Color.ORANGE, Shape.SQUARE)
    pos13 = Position(3, -4)
    tile13 = Tile(Color.RED, Shape.SQUARE)
    pos14 = Position(-3, 1)
    tile14 = Tile(Color.ORANGE, Shape.STAR)
    pos15 = Position(-2, 1)
    tile15 = Tile(Color.YELLOW, Shape.STAR)
    pos16 = Position(-3, 0)
    tile16 = Tile(Color.ORANGE, Shape.X)
    pos17 = Position(-3, -1)
    tile17 = Tile(Color.ORANGE, Shape.DIAMOND)
    pos18 = Position(-2, -1)
    tile18 = Tile(Color.YELLOW, Shape.DIAMOND)
    pos19 = Position(-2, -2)
    tile19 = Tile(Color.YELLOW, Shape.CIRCLE)
    pos20 = Position(0, 1)
    tile20 = Tile(Color.RED, Shape.STAR)
    pos21 = Position(-1, -4)
    tile21 = Tile(Color.ORANGE, Shape.X)
    pos22 = Position(0, -4)
    tile22 = Tile(Color.RED, Shape.X)
    pos23 = Position(1, -4)
    tile23 = Tile(Color.BLUE, Shape.X)
    pos24 = Position(4, -3)
    tile24 = Tile(Color.YELLOW, Shape.SQUARE)
    pos25 = Position(4, -4)
    tile25 = Tile(Color.BLUE, Shape.SQUARE)
    return [(pos1, tile1),
            (pos2, tile2),
            (pos3, tile3),
            (pos4, tile4),
            (pos5, tile5),
            (pos6, tile6),
            (pos7, tile7),
            (pos8, tile8),
            (pos9, tile9),
            (pos10, tile10),
            (pos11, tile11),
            (pos12, tile12),
            (pos13, tile13),
            (pos14, tile14),
            (pos15, tile15),
            (pos16, tile16),
            (pos17, tile17),
            (pos18, tile18),
            (pos19, tile19),
            (pos20, tile20),
            (pos21, tile21),
            (pos22, tile22),
            (pos23, tile23),
            (pos24, tile24),
            (pos25, tile25)]
