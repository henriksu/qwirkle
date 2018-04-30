#!/usr/bin/env python
# encoding: utf-8
import pytest
from qwirkle.game_logic.game import Board
from qwirkle.game_logic.tile import Tile, Color, Shape
from qwirkle.game_logic.board import Position


@pytest.fixture
def one_tile():
    return Tile(Color.RED, Shape.X)


def test_one_tile_in_cener(one_tile):
    board = Board()
    move = (Position(0, 0), one_tile)
    result = board.is_allowed([move])
    assert result


def test_one_tile_above_off_center(one_tile):
    board = Board()
    move = (Position(0, 1), one_tile)
    result = board.is_allowed([move])
    assert not result


def test_one_tile_right_off_center(one_tile):
    board = Board()
    move = (Position(1, 0), one_tile)
    result = board.is_allowed([move])
    assert not result


def test_one_tile_above_right_off_center(one_tile):
    board = Board()
    move = (Position(1, 1), one_tile)
    result = board.is_allowed([move])
    assert not result


def test_one_tile_belove_left_off_center(one_tile):
    board = Board()
    move = (Position(-1, -1), one_tile)
    result = board.is_allowed([move])
    assert not result


# TestTwoCompatibleTilesOnEmptyBoard
@pytest.fixture
def two_tiles():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.DIAMOND)
    return [tile1, tile2]


def test_origin_right(two_tiles):
    board = Board()
    move = [(Position(0, 0), two_tiles[0]),
            (Position(1, 0), two_tiles[1])]
    result = board.is_allowed(move)
    assert result


def test_origin_left(two_tiles):
    board = Board()
    move = [(Position(-1, 0), two_tiles[0]),
            (Position(0, 0), two_tiles[1])]
    result = board.is_allowed(move)
    assert result


def test_origin_down(two_tiles):
    board = Board()
    move = [(Position(0, 0), two_tiles[0]),
            (Position(0, -1), two_tiles[1])]
    result = board.is_allowed(move)
    assert result


def test_origin_up(two_tiles):
    board = Board()
    move = [(Position(0, 1), two_tiles[0]),
            (Position(0, 0), two_tiles[1])]
    result = board.is_allowed(move)
    assert result


def test_origin_diagonal(two_tiles):
    board = Board()
    move = [(Position(1, 1), two_tiles[0]),
            (Position(0, 0), two_tiles[1])]
    result = board.is_allowed(move)
    assert not result


# TestIncompatibleTilesOneEmptyBoard
def test_different_color_and_shape():
    board = Board()
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.GREEN, Shape.CIRCLE)
    move = [(Position(0, 0), tile1),
            (Position(0, 1), tile2)]
    result = board.is_allowed(move)
    assert not result


def test_duplicate_position():
    board = Board()
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.DIAMOND)
    move = [(Position(0, 0), tile1),
            (Position(0, 0), tile2)]
    result = board.is_allowed(move)
    assert not result


def test_non_contiguous():
    board = Board()
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.CIRCLE)
    move = [(Position(0, 0), tile1),
            (Position(0, 2), tile2)]
    result = board.is_allowed(move)
    assert not result


def test_non_contiguous2():
    board = Board()
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.CIRCLE)
    move = [(Position(0, 0), tile1),
            (Position(2, 0), tile2)]
    result = board.is_allowed(move)
    assert not result


# TestSecondMoveFromOneTile
@pytest.fixture
def one_piece_board():
    tile = Tile(Color.RED, Shape.X)
    return Board([(Position(0, 0), tile)])


def test_add_red_horizontally(one_piece_board):
    tile = Tile(Color.RED, Shape.CIRCLE)
    result = one_piece_board.is_allowed([(Position(1, 0), tile)])
    assert result


def test_add_x_horizontally(one_piece_board):
    tile = Tile(Color.GREEN, Shape.X)
    result = one_piece_board.is_allowed([(Position(1, 0), tile)])
    assert result


def test_add_red_vertically(one_piece_board):
    tile = Tile(Color.RED, Shape.CIRCLE)
    result = one_piece_board.is_allowed([(Position(0, 1), tile)])
    assert result


def test_add_x_vertically(one_piece_board):
    tile = Tile(Color.GREEN, Shape.X)
    result = one_piece_board.is_allowed([(Position(0, 1), tile)])
    assert result


def test_add_two_horizontally(one_piece_board):
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1),
                                    (Position(2, 0), tile2)])
    assert result


def test_add_two_horizontally2(one_piece_board):
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1),
                                    (Position(-1, 0), tile2)])
    assert result


def test_add_two_vertically(one_piece_board):
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(0, 1), tile1),
                                    (Position(0, 2), tile2)])
    assert result


def test_add_two_vertically2(one_piece_board):
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(0, 1), tile1),
                                    (Position(0, -1), tile2)])
    assert result


def test_add_two_in_different_direction(one_piece_board):
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(0, 1), tile1),
                                    (Position(1, 0), tile2)])
    assert not result


def test_add_one_diagonally(one_piece_board):
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    result = one_piece_board.is_allowed([(Position(1, 1), tile1)])
    assert not result


def test_add_one_illegal(one_piece_board):
    tile1 = Tile(Color.GREEN, Shape.CIRCLE)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1)])
    assert not result


def test_add_one_identical(one_piece_board):
    tile1 = Tile(Color.RED, Shape.X)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1)])
    assert not result


# TestLineSpecificIndexes
@pytest.fixture
def L_shaped_board():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.CIRCLE)
    tile3 = Tile(Color.RED, Shape.SQUARE)
    tile4 = Tile(Color.RED, Shape.CLOVER)
    tile5 = Tile(Color.GREEN, Shape.CLOVER)
    tile6 = Tile(Color.ORANGE, Shape.CLOVER)
    tile7 = Tile(Color.YELLOW, Shape.CLOVER)
    return Board([(Position(0, 0), tile1),
                  (Position(1, 0), tile2),
                  (Position(2, 0), tile3),
                  (Position(3, 0), tile4),
                  (Position(3, 1), tile5),
                  (Position(3, 2), tile6),
                  (Position(3, 3), tile7)])


def test_column_one_tile(L_shaped_board):
    tile1 = Tile(Color.YELLOW, Shape.X)
    result = L_shaped_board.is_allowed([(Position(0, 1), tile1)])
    assert result


def test_row_one_tile(L_shaped_board):
    tile1 = Tile(Color.YELLOW, Shape.X)
    result = L_shaped_board.is_allowed([(Position(2, 3), tile1)])
    assert result


def test_column_two_tiles(L_shaped_board):
    tile1 = Tile(Color.YELLOW, Shape.X)
    tile2 = Tile(Color.ORANGE, Shape.X)
    result = L_shaped_board.is_allowed([(Position(0, 1), tile1),
                                        (Position(0, 2), tile2)])
    assert result


def test_row_two_tiles(L_shaped_board):
    tile1 = Tile(Color.YELLOW, Shape.X)
    tile2 = Tile(Color.YELLOW, Shape.CIRCLE)
    result = L_shaped_board.is_allowed([(Position(2, 3), tile1),
                                        (Position(1, 3), tile2)])
    assert result


def test_legal_multi_tile_row(one_piece_board):
    tile1 = Tile(Color.RED, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1),
                                         (Position(2, 0), tile2)])
    assert result


def test_illegal_multi_tile_row2(one_piece_board):
    tile1 = Tile(Color.GREEN, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(0, 1), tile1),
                                         (Position(1, 1), tile2)])
    assert not result


def test_illegal_multi_tile_row1(one_piece_board):
    tile1 = Tile(Color.GREEN, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1),
                                         (Position(2, 0), tile2)])
    assert not result


# TestColumnStrikes
def test_legal_multi_tile_column(one_piece_board):
    tile1 = Tile(Color.RED, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(0, 1), tile1),
                                         (Position(0, 2), tile2)])
    assert result


def test_illegal_multi_tile_column2(one_piece_board):
    tile1 = Tile(Color.GREEN, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(1, 0), tile1),
                                         (Position(1, 1), tile2)])
    assert not result


def test_illegal_multi_tile_column1(one_piece_board):
    tile1 = Tile(Color.GREEN, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    result = one_piece_board.is_allowed([(Position(0, 1), tile1),
                                         (Position(0, 2), tile2)])
    assert not result


# TestColumnStrikes2
def test_illegal_multi_tile_column():
    tile1 = Tile(Color.RED, Shape.X)
    tile2 = Tile(Color.RED, Shape.CIRCLE)
    board = Board([(Position(0, 0), tile1),
                   (Position(0, 1), tile2)])
    tile1 = Tile(Color.YELLOW, Shape.X)
    tile2 = Tile(Color.YELLOW, Shape.CLOVER)
    result = board.is_allowed([(Position(1, 0), tile1),
                               (Position(1, 1), tile2)])
    assert not result


def test_valid_move():
    tile1 = Tile(Color.RED, Shape.X)
    board = Board([(Position(0, 0), tile1)])
    tile2 = Tile(Color.RED, Shape.CIRCLE)
    score = board.make_move([(Position(0, 1), tile2)])
    assert score == 2
    tiles = board.tiles
    expected = [(Position(0, 0), tile1),
                (Position(0, 1), tile2)]
    assert expected == tiles


def test_illegal_move():
    tile1 = Tile(Color.RED, Shape.X)
    board = Board([(Position(0, 0), tile1)])
    tile2 = Tile(Color.GREEN, Shape.CIRCLE)
    with pytest.raises(ValueError):
        board.make_move([(Position(0, 1), tile2)])
    tiles = board.tiles
    expected = [Position(Position(0, 0), tile1)]
    assert expected == tiles


def test_qwirkle_score():
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    tile3 = Tile(Color.RED, Shape.DIAMOND)
    tile4 = Tile(Color.RED, Shape.SQUARE)
    tile5 = Tile(Color.RED, Shape.STAR)
    tile6 = Tile(Color.RED, Shape.X)
    board = Board()
    move = [(Position(0, 0), tile1),
            (Position(1, 0), tile2),
            (Position(2, 0), tile3),
            (Position(3, 0), tile4),
            (Position(4, 0), tile5),
            (Position(5, 0), tile6)]
    score = board.make_move(move)
    assert score == 12


def testRepeatedMovePosition():
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    board = Board()
    move = [(Position(0, 0), tile1),
            (Position(0, 0), tile2)]
    result = board.is_allowed(move)
    assert not result


def testMoveOvershadowsExistingTile():
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    board = Board([(Position(0, 0), tile1),
                   (Position(0, 1), tile2)])
    tile1 = Tile(Color.RED, Shape.DIAMOND)
    tile2 = Tile(Color.RED, Shape.SQUARE)
    move = [(Position(0, 1), tile1),
            (Position(1, 1), tile2)]
    result = board.is_allowed(move)
    assert not result


def test_second_column_strike():
    tile1 = Tile(Color.RED, Shape.CIRCLE)
    tile2 = Tile(Color.RED, Shape.CLOVER)
    tile3 = Tile(Color.RED, Shape.DIAMOND)
    tile4 = Tile(Color.RED, Shape.CLOVER)
    placements = [(Position(0, 1), tile1),
                  (Position(0, 0), tile2),
                  (Position(0, -1), tile3),
                  (Position(1, -1), tile4)]
    board = Board(placements)
    tile5 = Tile(Color.RED, Shape.CLOVER)
    tile6 = Tile(Color.RED, Shape.CIRCLE)
    move = [(Position(1, 1), tile5),
            (Position(1, 2), tile6)]
    result = board.is_allowed(move)
    assert result
