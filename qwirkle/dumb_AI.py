from qwirkle.game import Game
import random
import numpy as np

ROUNDS_TO_LOOK_BACK = 4
UNACCEPTABLE_SCORE = 3 # By advice from a web page.


def run_single_player_AI():
# avg.: 307.51 std.: 18.18
    game = Game.make_new_game(num_players=1)
    board = game.board
    while game.current_player is not None:
        hand = game.current_player.hand
        legal_moves = board.legal_moves(hand)
        if legal_moves:
            move = random.choice(list(legal_moves))
            game.make_move(move.tiles_and_positions)
        else:
            bag_content = len(game.bag.tiles)
            if bag_content > 0:
                tiles = hand.tiles
                if len(tiles) > bag_content:
                    tiles_to_Swap = random.sample(tiles, bag_content)
                    game.exchange_tiles(tiles_to_Swap)
                else:
                    game.exchange_tiles(tiles)
            else:
                game.pass_round()
    return game


def run_single_player_AI_2():
# avg.: 4.82557 std.: 0.36824
    game = Game.make_new_game(num_players=1)
    board = game.board
    while game.current_player is not None:
        hand = game.current_player.hand
        legal_moves = board.legal_moves(hand)
        if legal_moves:
            scored_moves = {}
            for move in legal_moves:
                scored_moves[move] = move.score()
            max_score = max(scored_moves.values())
            high_score_moves = [move for move, score in scored_moves.items() if
                                score == max_score]
            move = random.choice(list(high_score_moves))
            game.make_move(move.tiles_and_positions)
        else:
            bag_content = len(game.bag.tiles)
            if bag_content > 0:
                tiles = hand.tiles
                if len(tiles) > bag_content:
                    tiles_to_Swap = random.sample(tiles, bag_content)
                    game.exchange_tiles(tiles_to_Swap)
                else:
                    game.exchange_tiles(tiles)
            else:
                game.pass_round()
    return game


def run_single_player_AI_3():
# avg.: 4.118 std.: 0.478778 (with 4, 6)
    game = Game.make_new_game(num_players=1)
    board = game.board
    while game.current_player is not None:
        hand = game.current_player.hand
        legal_moves = board.legal_moves(hand)
        if legal_moves:
            scored_moves = {}
            for move in legal_moves:
                scored_moves[move] = move.score()
            max_score = max(scored_moves.values())
            # X previous scores.
            bag_content = len(game.bag.tiles)
            last_scores = game.current_player.scores[-ROUNDS_TO_LOOK_BACK:  ]
            last_scores.append(max_score)
            if len(last_scores) > 2 and max(last_scores) <= UNACCEPTABLE_SCORE and last_scores[-2] != 0 and bag_content > 0:
                tiles = hand.tiles
                if len(tiles) > bag_content:
                    tiles_to_Swap = random.sample(tiles, bag_content)
                    game.exchange_tiles(tiles_to_Swap)
                else:
                    game.exchange_tiles(tiles)
            else:
                high_score_moves = [move for move, score in scored_moves.items() if
                                    score == max_score]
                move = random.choice(list(high_score_moves))
                game.make_move(move.tiles_and_positions)
        else:
            bag_content = len(game.bag.tiles)
            if bag_content > 0:
                tiles = hand.tiles
                if len(tiles) > bag_content:
                    tiles_to_Swap = random.sample(tiles, bag_content)
                    game.exchange_tiles(tiles_to_Swap)
                else:
                    game.exchange_tiles(tiles)
            else:
                game.pass_round()
    return game


# Other possibilities:
# - Number of qwirkle-able rows/columns (strikes).
#.- Same as above, but include what tiles are still in play. Prioritize by what I have on my han.
# - highest score on next round with pieces left on hand.
# - same as above, just with expectation of pices that CAN still be drawn.
# - number of positions open for business after a move.
# - Opt to exchange tiles if bad fit for board.
# - Opt to exchange only some tiles (voluntarily keeping some).


if __name__ == '__main__':
    scores = set()
    for i in range(100):
        print(i)
        game = run_single_player_AI_3()
        player = game.players[0]
        score = player.total_score()
        rounds = len(player.scores)
        scores.add(score/rounds)
    mean = np.mean(list(scores))
    std = np.std(list(scores))
    print(mean)
    print(std)
