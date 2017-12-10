
class Bag():
    def __init__(self, tiles):
        self.tiles = tiles
        
    @classmethod
    def make_default_bag(cls, seed=None):
        bag = []
        for color in Color:
            for shape in Shape:
                bag.extend(3 * [Tile(color, shape)])
        random.seed(seed)
        random.shuffle(bag) 
        return bag