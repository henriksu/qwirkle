from collections import namedtuple


class Position(namedtuple('Position', 'x y')):
    def neighbour_positions(self):
        x_coordinate, y_coordinate = self
        cls = type(self)
        north = cls(x_coordinate, y_coordinate + 1)
        south = cls(x_coordinate, y_coordinate - 1)
        east = cls(x_coordinate + 1, y_coordinate)
        west = cls(x_coordinate - 1, y_coordinate)
        return (north, south, east, west)


class Board():
    def __init__(self, tiles=None):
        self.tiles = []
        if tiles is not None:
            self.tiles.extend(tiles)
        # VALIDATING BOARD:
        # 1. Add piees to board (after making copy)
        #     While doing it, check for overlapping positions,
        #     both among new-new and old-new (and old-old?) tiles
        # 2. make three sets: explored positions, discovered positions,
        # undisovered tiles
        # Do a breadth first search.
        # 3. Identify all strikes by positions.
        # 4. verify that all strikes are valid (shapes & colors)

    @property
    def positions(self):
        if self.tiles:
            positions = list(zip(*self.tiles))[0]
        else:
            positions = ()
        return positions

    def is_allowed(self, tiles_and_positions):
        move = Move(self, tiles_and_positions)
        return move.is_allowed()

    def make_move(self, tiles_and_positions):
        move = Move(self, tiles_and_positions)
        if move.is_allowed():
            score = move.score()
            self._add_to_board(tiles_and_positions)
            return score
        else:
            raise ValueError()
            # TODO: Let a level closer to GUI expect this error.
            # It is not the boards responsibility to expect clumsy players,
            # and besides if the player is an AI, the error will have to be
            # dealt with very differently.
            # TODO: Subclass ValueError.

    def _add_to_board(self, tiles_and_positions):
        # Placeholder in case of more elaborate data structures.
        self.tiles.extend(tiles_and_positions)

    def column_indexes(self, row):
        pos = filter(lambda pos: pos.y == row, self.positions)
        existing_indexes = map(lambda p: p.x, pos)#list(zip(*pos))[0]
        return existing_indexes

    def row_indexes(self, column):
        pos = filter(lambda pos: pos.x == column, self.positions)
        existing_indexes = map(lambda p: p.y, pos)
        return existing_indexes


class Move():
    def __init__(self, board, tiles_and_positions):
        self.board = board
        self.tiles_and_positions = tiles_and_positions
        self.positions, self.tiles = zip(*tiles_and_positions)
        self.columns, self.rows = list(zip(*self.positions))
        self.combined_tiles_and_position = None
        self.combined_positions = None

    def score(self):
        score = 0
        if self.all_same_column():
            pos = self.positions[0]
            strike = self.get_column_strike(pos)
            score += self.score_strike(strike)
            for pos in self.positions:
                strike = self.get_row_strike(pos)
                score += self.score_strike(strike)
        else:  # all same row
            pos = self.positions[0]
            strike = self.get_row_strike(pos)
            score += self.score_strike(strike)
            for pos in self.positions:
                strike = self.get_column_strike(pos)
                score += self.score_strike(strike)
        return score

    def score_strike(self, strike):
        n = len(strike)
        if n == 1:
            return 0
        elif n == 6:
            return 12
        else:
            return n

    def is_allowed(self):
        return \
            self.unique_positions() and \
            self.is_connected() and\
            self.all_new_tiles_in_same_strike() and \
            self.is_compatible_with_surrounding_tiles()

    def unique_positions(self):
        tmp = set(self.board.positions) & set(self.positions)
        return (len(tmp) == 0) and \
            len(self.positions) == len(set(self.positions))

    def is_connected(self):
        if self.is_first_move():
            return True
        else:
            return self.a_new_tile_touches_a_old_tile()
        # THis is not the whole truth, as
        # every tile needs to be next to a new or old tile.
        # However, the problem only arises for multi-tile moves
        # and they are checked later by the one-strike stuff.

    def is_first_move(self):
        return (0, 0) in self.positions

    def a_new_tile_touches_a_old_tile(self):
        for pos in self.positions:
            for neighbour in pos.neighbour_positions():
                if neighbour in self.board.positions:
                    return True
        return False

    def all_new_tiles_in_same_strike(self):
        return self.only_one_tile_in_move() or \
            self.multiple_tiles_in_one_strike()

    def only_one_tile_in_move(self):
        return len(self.positions) == 1

    def multiple_tiles_in_one_strike(self):
        same_row = self.all_same_row()
        same_column = self.all_same_column()
        if same_row:
            existing_indexes = self.board.column_indexes(self.positions[0][1])
            move_indexes = self.columns
        elif same_column:
            existing_indexes = self.board.row_indexes(self.positions[0][0])
            move_indexes = self.rows
        else:
            return False
        result = self.verify_tiles_in_strikes(existing_indexes, move_indexes)
        return result

    def verify_tiles_in_strikes(self, existing_indexes, move_indexes):
        strikes = self.calculate_strikes(existing_indexes, move_indexes)
        return self.new_tiles_in_same_strike(strikes, move_indexes)

    def calculate_strikes(self, existing_indexes, move_indexes):
        indexes = list(existing_indexes) + list(move_indexes)
        strikes = divide_into_strikes(indexes)
        return strikes

    def new_tiles_in_same_strike(self, strikes, move_indexes):
        move_indexes = set(move_indexes)
        count = 0
        for strike in strikes:
            if move_indexes & set(strike):
                count += 1
        return count == 1

    def is_compatible_with_surrounding_tiles(self):
        self.combined_tiles_and_position = self.board.tiles + self.tiles_and_positions
        self.combined_positions = list(zip(*self.combined_tiles_and_position))[0]
        if self.all_same_column():
            if not self.verify_column_strike(self.positions[0]):
                return False
            for position, _ in self.tiles_and_positions:
                if not self.verify_row_strike(position):
                    return False
        else:  # All same row.
            if not self.verify_row_strike(self.positions[0]):
                return False
            for position, _ in self.tiles_and_positions:
                if not self.verify_column_strike(position):
                    return False
        return True

    def verify_row_strike(self, position):
        strike_positions = self.get_row_strike_positions(position)
        strike_tiles = [tile for position, tile in
                        self.combined_tiles_and_position if
                        position in strike_positions]
        return is_valid_strike(strike_tiles)

    def get_row_strike_positions(self, position):
        strike = self.get_row_strike(position)
        strike_positions = [(x, position.y) for x in strike]
        return strike_positions

    def get_row_strike(self, position):
        y = position[1]
        row_positions = [pos for pos in self.combined_positions if pos[1] == y]
        indexes = [x for x, _ in row_positions]
        strikes = divide_into_strikes(indexes)
        for strike in strikes:
            if position[0] in strike:
                return strike

    def verify_column_strike(self, position):
        strike_positions = self.get_column_strike_positions(position)
        strike_tiles = [tile for position, tile in
                        self.combined_tiles_and_position if
                        position in strike_positions]
        return is_valid_strike(strike_tiles)

    def get_column_strike_positions(self, position):
        strike = self.get_column_strike(position)
        strike_positions = [(position.x, y) for y in strike]
        return strike_positions

    def get_column_strike(self, position):
        x = position[0]
        row_positions = [pos for pos in self.combined_positions if pos[0] == x]
        indexes = [y for _, y in row_positions]
        strikes = divide_into_strikes(indexes)
        for strike in strikes:
            if position[1] in strike:
                return strike

    def all_same_row(self):
        return len(set(self.rows)) == 1

    def all_same_column(self):
        return len(set(self.columns)) == 1


def is_valid_strike(tiles):
    strike_length = len(tiles)
    tiles = [(t.color, t.shape) for t in tiles]
    colors, shapes = list(zip(*tiles))
    num_unique_colors = len(set(colors))
    num_unique_shapes = len(set(shapes))
    if num_unique_colors == 1 and num_unique_shapes == strike_length:
        return True
    elif num_unique_shapes == 1 and num_unique_colors == strike_length:
        return True
    else:
        return False


def divide_into_strikes(indexes):
    indexes.sort()
    strikes = []
    current_strike = [indexes[0]]
    for i in indexes[1:]:
        if i == (current_strike[-1] + 1):
            current_strike.append(i)
        else:
            strikes.append(current_strike)
            current_strike = [i]
    strikes.append(current_strike)
    return strikes
