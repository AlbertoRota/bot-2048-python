import random

from bot.game.board_abc import BoardABC
from bot.fitness.fitness_2048 import Fitness2048
from bot.tables.row import Row


class Board2048(BoardABC):
    MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP = 0, 1, 2, 3
    ALL_MOVES = (MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP)

    idx_to_row = []
    row_to_idx = {}
    move_table = {}
    move_table_grid_size = 0

    def __init__(self, grid: [[int]] = None, initialize: bool = False, score: int = 0):
        super().__init__()

        self.grid = grid or [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        if initialize:
            self.spawn_tile()
            self.spawn_tile()

        self.score = score

        if not Board2048.move_table or len(self.grid[0]) != Board2048.move_table_grid_size:
            Board2048.init_move_table(len(self.grid[0]))

        if len(self.grid) == 3:
            self.rot_90, self.rot_180, self.rot_270 = Board2048.rot_3x3_90, Board2048.rot_3x3_180, Board2048.rot_3x3_270
        elif len(self.grid) == 4:
            self.rot_90, self.rot_180, self.rot_270 = Board2048.rot_4x4_90, Board2048.rot_4x4_180, Board2048.rot_4x4_270

        self.cached_moves = None
        self.cached_fitness = None

    @staticmethod
    def init_move_table(size: int):
        Board2048.move_table_grid_size = size
        Board2048.move_table = {}
        Board2048.idx_to_row = []
        Board2048.row_to_idx = {}

        values = [0] + [2 ** x for x in range(1, (size * size + 1))]
        max_cell = values[len(values) - 1]

        # TODO: Clarify, it does the same as the commented code
        Board2048.foo_recursive(values, size)
        # idx = 0
        # for a in values:
        #     for b in values:
        #         for c in values:
        #             for d in values:
        #                 row = a, b, c, d
        #                 Board2048.idx_to_row.append(row)
        #                 Board2048.row_to_idx[row] = idx
        #                 idx += 1

        for idx, row in enumerate(Board2048.idx_to_row):
            row_moved = tuple(Board2048.swipe_row_left(row))
            if max(row_moved[0]) > max_cell:
                Board2048.move_table[idx] = -1
            else:
                Board2048.move_table[idx] = Board2048.row_to_idx[tuple(row_moved[0])]
                Board2048.move_table[row] = Row(row)

    @staticmethod
    def foo_recursive(values, size):
        Board2048.foo_recursion(values, (), size, 0)

    @staticmethod
    def foo_recursion(values, row, depth, idx):
        if depth == 0:
            Board2048.idx_to_row.append(row)
            Board2048.row_to_idx[row] = idx
            idx += 1
            return idx
        else:
            for value in values:
                new_row = row + (value,)
                idx = Board2048.foo_recursion(values, new_row, depth - 1, idx)
            return idx

    def clone(self) -> "Board2048":
        return Board2048(grid=self.grid.copy(), score=self.score)

    def do_move(self, move: int, spawn_tile: bool):
        rotated_grid = self.rotate_grid(move)
        for i, row in enumerate(rotated_grid):
            aux = Board2048.move_table[tuple(row)]
            moved_row = aux.moved_left
            score_inc = aux.score_left
            self.grid[i] = moved_row.copy()
            self.score += score_inc
        self.grid = self.rotate_grid(4 - move)

        if spawn_tile:
            self.spawn_tile()

        self.cached_moves = None
        self.cached_fitness = None

    def get_moves(self) -> [int]:
        if self.cached_moves is None:
            valid_moves = {}

            left_right_grid = self.rotate_grid(Board2048.MOVE_LEFT)
            for row in left_right_grid:
                table_row = Board2048.move_table[tuple(row)]
                if table_row.can_move_left:
                    valid_moves[Board2048.MOVE_LEFT] = True
                if table_row.can_move_right:
                    valid_moves[Board2048.MOVE_RIGHT] = True
                if Board2048.MOVE_LEFT in valid_moves and Board2048.MOVE_RIGHT in valid_moves:
                    break

            down_up_grid = self.rotate_grid(Board2048.MOVE_DOWN)
            for row in down_up_grid:
                table_row = Board2048.move_table[tuple(row)]
                if table_row.can_move_left:
                    valid_moves[Board2048.MOVE_DOWN] = True
                if table_row.can_move_right:
                    valid_moves[Board2048.MOVE_UP] = True
                if Board2048.MOVE_DOWN in valid_moves and Board2048.MOVE_UP in valid_moves:
                    break

            self.cached_moves = list(valid_moves.keys())

        return self.cached_moves

    def do_chance_move(self, chance_move: (float, (int, int), int)):
        cell = chance_move[1]
        value = chance_move[2]
        self.grid[cell[0]][cell[1]] = value

        self.cached_moves = None
        self.cached_fitness = None

    def get_chance_moves(self) -> [(float, (int, int), int)]:
        grid = self.grid
        zero_list = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == 0]
        num_zeros = len(zero_list)
        return [(chance / num_zeros, (i, j), val) for i, j in zero_list for chance, val in [(0.9, 2), (0.1, 4)]]

    def get_result(self) -> float:
        return self.score

    def get_fitness(self) -> float:
        if not self.cached_fitness:
            if self.get_moves():
                score_free = Fitness2048.eval_free(self.grid)

                score_monotone_lr = 0
                score_smoothness_lr = 0
                for row in self.grid:
                    table_row = Board2048.move_table[tuple(row)]
                    score_monotone_lr += table_row.monotone_fitness
                    score_smoothness_lr += table_row.smoothness_fitness

                score_monotone_ud = 0
                score_smoothness_ud = 0
                for column in self.rot_90(self.grid):
                    table_column = Board2048.move_table[tuple(column)]
                    score_monotone_ud += table_column.monotone_fitness
                    score_smoothness_ud += table_column.smoothness_fitness

                score_monotone = score_monotone_lr + score_monotone_ud
                score_smoothness = (score_smoothness_lr + score_smoothness_ud) / (len(self.grid) * 2)

                self.cached_fitness = score_free + score_monotone + score_smoothness
            else:
                self.cached_fitness = -float("inf")

        return self.cached_fitness

    def __repr__(self) -> str:
        return "Grid: {}\nValid moves: {}\nScore: {}".format(
            self.grid,
            self.get_moves(),
            self.get_result()
        )

    def spawn_tile(self):
        tile_distribution = [2] * 9 + [4]
        tile_to_spawn = tile_distribution[int(len(tile_distribution) * random.random())]

        grid = self.grid
        zero_list = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == 0]

        chosen_zero = zero_list[int(len(zero_list) * random.random())]
        self.grid[chosen_zero[0]][chosen_zero[1]] = tile_to_spawn

    def rotate_grid(self, times: int) -> [[int]]:
        grid = self.grid
        if times == 0 or times == 4:
            rotated_grid = grid.copy()
        elif times == 1:
            rotated_grid = self.rot_90(grid)
        elif times == 2:
            rotated_grid = self.rot_180(grid)
        elif times == 3:
            rotated_grid = self.rot_270(grid)
        else:
            raise NotImplementedError("Only values between 0 and 4 are supported.")
        return rotated_grid

    @staticmethod
    def rot_3x3_90(grid):
        g = grid
        return [
            [g[2][0], g[1][0], g[0][0]],
            [g[2][1], g[1][1], g[0][1]],
            [g[2][2], g[1][2], g[0][2]]
        ]

    @staticmethod
    def rot_4x4_90(grid):
        g = grid
        return [
            [g[3][0], g[2][0], g[1][0], g[0][0]],
            [g[3][1], g[2][1], g[1][1], g[0][1]],
            [g[3][2], g[2][2], g[1][2], g[0][2]],
            [g[3][3], g[2][3], g[1][3], g[0][3]]
        ]

    @staticmethod
    def rot_3x3_180(grid):
        g = grid
        return [
            [g[2][2], g[2][1], g[2][0]],
            [g[1][2], g[1][1], g[1][0]],
            [g[0][2], g[0][1], g[0][0]]
        ]

    @staticmethod
    def rot_4x4_180(grid):
        g = grid
        return [
            [g[3][3], g[3][2], g[3][1], g[3][0]],
            [g[2][3], g[2][2], g[2][1], g[2][0]],
            [g[1][3], g[1][2], g[1][1], g[1][0]],
            [g[0][3], g[0][2], g[0][1], g[0][0]]
        ]

    @staticmethod
    def rot_3x3_270(grid):
        g = grid
        return [
            [g[0][2], g[1][2], g[2][2]],
            [g[0][1], g[1][1], g[2][1]],
            [g[0][0], g[1][0], g[2][0]]
        ]

    @staticmethod
    def rot_4x4_270(grid):
        g = grid
        return [
            [g[0][3], g[1][3], g[2][3], g[3][3]],
            [g[0][2], g[1][2], g[2][2], g[3][2]],
            [g[0][1], g[1][1], g[2][1], g[3][1]],
            [g[0][0], g[1][0], g[2][0], g[3][0]]
        ]

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
