from bot.fitness.fitness_2048 import Fitness2048


class Row:
    def __init__(self, row: [[int]]):
        self.moved_left, self.score_left = Row.swipe_row_left(row)
        self.can_move_left = self.moved_left != list(row)

        self.moved_right, self.score_right = Row.swipe_row_left(list(reversed(row)))
        self.can_move_right = self.moved_right != list(reversed(row))

        self.zeroes = [i for i, cell in enumerate(row) if cell == 0]

        self.monotone_fitness = Fitness2048.eval_row_monotone(row)
        self.smoothness_fitness = Fitness2048.eval_row_smoothness(row)
        self.zeroes_fitness = 0

    @staticmethod
    def swipe_row_left(row: [int]) -> ([int], int):
        last_non_zero = -1
        first_free_cell = 0
        new_row = [0] * len(row)
        score_inc = 0

        for cell in row:
            if cell != 0:
                if cell == last_non_zero:
                    new_tile = last_non_zero + cell
                    new_row[first_free_cell - 1] = new_tile
                    score_inc += new_tile
                    last_non_zero = -1
                else:
                    last_non_zero = cell
                    new_row[first_free_cell] = cell
                    first_free_cell += 1
        return new_row, score_inc