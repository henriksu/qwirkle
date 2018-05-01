import random
import numpy as np
from qwirkle.game_logic.board import Move
from qwirkle.game_logic.tile import Shape, Color, Tile
import itertools
from collections import defaultdict


class AI():
    # avg.: 307.51 std.: 18.18
    # avg.: 2.7952 std.: 0.13978
    def __init__(self, game):
        self.game = game

    def make_move(self):
        hand = self.game.current_player.hand
        legal_single_piece_moves = self.game.board.legal_single_piece_moves(hand)
        if legal_single_piece_moves:
            self.choose_move(legal_single_piece_moves, hand)
        else:
            self.no_allowed_moves_turn(hand)

    def no_allowed_moves_turn(self, hand):
        bag_content = len(self.game.bag.tiles)
        if bag_content > 0:
            self.do_forced_swap(hand, bag_content)
        else:
            self.game.pass_round()

    def choose_move(self, legal_single_piece_moves, hand):
        move = random.choice(list(legal_single_piece_moves))
        self.game.make_move(move.tiles_and_positions)

    def do_forced_swap(self, hand, bag_content):
        max_exchangeable = min(len(hand.tiles), bag_content)
        num_exchanging = random.randrange(1, max_exchangeable+1)
        tiles_to_swap = random.sample(hand.tiles, num_exchanging)
        self.game.exchange_tiles(tiles_to_swap)


class ExchangeAllIfExchanging(AI):
    def do_forced_swap(self, hand, bag_content):
        self.exchange_as_many_as_possible(hand, bag_content)

    def exchange_as_many_as_possible(self, hand, bag_content):
        tiles = hand.tiles
        if len(tiles) > bag_content:
            tiles_to_Swap = random.sample(tiles, bag_content)
            self.game.exchange_tiles(tiles_to_Swap)
        else:
            self.game.exchange_tiles(tiles)


class BestSingleMoveAI(ExchangeAllIfExchanging):
    # avg.: 4.82557 std.: 0.36824
    # avg.: 4.771155 std.: 0.3123
    def score_moves(self, legal_moves):
        scored_moves = {}
        for move in legal_moves:
            scored_moves[move] = move.score()
        max_score = max(scored_moves.values())
        return scored_moves, max_score

    def do_a_high_score_move(self, scored_moves, max_score):
        high_score_moves = [move for move, score in scored_moves.items() if
                            score == max_score]
        self.num_high_score = len(list(high_score_moves))
        move = random.choice(list(high_score_moves))
        self.game.make_move(move.tiles_and_positions)

    def choose_move(self, legal_single_piece_moves, hand):
        scored_moves, max_score = self.score_moves(legal_single_piece_moves)
        self.do_a_high_score_move(scored_moves, max_score)


class BestMultiMoveAI(BestSingleMoveAI):
    # avg.: 7.843 std.: 0.518 (assuming best move has most tiles)
    # avg.: 8.057 std.: 0.512 (corrected)

    def choose_move(self, legal_single_piece_moves, hand):
        legal_moves = self.game.board.legal_moves(hand)
        scored_moves, max_score = self.score_moves(legal_moves)
        self.do_a_high_score_move(scored_moves, max_score)


class SimpleProactiveExchange(BestSingleMoveAI):
    ROUNDS_TO_LOOK_BACK = 4
    UNACCEPTABLE_SCORE = 3  # By advice from a web page.
    # avg.: 4.118 std.: 0.478778 (with 4, 6)
    # avg.: 4.7151 std.: 0.351013 (with 4, 3)

    def __init__(self, game):
        self.no_proactive_swaps = 0
        super().__init__(game)

    def choose_move(self, legal_single_piece_moves, hand):
        scored_moves, max_score = self.score_moves(legal_single_piece_moves)
        # X previous scores.
        bag_content = len(self.game.bag.tiles)
        if self.should_exchange_tiles(bag_content, max_score) and bag_content:
            self.no_proactive_swaps += 1
            self.exchange_as_many_as_possible(hand, bag_content)
        else:
            self.do_a_high_score_move(scored_moves, max_score)

    def should_exchange_tiles(self, bag_content, max_score):
        last_scores = \
            self.game.current_player.scores[-self.ROUNDS_TO_LOOK_BACK:]
        last_scores.append(max_score)
        return len(last_scores) > 2 and \
            max(last_scores) <= self.UNACCEPTABLE_SCORE and \
            last_scores[-2] != 0 and bag_content > 0


class SimpleBoardBasedProactiveExchange(SimpleProactiveExchange):
    # avg.: 3.58723187918 std.: 0.502896167549
    # avg.: 3.87815292667 std.: 0.389971484227 after only considering tiles that can be drawn.
    # avg.: 4.50563448006 std.: 0.509617095829 after trying to approximate expected returns. 50 tries
    # avg.: 4.57028669443 std.: 0.458166148928 after increasing tries to 500
    # increasing to 2.5 times max score -> around 4.7.
    # avg.: 4.70551209571 std.: 0.370894895012 2.5*max_Score + 2 (results in fewer swaps)
    # avg.: 4.78300223679 std.: 0.382913973977 2.8*max_Score + 2
    # avg.: 4.82635925493 std.: 0.361110419439 2.8*max_score + 4

    def should_exchange_tiles(self, bag_content, max_score):
        if self.skipped_last():
            return False
        unseen_tiles = self.get_unseen_tiles()
        tiles_list = list(unseen_tiles.keys())  # Is list() needed?
        tile_scores = self.get_tile_scores(tiles_list)
        if not tile_scores:
            return False
        max_scores = self.get_expected_max_score(unseen_tiles, tile_scores)
        expected_max_score = np.mean(max_scores)
        return (expected_max_score > 2.8*max_score + 4)

    def get_expected_max_score(self, unseen_tiles, tile_scores):
        scores = []
        for tile, count in unseen_tiles.items():
            score_for_tile = [tile_scores[tile]]*count
            scores.extend(score_for_tile)
        # simulations
        best = []
        tiles = min(6, len(self.game.bag.tiles))
        for _ in range(500):
            hand = random.sample(scores, tiles)
            best.append(max(hand))
        return best

    def skipped_last(self):
        scores = self.game.current_player.scores
        if scores:
            return scores[-1] == 0
        else:
            return False

    def get_total_tiles(self):
        tile_types = [Tile(color, shape) for color, shape in itertools.product(Color, Shape)] # TODO: Use remaining unseen_tiles.
        total_tiles = {tile: 3 for tile in tile_types}
        return total_tiles

    def get_unseen_tiles(self):
        tiles = self.get_total_tiles()
        for _, tile in self.game.board.tiles:
            tiles[tile] -= 1
        for tile in self.game.current_player.hand.tiles:
            tiles[tile] -= 1
        return {tile: count for tile, count in tiles.items() if count > 0}

    def get_tile_scores(self, unseen_tiles):
        tile_scores = defaultdict(lambda: 0)
        adj_pos = self.game.board.adjacent_positions()
        for pos in adj_pos:
            move = Move(self.game.board, [(pos, None)])
            score = move.score()
            for tile in unseen_tiles:
                move = Move(self.game.board, [(pos, tile)])
                if move.is_allowed():
                    tile_scores[tile] = max(score, tile_scores[tile])
        return tile_scores
        
# Other possibilities:
# - Number of qwirkle-able rows/columns (strikes).
#.- Same as above, but include what unseen_tiles are still in play. Prioritize by what I have on my han.
# - highest score on next round with pieces left on hand.
# - same as above, just with expectation of pices that CAN still be drawn.
# - number of positions open for business after a move.
# - Opt to exchange unseen_tiles if bad fit for board.
# - Opt to exchange only some unseen_tiles (voluntarily keeping some).
