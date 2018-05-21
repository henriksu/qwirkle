import lxml.etree as etree
from qwirkle.game_logic.tile import Color, Shape
from qwirkle.graphics.example_game import make_tiles, make_moves
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
        elem = etree.Element("use")
        shape_string = SHAPE_NAMES[tile.shape]
        elem.attrib["{http://www.w3.org/1999/xlink}href"] = "#{}_tile".format(shape_string)
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
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse('tiles.svg', parser)
    root = tree.getroot()
    tile_defs = root.find('{http://www.w3.org/2000/svg}defs')
    return tile_defs


def create_svg_skeleton():
    SVG_NS = "http://www.w3.org/2000/svg"
    XLINK_NS = "http://www.w3.org/1999/xlink"
    NS_MAP = {None: SVG_NS, "xlink": XLINK_NS}
    rootName = etree.QName("svg")
#    ET.register_namespace(None, "http://www.w3.org/2000/svg")
#    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
    svg_root = etree.Element(rootName, nsmap=NS_MAP)
    svg = etree.ElementTree(svg_root)
    return svg


def populate_board(svg_root, tiles_and_positions):
    board = Board()
    for pos, tile in tiles_and_positions:
        elem = board.make_tile_tag(pos, tile)
        svg_root.append(elem)
    view_box = board.get_view_box()
    svg_root.set("viewBox", "{} {} {} {}".format(*view_box))


def populate_animated_board(svg_root, moves):
    board = Board()
    N = len(moves)
    num = 0  # slight offset at beginning.
    for move in moves:
        num += 1
        node = etree.Element("g")
        node.set("id", "move-{}".format(num))
        node.set("opacity", "0")
        for pos, tile in move:
            elem = board.make_tile_tag(pos, tile)
            node.append(elem)
        svg_root.append(node)
    dur = "0.2s"
    sek_interval = 0.7
    for i in range(N):
        animation = etree.Element("animate")
        animation.set("{http://www.w3.org/1999/xlink}href", "#move-{}".format(i+1))
        animation.set("attributeName", "opacity")
        animation.set("attributeType", "XML")
        animation.set("begin", "{:.2f}s".format(sek_interval*(i+1)))
        animation.set("dur", dur)
        animation.set("from", "0")
        animation.set("to", "1")
        animation.set("fill", "freeze")
        svg_root.append(animation)
    view_box = board.get_view_box()
    svg_root.set("viewBox", "{} {} {} {}".format(*view_box))


def make_svg(file_name, tiles_and_positions):
    svg = create_svg_skeleton()
    svg_root = svg.getroot()
    tile_defs = get_tile_prototypes()
    svg_root.append(tile_defs)
    populate_board(svg_root, tiles_and_positions)
    svg.write(file_name, encoding="UTF-8", pretty_print=True, xml_declaration=True)


def make_animated_svg(file_name, moves):
    svg = create_svg_skeleton()
    svg_root = svg.getroot()
    tile_defs = get_tile_prototypes()
    svg_root.append(tile_defs)
    populate_animated_board(svg_root, moves)
    svg.write(file_name, encoding="UTF-8", pretty_print=True, xml_declaration=True)


make_svg("test.svg", make_tiles())
make_animated_svg("test2.svg", make_moves())
