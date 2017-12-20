class Position():
    # TODO: IS this a named tuple?
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and \
            self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)


class Board():
    def __init__(self, tiles=None):
        self.tiles = []
        if tiles is not None:
            self.tiles.extend(tiles)

    def is_connected(self, move_positions):
        if (0, 0) in move_positions:
            return True
        else:
            for pos in move_positions:
                neighbours = self.get_neighbour_positions(pos)
                for neighbour in neighbours:
                    if neighbour in self.positions:
                        return True
            else:
                return False
                # THis is not the whole truth, as
                # every tile needs to be next to a new or old tile.
                # However, the problem only arises for multi-tile moves
                # and they are checked later by the one-strike stuff.

    def get_neighbour_positions(self, position):
        # TODO: belongs on position.
        x, y = position
        north = (x, y + 1)
        south = (x, y - 1)
        east = (x + 1, y)
        west = (x - 1, y)
        return (north, south, east, west)

    @property
    def positions(self):
        if self.tiles:
            positions = list(zip(*self.tiles))[0]
        else:
            positions = ()
        return positions

    def is_allowed(self, tiles_and_positions):
        positions, _ = zip(*tiles_and_positions)
        if self.is_connected(positions):
            pass
        else:
            return False
        if not self.unique_positions(positions):
            return False
        # TODO: Move into if (len(positions) > 1
        same_row = self.all_same_row(positions)
        same_column = self.all_same_column(positions)
        if same_row or same_column:
            pass
        else:
            return False

        if len(positions) > 1:
            # IF several tiles, ensure one strike.
            if same_row:
                if self.positions:
                    existing_indexes = list(zip(*self.positions))[0]
                else:
                    existing_indexes = []
                move_indexes = list(zip(*positions))[0]
            elif same_column:
                if self.positions:
                    existing_indexes = list(zip(*self.positions))[1]
                else:
                    existing_indexes = []
                move_indexes = list(zip(*positions))[1]
            indexes = list(existing_indexes) + list(move_indexes)
            strikes = self.divide_into_strikes(indexes)
            if self.new_tiles_in_same_strike(strikes, move_indexes):
                pass
            else:
                return False
        else:
            pass  # not needed

        combined_tiles_and_position = self.tiles + tiles_and_positions
        combined_positions = list(zip(*combined_tiles_and_position))[0]
        for position, tile in tiles_and_positions:
            # for multi-tile moves eighter row or column strikes are identical.

            # row strike
            y = position[1]
            row_positions = [pos for pos in combined_positions if pos[1] == y]
            indexes = [x for x, _ in row_positions]
            strikes = self.divide_into_strikes(indexes)
            for strike in strikes:
                if position[0] in strike:
                    break
            strike_positions = [(x, y) for x in strike]
            strike_tiles = [tile for position, tile in
                            combined_tiles_and_position if
                            position in strike_positions]
            legal_strike = self.verify_strike(strike_tiles)
            if not legal_strike:
                return False
            else:
                pass
            # column strike
            x = position[0]
            row_positions = [pos for pos in combined_positions if pos[0] == x]
            indexes = [y for _, y in row_positions]
            strikes = self.divide_into_strikes(indexes)
            for strike in strikes:
                if position[1] in strike:
                    break
            strike_positions = [(x, y) for y in strike]
            strike_tiles = [tile for position, tile in
                            combined_tiles_and_position if
                            position in strike_positions]
            legal_strike = self.verify_strike(strike_tiles)
            if not legal_strike:
                return False
            else:
                pass

        return True
        # return a bool.
        # 1. Next to an existing piece (not first move).
        # 2. In same "strike".
        # 3. The row strikes and column strikes in which they
        # are included, are legal (same shape/color, and
        # all different for the other trait.
        # TODO: Make sure these are enough conditions.

        # ALTERNATE APPROACH:
        # 1. Add piees to board (after making copy)
        #     While doing it, check for overlapping positions,
        #     both among new-new and old-new (and old-old?) tiles
        # 2. make three sets: explored positions, discovered positions,
        # undisovered tiles
        # Do a breadth first search.
        # 3. Identify all strikes by positions.
        # 4. verify that all strikes are valid (shapes & colors)
        # 5. No. 4 can be exploited for points too.

    def verify_strike(self, tiles):
        strike_length = len(tiles)
        tiles = [(t.color, t.shape) for t in tiles]
        colors, shapes = list(zip(*tiles))
        num_unique_colors = len(set(colors))
        num_unique_shapes = len(set(shapes))
        # color_strike
        if num_unique_colors == 1 and num_unique_shapes == strike_length:
            return True
        elif num_unique_shapes == 1 and num_unique_colors == strike_length:
            return True
        else:
            False

        # shape_strike

    def divide_into_strikes(self, indexes):
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

    def new_tiles_in_same_strike(self, strikes, move_indexes):
        move_indexes = set(move_indexes)
        count = 0
        for strike in strikes:
            if move_indexes & set(strike):
                count += 1
        return count == 1

    def contiguous(self, positions):
        # TODO: identify row/column strike only once.
        if self.all_same_column(positions):
            indexes = list(list(zip(*positions))[1])
        else:
            indexes = list(list(zip(*positions))[0])
        indexes.sort()
        return indexes[-1] - indexes[0] + 1 == len(indexes)

    def unique_positions(self, positions):
        # TODO: Is there a builtin for this?
        return len(positions) == len(set(positions))

    def all_same_row(self, positions):
        # TODO: Join with self.all_same_column() to
        # benefit from zipping only once.
        rows = list(zip(*positions))[1]
        return len(set(rows)) == 1

    def all_same_column(self, positions):
        columns = list(zip(*positions))[0]
        return len(set(columns)) == 1

    def make_move(self, tiles_and_positions):
        positions, tiles = zip(*tiles_and_positions)
        if self.is_allowed(tiles, positions):
            score = self.score(positions)
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
