from qwirkle.game import Game
import random
import numpy as np


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
# avg.: 519.4 std.: 35.63
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


if __name__ == '__main__':
    scores = set()
    for i in range(100):
        print(i)
        game = run_single_player_AI_2()
        player = game.players[0]
        score = player.total_score()
        scores.add(score)
    mean = np.mean(list(scores))
    std = np.std(list(scores))
    print(mean)
    print(std)
