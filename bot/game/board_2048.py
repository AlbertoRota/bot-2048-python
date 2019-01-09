import random

from bot.game.board_abc import BoardABC
from bot.tables.move_table import MoveTable
from bot.tables.fitness_table import FitnessTable


class Board2048(BoardABC):
    MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP = 0, 1, 2, 3
    ALL_MOVES = (MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP)

    idx_to_row = []
    row_to_idx = {}
    move_table = {}
    fitness_table = {}
    move_table_grid_size = 0

    def __init__(self, grid: [[int]] = None, initialize: bool = False, score: int = 0):
        super().__init__()

        self.grid = grid or [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        if initialize:
            self.spawn_tile()
            self.spawn_tile()

        self.score = score

        if not Board2048.move_table:
            Board2048.move_table = MoveTable.get_move_table()

        if not Board2048.fitness_table:
            Board2048.fitness_table = FitnessTable.get_fitness_table()

        self.cached_moves = None
        self.cached_fitness = None

    def clone(self) -> "Board2048":
        return Board2048(grid=self.grid.copy(), score=self.score)

    def do_move(self, move: int, spawn_tile: bool):
        rotated_grid = self.rotate_grid(move)
        for i, row in enumerate(rotated_grid):
            aux = Board2048.move_table[tuple(row)]
            moved_row = aux.moved_left
            score_inc = aux.score_left
            self.grid[i] = [x for x in moved_row]
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

            up_down_grid = self.rotate_grid(Board2048.MOVE_UP)
            for row in up_down_grid:
                table_row = Board2048.move_table[tuple(row)]
                if table_row.can_move_left:
                    valid_moves[Board2048.MOVE_UP] = True
                if table_row.can_move_right:
                    valid_moves[Board2048.MOVE_DOWN] = True
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
        return [(chance / num_zeros, (i, j), val) for i, j in zero_list for chance, val in [(0.9, 1), (0.1, 2)]]

    def get_result(self) -> float:
        return self.score

    def get_fitness(self) -> float:
        if not self.cached_fitness:
            fitness = 0
            for row in self.grid:
                fitness_table_entry = Board2048.fitness_table[tuple(row)]
                fitness += fitness_table_entry.fitness

            for col in self.rot_270(self.grid):
                fitness_table_entry = Board2048.fitness_table[tuple(col)]
                fitness += fitness_table_entry.fitness

            self.cached_fitness = fitness

        return self.cached_fitness

    def __repr__(self) -> str:
        return "Grid: {}\nValid moves: {}\nScore: {}".format(
            self.grid,
            self.get_moves(),
            self.get_result()
        )

    def spawn_tile(self):
        tile_distribution = [1] * 9 + [2]
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
    def rot_90(grid):
        g = grid
        return [
            [g[3][0], g[2][0], g[1][0], g[0][0]],
            [g[3][1], g[2][1], g[1][1], g[0][1]],
            [g[3][2], g[2][2], g[1][2], g[0][2]],
            [g[3][3], g[2][3], g[1][3], g[0][3]]
        ]

    @staticmethod
    def rot_180(grid):
        g = grid
        return [
            [g[3][3], g[3][2], g[3][1], g[3][0]],
            [g[2][3], g[2][2], g[2][1], g[2][0]],
            [g[1][3], g[1][2], g[1][1], g[1][0]],
            [g[0][3], g[0][2], g[0][1], g[0][0]]
        ]

    @staticmethod
    def rot_270(grid):
        g = grid
        return [
            [g[0][3], g[1][3], g[2][3], g[3][3]],
            [g[0][2], g[1][2], g[2][2], g[3][2]],
            [g[0][1], g[1][1], g[2][1], g[3][1]],
            [g[0][0], g[1][0], g[2][0], g[3][0]]
        ]
