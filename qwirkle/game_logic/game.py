import math
import random
from qwirkle.game_logic.bag import Bag
from qwirkle.game_logic.hand import Hand
from qwirkle.game_logic.board import Board


class Player():
    def __init__(self, hand, scores=None):
        self.hand = hand
        if scores is not None:
            self.scores = scores
        else:
            self.scores = []

    def total_score(self):
        return sum(self.scores)

    def no_score_turn(self):
        self.scores.append(0)

    def score(self, points):
        self.scores.append(points)

    @classmethod
    def init_from(cls, bag):
        hand = Hand.init_from(bag)
        return cls(hand)


class Game():
    def __init__(self, bag, board, players, current_player):
        self.bag = bag
        self.board = board
        self.players = players
        self.num_players = len(players)
        self.set_current_player(current_player)

    @classmethod
    def make_new_game(cls, num_players, seed=None):
        bag = Bag.make_default(seed)
        board = Board()
        players = []
        for _ in range(num_players):
            players.append(Player.init_from(bag))
        starting_player = cls.determine_starting_player(players)
        return cls(bag, board, players, starting_player)

    def get_tiles(self, player):
        return self.players[player].hand.tiles

    @staticmethod
    def determine_starting_player(players):
        starting_players = []
        max_score = -math.inf
        for player in players:
            score = player.hand.starting_score()
            if score > max_score:
                starting_players = []
                max_score = score
            if score == max_score:
                starting_players.append(player)

        starting_player = random.choice(starting_players)
        return starting_player

    def make_move(self, tiles_and_positions):
        turn = BoardTurn(self.board, self.current_player,
                         self.bag, tiles_and_positions)
        try:
            turn.execute()
        except EndOfGame:
            self.end_game()
        else:
            self._advance_player()

    def exchange_tiles(self, tiles):
        turn = ExchangeTilesTurn(self.current_player, self.bag, tiles)
        turn.execute()
        self._advance_player()
        if len(self.board.legal_positions_with_exhaustion()) == 0:
            print('End by stalemate')
            self.end_game()

    def pass_round(self):
        turn = PassTurn(self.current_player,
                        self.bag, self.board)
        turn.execute()
        self._advance_player()
        if len(self.board.legal_positions_with_exhaustion()) == 0:
            print('End by stalemate')
            self.end_game()

    def end_game(self):
        self.current_player = None
        self._current_player = None
        # TODO: Consider end of iteration.

    def _advance_player(self):
        self._current_player = (self._current_player + 1) % self.num_players
        self.current_player = self.players[self._current_player]

    def set_current_player(self, player):
        self._current_player = self.players.index(player)
        self.current_player = player


class BoardTurn():
    def __init__(self, board, player, bag, tiles_and_positions):
        self.board = board
        self.player = player
        self.bag = bag
        self.tiles_and_positions = tiles_and_positions

    def execute(self):
        _, tiles = zip(*self.tiles_and_positions)
        hand = self.player.hand
        hand.validate_choice(tiles)
        board_score = self.board.make_move(self.tiles_and_positions)
        hand.remove_old_tiles_from_hand(tiles)
        hand.fill_from(self.bag)
        self.file_score(board_score)

    def file_score(self, board_score):
        if self.player.hand.is_empty():
            score = board_score + 6
            self.player.score(score)
            raise EndOfGame()
        else:
            self.player.score(board_score)


class ExchangeTilesTurn():
    def __init__(self, player, bag, tiles):
        self.player = player
        self.bag = bag
        self.tiles = tiles

    def execute(self):
        self.player.hand.exchange_tiles(self.tiles, self.bag)
        self.player.no_score_turn()


class EndOfGame(Exception):
    pass


class PassTurn():
    def __init__(self, player, bag, board):
        self.player = player
        self.bag = bag
        self.board = board

    def execute(self):
        if self.cannot_move():
            self.player.no_score_turn()
        else:
            raise IllegalPass()

    def cannot_move(self):
        return self.bag.is_empty() and len(self.board.legal_single_piece_moves(self.player.hand)) == 0


class IllegalPass(ValueError):
    pass
