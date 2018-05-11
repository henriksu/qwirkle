import os


def convert(square_size):
    """ square_size is the width and height of the box reserced for a tile,
    that is, it includes borders and/or "air" around the black tile.
    """
    assert isinstance(square_size, int)
    s = 6 * square_size
    pwd = os.getcwd()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.system("cd " + dir_path)
    command = "rsvg -w {}  -h {} -f png tile_map.svg tile_map_{}.png".format(
        s, s, square_size)
    os.system(command)

    os.chdir(pwd)


if __name__ == "__main__":
    convert(50)
