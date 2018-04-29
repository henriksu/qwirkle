from qwirkle.game_logic.game import Game, Player
from qwirkle.game_logic.tile import Tile, Color, Shape
from qwirkle.game_logic.hand import Hand
from qwirkle.game_logic.board import Board, Position
from qwirkle.game_logic.bag import Bag
from tests.game_logic.test_pass_turn import MockBoard


def test_make_game():
    Game.make_new_game(num_players=2)


def test_racks():
    game = Game.make_new_game(num_players=2, seed=0)
    player_1 = game.get_tiles(player=0)
    expected = [Tile(Color.RED, Shape.X),
                Tile(Color.YELLOW, Shape.DIAMOND),
                Tile(Color.ORANGE, Shape.X),
                Tile(Color.BLUE, Shape.CIRCLE),
                Tile(Color.GREEN, Shape.CIRCLE),
                Tile(Color.PURPLE, Shape.STAR)]
    assert set(player_1) == set(expected)
    player_2 = game.get_tiles(player=1)
    expected = [Tile(Color.ORANGE, Shape.DIAMOND),
                Tile(Color.GREEN, Shape.CLOVER),
                Tile(Color.PURPLE, Shape.SQUARE),
                Tile(Color.BLUE, Shape.SQUARE),
                Tile(Color.ORANGE, Shape.SQUARE),
                Tile(Color.PURPLE, Shape.X)]
    assert set(player_2) == set(expected)


def test_normal_move():
    tiles = [Tile(Color.RED, Shape.CLOVER),
             Tile(Color.RED, Shape.DIAMOND),
             Tile(Color.GREEN, Shape.SQUARE),
             Tile(Color.PURPLE, Shape.SQUARE),
             Tile(Color.YELLOW, Shape.STAR),
             Tile(Color.PURPLE, Shape.STAR)]
    hand = Hand(tiles)
    player1 = Player(hand)
    player2 = Player([])  # TODO: Illegal
    board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
    bag = Bag([Tile(Color.GREEN, Shape.CIRCLE)])
    game = Game(bag, board, [player2, player1], player1)
    tiles_and_positions = [(Position(0, 1),
                           Tile(Color.RED, Shape.CLOVER))]
    game.make_move(tiles_and_positions)
    assert player1.total_score() == 2
    expected_tiles_on_hand = [
        Tile(Color.RED, Shape.DIAMOND),
        Tile(Color.GREEN, Shape.SQUARE),
        Tile(Color.PURPLE, Shape.SQUARE),
        Tile(Color.YELLOW, Shape.STAR),
        Tile(Color.PURPLE, Shape.STAR),
        Tile(Color.GREEN, Shape.CIRCLE)]
    assert set(expected_tiles_on_hand) == set(player1.hand.tiles)
    assert not bag.tiles
    assert player2 == game.current_player


def test_last_move():
    tiles = [Tile(Color.RED, Shape.CLOVER)]
    hand = Hand(tiles)
    player1 = Player(hand, [1, 1])
    player2 = Player([])  # TODO: Illegal state
    board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
    bag = Bag([])
    game = Game(bag, board, [player2, player1], player1)
    tiles_and_positions = [(Position(0, 1),
                           Tile(Color.RED, Shape.CLOVER))]
    game.make_move(tiles_and_positions)
    assert 2+6+2 == player1.total_score()
    expected_tiles_on_hand = []
    assert set(expected_tiles_on_hand) == set(player1.hand.tiles)
    assert not bag.tiles
    assert game.current_player is None


# TODO: DOn't allow the  very first turn to be exchanging tiles!
def test_exchange_tiles():
    tiles = [Tile(Color.RED, Shape.CIRCLE)]
    hand = Hand(tiles)
    player1 = Player(hand)
    player2 = Player([])  # TODO: Illegal state.
    bag = Bag([Tile(Color.GREEN, Shape.CLOVER)])
    board = Board([(Position(0, 0), Tile(Color.RED, Shape.DIAMOND))])
    game = Game(bag, board, [player2, player1], player1)
    tiles_to_exchange = [Tile(Color.RED, Shape.CIRCLE)]
    game.exchange_tiles(tiles_to_exchange)
    expected_hand = [Tile(Color.GREEN, Shape.CLOVER)]
    assert expected_hand == player1.hand.tiles
    expected_bag = [Tile(Color.RED, Shape.CIRCLE)]
    assert expected_bag == bag.tiles
    assert player1.total_score() == 0
    assert player2 == game.current_player


def test_pass_once():
    tiles = [Tile(Color.RED, Shape.CIRCLE)]
    hand = Hand(tiles)
    player1 = Player(hand)
    player2 = Player([])
    player3 = Player([])
    bag = Bag([])
    board = MockBoard(moves=[], possible_moves=[1, 2, 3])
    game = Game(bag, board, [player2, player3, player1], player1)
    game.pass_round()
    points = player1.total_score()
    assert points == 0
    tiles = [Tile(Color.RED, Shape.CIRCLE)]
    assert tiles == player1.hand.tiles
    assert player2 == game.current_player

# TODO: Commented out because useless after refactoring of premature ending.
#     def test_pass_and_end_game(self):
#         tiles = [Tile(Color.RED, Shape.CIRCLE)]
#         hand = Hand(tiles)
#         player1 = Player(hand)
#         player2 = Player([])
#         bag = Bag([])
#         board = MockBoard(moves=[], possible_moves=[])
#         game = Game(bag, board, [player2, player1], player1)
#         game.pass_round()
#         points = player1.total_score()
#         self.assertEqual(0, points)
#         tiles = [Tile(Color.RED, Shape.CIRCLE)]
#         self.assertListEqual(tiles, player1.hand.tiles)
#         self.assertIsNone(game.current_player)



# TODO: TEst that game ends after all have passed.
# TODO: What about the REALLY bad case that the players
# continously changes tiles. Is it wven possible?
