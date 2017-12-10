import random

from qwirkle.tile import Tile, Color, Shape

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board():
    def __init__(self):
        self.tiles = []
    
    def is_allowed(self, tiles_and_positions):
        pass
        #return a bool
        
    def make_move(self, tiles_and_positions):
        positions = None
        if self.is_allowed(tiles_and_positions):
            score = self.score(positions)
            self.tiles.extend(tiles_and_positions)
            return score
        else:
            raise ValueError()
            # TODO: Let a level closer to GUI expect this error.
            # It is not the boards responsibility to expect clumsy players,
            # and besides if the player is an AI, the error will have to be
            # dealt with very differently.
            # TODO: Subclass ValueError. 


class Game():
    def __init__(self, players, seed=None):
        self.bag = self._make_bag(seed)
        self.board = Board()
        self.hand = players * [None]
        for player in range(players):
            self.hand[player] = self._draw_tiles(6)  # Each player starts with 6 tiles.
            
        self.current_player = 0
        # TODO: follow the rules.
        # The player that can play the most tiles, starts.
        self.none_has_finished = True

    def get_tiles(self, player):
        return self.hand[player]

    def _draw_tiles(self, number):
        # Look into how this should be done if there are not enough tiles.
        result = self.bag[:number]
        self.bag = self.bag[number:]
        return result

    def make_move(self, tiles_and_positions):
        # Check current players hand
        board_score = self.board.make_move(tiles_and_positions)
        self.fill_hand_for_player(self.current_player)
        if self.hand_is_empty(self.current_player) and self.none_has_finished:
            score = board_score + 6
            self.none_has_finished = False
        else:
            score = board_score
        self.scores[self.current_player].append(score)

    def exchange_tiles(self, tiles):
        self.validate_choice(tiles)
        new_tiles = self.exchange_tiles_in_bag(tiles)
        self.remove_old_tiles_from_hand(tiles)
        self.hand[self.current_player].extend(new_tiles)
        # Check that the required number can be drawn (not too few tiles left), or throw.
        # Draw new tiles.
        # Reinsert the old ones and shuffle.
        self.scores[self.current_player].append(0)

    def validate_choice(self, tiles):
        n = len(tiles)
        if n < 1:
            raise ValueError() # TODO: Subclass and explain that at least one tile must be changed.
        # Check the tile to loose are on the current players hand (rules says at least one must be exchanged).
    
    def remove_old_tiles_from_hand(self, old_tiles):
        hand = self.hand[self.current_player]
        for tile in old_tiles:
            hand.remove(tile)
    
    def exchange_tiles_in_bag(self, old_tiles):
        n = len(old_tiles)
        if len(self.bag) < n:
            raise ValueError # TODO: Make more specific .
        new_tiles = self._draw_tiles(n)
        self.bag.extend(old_tiles)
        random.shuffle(self.bag)
        return new_tiles