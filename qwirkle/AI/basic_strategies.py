import random


ROUNDS_TO_LOOK_BACK = 4
UNACCEPTABLE_SCORE = 3 # By advice from a web page.


class AI():
# avg.: 307.51 std.: 18.18
# avg.: 2.7952 std.: 0.13978
    def __init__(self, game):
        self.game = game

    def make_move(self):
        hand = self.game.current_player.hand
        legal_moves = self.game.board.legal_moves(hand)
        if legal_moves:
            self.choose_move(legal_moves, hand)
        else:
            self.no_allowed_moves_turn(hand)

    def no_allowed_moves_turn(self, hand):
        bag_content = len(self.game.bag.tiles)
        if bag_content > 0:
            self.do_forced_swap(hand, bag_content)
        else:
            self.game.pass_round()

    def choose_move(self, legal_moves, hand):
        move = random.choice(list(legal_moves))
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


class BestMoveAI(ExchangeAllIfExchanging):
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
        move = random.choice(list(high_score_moves))
        self.game.make_move(move.tiles_and_positions)

    def choose_move(self, legal_moves, hand):
        scored_moves, max_score = self.score_moves(legal_moves)
        self.do_a_high_score_move(scored_moves, max_score)


class BestMoveAndProactiveExchange(BestMoveAI):
# avg.: 4.118 std.: 0.478778 (with 4, 6)
# avg.: 4.7151 std.: 0.351013 (with 4, 3)
    def should_exchange_tiles(self, bag_content, max_score):
        last_scores = self.game.current_player.scores[-ROUNDS_TO_LOOK_BACK:  ]
        last_scores.append(max_score)
        return len(last_scores) > 2 and max(last_scores) <= UNACCEPTABLE_SCORE and last_scores[-2] != 0 and bag_content > 0

    def choose_move(self, legal_moves, hand):
        scored_moves, max_score = self.score_moves(legal_moves)
        # X previous scores.
        bag_content = len(self.game.bag.tiles)
        if self.should_exchange_tiles(bag_content, max_score):
            self.exchange_as_many_as_possible(hand, bag_content)
        else:
            self.do_a_high_score_move(scored_moves, max_score)


# Other possibilities:
# - Number of qwirkle-able rows/columns (strikes).
#.- Same as above, but include what tiles are still in play. Prioritize by what I have on my han.
# - highest score on next round with pieces left on hand.
# - same as above, just with expectation of pices that CAN still be drawn.
# - number of positions open for business after a move.
# - Opt to exchange tiles if bad fit for board.
# - Opt to exchange only some tiles (voluntarily keeping some).
