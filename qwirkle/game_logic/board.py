from collections import namedtuple, Counter
import copy
from qwirkle.game_logic.tile import Color, Shape, Tile


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

    @property
    def tiles_list(self):
        # TODO: Rename to "tiles", after renaming the
        # existing "tiles" variable.
        if self.tiles:
            tiles = list(zip(*self.tiles))[1]
        else:
            tiles = ()
        return tiles

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
            raise IllegalMoveError()

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

    def legal_single_piece_moves(self, hand):
        moves = set()
        if len(self.positions) == 0:
            positions = [Position(0, 0)]
        else:
            positions = self.adjacent_positions()
        for pos in positions:
            for tile in hand.tiles:
                move = Move(self, [(pos, tile)])
                if move.is_allowed():
                    moves.add(move)
        return moves

    def legal_moves(self, hand):
        single_piece_moves = self._get_single_piece_moves(hand)
        two_piece_moves = self._get_two_piece_moves(single_piece_moves)
        two_piece_moves = uniquify_moves(two_piece_moves)
        three_piece_moves = self._get_one_pluss_moves(two_piece_moves)
        three_piece_moves = uniquify_moves(three_piece_moves)
        four_piece_moves = self._get_one_pluss_moves(three_piece_moves)
        four_piece_moves = uniquify_moves(four_piece_moves)
        five_piece_moves = self._get_one_pluss_moves(four_piece_moves)
        five_piece_moves = uniquify_moves(five_piece_moves)
        six_piece_moves = self._get_one_pluss_moves(five_piece_moves)
        six_piece_moves = uniquify_moves(six_piece_moves)

        moves_list = [single_piece_moves, two_piece_moves, three_piece_moves,
                      four_piece_moves, five_piece_moves, six_piece_moves]
        result = []
        for moves in moves_list:
            new_moves = set()
            for move, _ in moves:
                new_moves.add(move)
            result.append(new_moves)
        return result
        # Does not take the union of the sets,
        # because the highest paying move is guaranteed to
        # be in the last non-empty set.

    def _get_single_piece_moves(self, hand):
        moves = set()
        if len(self.positions) == 0:
            positions = [Position(0, 0)]
        else:
            positions = self.adjacent_positions()
        hand_set = set(hand.tiles)
        for pos in positions:
            for tile in hand_set:
                move = Move(self, [(pos, tile)])
                if move.is_allowed():
                    reduced_hand_set = set(hand_set)
                    reduced_hand_set.remove(tile)
                    reduced_hand_set = frozenset(reduced_hand_set)
                    # TODO: Also remove any pieces with neighter
                    # same color or same shape as the used piece.
                    moves.add((move, reduced_hand_set))
        return moves

    def _get_two_piece_moves(self, single_piece_moves):
        # Try to place remaining pieces in hand at the end of any "strike" the
        # current piece is part of.
        moves = set()
        for move, hand_set in single_piece_moves:
            pos = move.positions[0]

            # Positions in column
            strike = move.get_column_strike(pos)
            pos1 = Position(pos[0], strike[0]-1)
            pos2 = Position(pos[0], strike[-1]+1)

            # Positions in row
            strike = move.get_row_strike(pos)
            pos3 = Position(strike[0]-1, pos[1])
            pos4 = Position(strike[-1]+1, pos[1])

            positions = (pos1, pos2, pos3, pos4)
            for tile in hand_set:
                for position in positions:
                    tiles_and_positions = copy.copy(move.tiles_and_positions)
                    tiles_and_positions.append((position, tile))
                    new_move = Move(self, tiles_and_positions)
                    if new_move.is_allowed():
                        reduced_hand_set = set(hand_set)
                        reduced_hand_set.remove(tile)
                        reduced_hand_set = frozenset(reduced_hand_set)
                        # TODO: At this point the move has a well defined
                        # color or shape. Identify it, and remove all
                        # irrelevant pieces (for efficiency)
                        moves.add((new_move, reduced_hand_set))
        return moves

    def _get_one_pluss_moves(self, multi_piece_moves):
        """'multi_piece_moves' consist of at least two pieces,
        the row/columnness is established."""
        moves = set()
        for move, hand_set in multi_piece_moves:
            pos = move.positions[0]
            if move.all_same_column():
                strike = move.get_column_strike(pos)
                pos1 = Position(pos[0], strike[0]-1)
                pos2 = Position(pos[0], strike[-1]+1)
            else:
                strike = move.get_row_strike(pos)
                pos1 = Position(strike[0]-1, pos[1])
                pos2 = Position(strike[-1]+1, pos[1])
            positions = (pos1, pos2)
            for tile in hand_set:
                for position in positions:
                    tiles_and_positions = copy.copy(move.tiles_and_positions)
                    tiles_and_positions.append((position, tile))
                    new_move = Move(self, tiles_and_positions)
                    if new_move.is_allowed():
                        reduced_hand_set = set(hand_set)
                        reduced_hand_set.remove(tile)
                        reduced_hand_set = frozenset(reduced_hand_set)
                        moves.add((new_move, reduced_hand_set))
        return moves

    def adjacent_positions(self):
        marked = set()
        for pos in self.positions:
            for neigh in pos.neighbour_positions():
                if (neigh not in self.positions) and (neigh not in marked):
                    marked.add(neigh)
                    yield neigh

    def legal_positions(self):
        # TODO: Can be cached and kept up to date.
        result = set()
        for pos in self.adjacent_positions():
            if len(self.legal_tiles(pos)) > 0:
                result.add(pos)
        return result

    def has_a_legal_move(self):
        """Same as legal_positions_with_exhaustion, but returns early
        once a legal move is found."""
        # TODO: Can be cached and kept up to date.
        # TODO: see similarity to legal single piece moves.
        remaining_tiles = self.remaining_tiles()
        if len(self.positions) == 0:
            return True
        else:
            positions = self.adjacent_positions()
        for pos in positions:
            for tile in remaining_tiles:
                move = Move(self, [(pos, tile)])
                if move.is_allowed():
                    return True
        return False

    def legal_positions_with_exhaustion(self):
        """Same as legal_positions, but takes into account
        that all three of some tiles are already played."""
        # TODO: Can be cached and kept up to date.
        remaining_tiles = self.remaining_tiles()
        return self.legal_positions_based_on_tiles(remaining_tiles)

    def legal_positions_based_on_tiles(self, tiles):
        result = set()
        for pos in self.adjacent_positions():
            if len(self.legal_tiles(pos, tiles)) > 0:
                result.add(pos)
        return result

    def legal_positions_based_on_tile(self, tile):
        return self.legal_positions_based_on_tiles(set(tile))

    def legal_positions_based_on_provisional_move_and_tile(self, move, tile):
        raise NotImplementedError()
        # TODO: implement

    def all_reachable_positions_based_on_hand(self, hand):
        # differs from legal_positions_based_on_tiles() by
        # including positions not adjacent to existing tiles.
        legal_moves = self.legal_moves(hand)
        result = set()
        for moves in legal_moves:
            for move in moves:
                result.update(move.positions)
        return result

    def forbidden_positions(self):
        """Return set of positions that cannot be legally filled with a tile.

        As a game of Qwirkle unfolds, some positions on the board cannot be filled.
        This can be due to them being at the end of a qwirkle or due to conflicting
        demands from different adjacent positions.

        See also: forbidden_positions_with_exhaustion()"""
        # TODO: Can be cached and kept up to date.
        result = set()
        for pos in self.adjacent_positions():
            if len(self.legal_tiles(pos)) == 0:
                result.add(pos)
        return result

    def forbidden_positions_with_exhaustion(self):
        # TODO: Can be cached and kept up to date.
        """Same as forbidden positions, but takes into account
        that all three of some tiles are already played."""
        result = set()
        remaining_tiles = self.remaining_tiles()
        for pos in self.adjacent_positions():
            if len(self.legal_tiles(pos, remaining_tiles)) == 0:
                result.add(pos)
        return result

    def remaining_tiles(self):
        """Returns a set of tiles that could still be played,
        that is less than three instances of it is found on the board.
        """
        tiles = Tile.set_of_all_tiles()
        result = set()
        count = Counter(self.tiles_list)
        for tile in tiles:
            if count[tile] < 3:
                result.add(tile)
        return result

    def legal_tiles(self, adjacent_position, tiles=None):
        """Given a Position, this method returns the set
        of tiles that can be placed there.
        """
#         # 0.1 check not occupied
#         if adjacent_position in self.positions:
#             raise ValueError('Position already occupied.')
#         # 0.2 check actually adjacent.
#         neighbours = adjacent_position.neighbour_positions()
#         for pos in neighbours:
#             if pos in self.positions:
#                 break
#         else:
#             raise ValueError('Position not adjacent to any tile.')
        # 1. For each adjacent strike, find set of allowed continuations.
        if tiles is None:
            tiles = Tile.set_of_all_tiles()
        result = set()
        for tile in tiles:
            if Move(self, [(adjacent_position, tile)]).is_allowed():
                result.add(tile)
        return result
        # Note: this set can be cashed, and as the game unfolds,
        # the set can only shrink.
        # In particular. Certain squares will become unusable.
        # IF the reuslt is to be cached, another algorithm may be better.


class IllegalMoveError(ValueError):
    pass


class Move():
    def __init__(self, board, tiles_and_positions):
        self.board = board
        self.tiles_and_positions = tiles_and_positions
        self.positions, self.tiles = zip(*tiles_and_positions)
        self.columns, self.rows = list(zip(*self.positions))
#        self.combined_tiles_and_position = None
#        self.combined_positions = None

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

    @property
    def combined_tiles_and_position(self):
        return self.board.tiles + self.tiles_and_positions

    @property
    def combined_positions(self):
        return list(zip(*self.combined_tiles_and_position))[0]

    def is_compatible_with_surrounding_tiles(self):
#         self.combined_tiles_and_position = self.board.tiles + self.tiles_and_positions
#         self.combined_positions = list(zip(*self.combined_tiles_and_position))[0]
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


def uniquify_moves(moves):
    new_moves = set()
    result = set()
    for move, hand in moves:
        tiles_and_positions = tuple(move.tiles_and_positions)
        if tiles_and_positions not in new_moves:
            new_moves.add(tiles_and_positions)
            result.add((move, hand))
    return result


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
