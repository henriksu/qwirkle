from qwirkle.game_logic.board import Position


def test_neighbours():
    pos = Position(0, 0)
    neighbours = pos.neighbour_positions()
    expected = set([Position(1, 0),
                    Position(-1, 0),
                    Position(0, 1),
                    Position(0, -1)])
    assert expected == set(neighbours)
