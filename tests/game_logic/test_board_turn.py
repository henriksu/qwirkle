import pytest
from qwirkle.game_logic.tile import Tile, Color, Shape
from qwirkle.game_logic.hand import Hand
from qwirkle.game_logic.board import Board, Position
from qwirkle.game_logic.game import Player, BoardTurn, EndOfGame
from qwirkle.game_logic.bag import Bag


def test_early_play():
    tiles = [Tile(Color.RED, Shape.CLOVER),
             Tile(Color.RED, Shape.DIAMOND),
             Tile(Color.GREEN, Shape.SQUARE),
             Tile(Color.PURPLE, Shape.SQUARE),
             Tile(Color.YELLOW, Shape.STAR),
             Tile(Color.PURPLE, Shape.STAR)]
    hand = Hand(tiles)
    player = Player(hand)
    board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
    bag = Bag([Tile(Color.GREEN, Shape.CIRCLE)])
    tiles_and_positions = [(Position(0, 1),
                           Tile(Color.RED, Shape.CLOVER))]
    turn = BoardTurn(board, player, bag, tiles_and_positions)
    turn.execute()
    assert player.total_score() == 2
    expected_tiles_on_hand = [
        Tile(Color.RED, Shape.DIAMOND),
        Tile(Color.GREEN, Shape.SQUARE),
        Tile(Color.PURPLE, Shape.SQUARE),
        Tile(Color.YELLOW, Shape.STAR),
        Tile(Color.PURPLE, Shape.STAR),
        Tile(Color.GREEN, Shape.CIRCLE)]
    assert set(expected_tiles_on_hand) == set(player.hand.tiles)
    assert not bag.tiles


def test_late_play():
    tiles = [Tile(Color.RED, Shape.CLOVER),
             Tile(Color.RED, Shape.DIAMOND)]
    hand = Hand(tiles)
    player = Player(hand)
    board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
    bag = Bag([])
    tiles_and_positions = [(Position(0, 1),
                           Tile(Color.RED, Shape.CLOVER))]
    turn = BoardTurn(board, player, bag, tiles_and_positions)
    turn.execute()
    assert player.total_score() == 2
    expected_tiles_on_hand = [
        Tile(Color.RED, Shape.DIAMOND)]
    assert set(expected_tiles_on_hand) == set(player.hand.tiles)
    assert not bag.tiles


def test_last_play():
    tiles = [Tile(Color.RED, Shape.CLOVER)]
    hand = Hand(tiles)
    player = Player(hand, [1, 1])
    board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
    bag = Bag([])
    tiles_and_positions = [(Position(0, 1),
                           Tile(Color.RED, Shape.CLOVER))]
    turn = BoardTurn(board, player, bag, tiles_and_positions)
    with pytest.raises(EndOfGame):
        turn.execute()
    assert player.total_score() == 2+6+2
    expected_tiles_on_hand = []
    assert set(expected_tiles_on_hand) == set(player.hand.tiles)
    assert not bag.tiles
