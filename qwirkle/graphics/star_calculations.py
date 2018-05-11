from math import pi, cos, sin
# TODO: Write tests.
# TODO: Refactor


def angle_interval(points):
    return 2*pi/points


def get_crest_angles(points):
    interval = angle_interval(points)
    return [i*interval for i in range(points)]


def get_trough_angles(points):
    interval = angle_interval(points)
    return [interval*(1/2+i) for i in range(points)]


def get_crest_and_though_angles(points, fraction, radius, offset):
    crest_angles = get_crest_angles(points)
    crest_polar_points = [(radius, theta) for theta in crest_angles]

    through_angles = get_trough_angles(points)
    inner_radius = fraction * radius
    through_polar_points = [(inner_radius, theta) for theta in through_angles]

    star_points = []
    for crest, through in zip(crest_polar_points, through_polar_points):
        star_points.append(crest)
        star_points.append(through)

    cartsian_star_points = [(r*cos(theta), r*sin(theta)) for r, theta in star_points]
    # TODO: Transfor to Cartesian

    result = [(x + offset, y + offset) for x, y in cartsian_star_points]
    return result


if __name__ == "__main__":
    result = get_crest_and_though_angles(8, 1/2.5, 460, 500)
    for x, y in result:
        print(str(x)+ " " + str(y) + ",")
