class MoveTable:
    move_table = {}

    def __init__(self):
        raise NotImplementedError("This class should NOT be instantiated, use the static method \"get_move_table()\"")

    @staticmethod
    def get_move_table() -> {}:
        if not MoveTable.move_table:
            MoveTable.init_move_table()

        return MoveTable.move_table

    @staticmethod
    def init_move_table():
        max_cell = 16
        values = range(max_cell + 1)
        move_table = MoveTable.move_table

        for cell_1 in values:
            for cell_2 in values:
                for cell_3 in values:
                    for cell_4 in values:
                        row = cell_1, cell_2, cell_3, cell_4
                        move_table[row] = MoveTableEntry(row)


class MoveTableEntry:
    def __init__(self, row: ()):
        self.moved_left, self.score_left = MoveTableEntry.swipe_row_left(row)
        self.can_move_left = self.moved_left != row

        self.moved_right, self.score_right = MoveTableEntry.swipe_row_left(tuple(reversed(row)))
        self.can_move_right = self.moved_right != tuple(reversed(row))

    @staticmethod
    def swipe_row_left(row: ()) -> ():
        last_non_zero = -1
        first_free_cell = 0
        new_row = [0] * len(row)
        score_inc = 0

        for cell in row:
            if cell != 0:
                if cell == last_non_zero:
                    new_tile = last_non_zero + 1
                    new_row[first_free_cell - 1] = new_tile
                    score_inc += 2 ** new_tile
                    last_non_zero = -1
                else:
                    last_non_zero = cell
                    new_row[first_free_cell] = cell
                    first_free_cell += 1

        return tuple(new_row), score_inc
