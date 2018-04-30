from qwirkle.game_logic.game import Game
"""
Ting som bør lagres:
- (runde nr.)
- brikker på brettet ved rundens begynnelse.
- antall spillbare felt.
- antall helt forbudte felt.
- antall lovlige trekk (gitt hånden)
- antall lovlig  trekk med maksimal poengsum?
- antall unike brikker på hånda før runden.
- Poeng for trekket.
- antall brikker spilt i trekket.
"""
from qwirkle.AI.basic_strategies import BestMultiMoveAI
import pickle
import os
import datetime


# TODO: Might want to include the size of the set
# of all tiles that can be played adjacent to an existing tile.
# This may be a better measure of "openness" of the board than playable adjacent positions.

class RunnerLogger:
    def __init__(self, ai_player):
        self.game = Game.make_new_game(num_players=1)
        self.ai = ai_player(self.game)
        self.log = {
            'tiles on board at start of round': [],
            'playable positions total': [],
            'completely forbidden positions': [],
            'number of legal moves for hand': [],
            'number of legal moves of max score for hand': [],
            'unique tiles on hand': [],
            'score of move':[],
            'tiles played in move':  []}

    def run(self):
        num_tiles_on_board = 0
        while self.game.current_player is not None:
            self.log['tiles on board at start of round'].append(num_tiles_on_board)
            self.log['playable positions total'].append(len(self.game.board.legal_positions_with_exhaustion()))
            self.log['completely forbidden positions'].append(len(self.game.board.forbidden_positions_with_exhaustion()))
            hand = self.game.current_player.hand
            self.log['number of legal moves for hand'].append(len(self.game.board.legal_moves(hand)))
            # May not be the best consept towars the end f the game.
            self.log['unique tiles on hand'].append(len(set(self.game.current_player.hand.tiles)))
            self.ai.make_move()
            self.log['number of legal moves of max score for hand'].append(self.ai.num_high_score)
            self.log['score of move'].append(self.game.players[0].scores[-1])
            tmp = len(self.game.board.positions)
            # TODO: Not needed?
            self.log['tiles played in move'].append(tmp-num_tiles_on_board)
            num_tiles_on_board = tmp
        self.store()

    def store(self):
        filename = 'analysis/' + str(os.getpid()) + str(datetime.datetime.now())
        with open(filename, 'wb') as f:
            pickle.dump(self.log, f)


if __name__ == "__main__":
    for i in range(100):
        runner = RunnerLogger(BestMultiMoveAI)
        runner.run()
