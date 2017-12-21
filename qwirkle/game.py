import random
from qwirkle.bag import Bag
from qwirkle.hand import Hand
from qwirkle.board import Board


class Game():
    def __init__(self, players, seed=None):
        self.bag = Bag.make_default(seed)
        self.board = Board()
        self.num_players = players
        self.hand = players * [None]
        for player in range(players):
            # Each player starts with 6 tiles.
            self.hand[player] = Hand.init_from(self.bag)
        self.current_player = self.determine_starting_player()
        self.none_has_finished = True

    def determine_starting_player(self):
        starting_players = []
        max_score = 0
        for player, hand in enumerate(self.hand):
            score = hand.starting_score()
            if score > max_score:
                starting_players = []
                max_score = score
            if score == max_score:
                starting_players.append(player)

        starting_player = random.choice(starting_players)
        return starting_player

    def get_tiles(self, player):
        return self.hand[player].tiles

    def make_move(self, tiles_and_positions):
        _, tiles = zip(*tiles_and_positions)
        hand = self.hand[self.current_player]
        hand.validate_choice(tiles)
        board_score = self.board.make_move(tiles_and_positions)
        hand.fill_from(self.bag)
        score = self._compute_score(hand, board_score)
        self.scores[self.current_player].append(score)
        self._advance_player()

    def _compute_score(self, hand, board_score):
        if hand.is_empty() and self.none_has_finished:
            # TODO: oone else will have finished.
            score = board_score + 6
            self.none_has_finished = False
        else:
            score = board_score
        return score

    def exchange_tiles(self, tiles):
        self.hand[self.current_player].exchange_tiles(tiles, self.bag)
        self.scores[self.current_player].append(0)
        self._advance_player()

    def _advance_player(self):
        self.current_player = (self.current_player + 1) % self.num_players
