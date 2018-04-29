from qwirkle.game_logic.tile import Tile, Shape, Color
from qwirkle.game_logic.game import Player, ExchangeTilesTurn
from qwirkle.game_logic.hand import Hand
from qwirkle.game_logic.bag import Bag


def test_exchanging_one_of_one():
    tiles = [Tile(Color.RED, Shape.CIRCLE)]
    hand = Hand(tiles)
    player = Player(hand)
    bag = Bag([Tile(Color.GREEN, Shape.CLOVER)])
    tiles_to_exchange = [Tile(Color.RED, Shape.CIRCLE)]
    turn = ExchangeTilesTurn(player, bag, tiles_to_exchange)
    turn.execute()
    expected_hand = [Tile(Color.GREEN, Shape.CLOVER)]
    assert expected_hand == player.hand.tiles
    expected_bag = [Tile(Color.RED, Shape.CIRCLE)]
    assert expected_bag == bag.tiles
    assert player.total_score() == 0
