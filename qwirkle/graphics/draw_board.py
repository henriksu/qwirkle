import xml.etree.ElementTree as ET
from qwirkle.game_logic.tile import Color, Shape
from qwirkle.graphics.example_game import make_tiles
# TODO: install lxml for better formatting of result.


COLOR_NAMES = {
    Color.RED: "red",
    Color.ORANGE: "darkorange",
    Color.YELLOW: "yellow",
    Color.GREEN: "green",
    Color.BLUE: "blue",
    Color.PURPLE: "blueviolet"}

SHAPE_NAMES = {
    Shape.CIRCLE: "circle",
    Shape.X: "x",
    Shape.DIAMOND: "diamond",
    Shape.SQUARE: "square",
    Shape.STAR: "star",
    Shape.CLOVER: "clover"}


class Board():
    def __init__(self, offset_in_frame=0.045):
        self.offset_in_frame = offset_in_frame
        self.tile_fraction_in_frame = "{:.3f}".format(1 - 2*offset_in_frame)

        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

    def make_tile_tag(self, position, tile):
        elem = ET.Element("use")
        shape_string = SHAPE_NAMES[tile.shape]
        elem.set("xlink:href", "#{}_tile".format(shape_string))
        color_string = COLOR_NAMES[tile.color]
        elem.set("style", "fill:{}".format(color_string))

        x_str = self.process_x(position)
        elem.set("x", x_str)
        y_str = self.process_y(position)
        elem.set("y", y_str)
        elem.set("width", self.tile_fraction_in_frame)
        elem.set("height", self.tile_fraction_in_frame)
        return elem

    def process_x(self, position):
        x = position.x
        self.x_max = max(self.x_max, x)
        self.x_min = min(self.x_min, x)
        return "{:.3f}".format(x + self.offset_in_frame)

    def process_y(self, position):
        y = -position.y
        self.y_max = max(self.y_max, y)
        self.y_min = min(self.y_min, y)
        return "{:.3f}".format(y + self.offset_in_frame)

    def get_view_box(self):
        return self.x_min, self.y_min, \
            (self.x_max - self.x_min + 1), (self.y_max - self.y_min + 1)


def get_tile_prototypes():
    tree = ET.parse('tiles.svg')
    root = tree.getroot()
    tile_defs = root.find('{http://www.w3.org/2000/svg}defs')
    return tile_defs


def create_svg_skeleton():
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
    svg_root = ET.Element("svg")
    svg = ET.ElementTree(svg_root)
    return svg


def populate_board(svg_root, tiles_and_positions):
    board = Board()
    for pos, tile in tiles_and_positions:
        elem = board.make_tile_tag(pos, tile)
        svg_root.append(elem)
    view_box = board.get_view_box()
    svg_root.set("viewBox", "{} {} {} {}".format(*view_box))


def make_svg(file_name, tiles_and_positions):
    svg = create_svg_skeleton()
    svg_root = svg.getroot()
    tile_defs = get_tile_prototypes()
    svg_root.append(tile_defs)
    populate_board(svg_root, tiles_and_positions)
    svg.write(file_name, encoding="UTF-8")


make_svg("test.svg", make_tiles())
