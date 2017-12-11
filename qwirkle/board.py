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
        positions, tiles = zip(*tiles_and_positions)
        if self.is_allowed(tiles, positions):
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
