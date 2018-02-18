from qwirkle.game_logic.game import Game
import numpy as np
from qwirkle.AI.basic_strategies import AI


def run_single_player_AI(game, ai_player):
    ai = ai_player(game)
    while game.current_player is not None:
        ai.make_move()
    return game


if __name__ == '__main__':
    scores = set()
    for i in range(100):
        print(i)
        game = Game.make_new_game(num_players=1)
        played_game = run_single_player_AI(game, AI)
        player = played_game.players[0]
        score = player.total_score()
        rounds = len(player.scores)
        scores.add(score/rounds)
    mean = np.mean(list(scores))
    std = np.std(list(scores))
    print(mean)
    print(std)
