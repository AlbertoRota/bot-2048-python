import random
import itertools
import numpy as np


class Game:
    directions = ["LEFT", "UP", "DOWN", "RIGHT"]
    direction_to_rotation = {"LEFT": 0, "UP": 1, "DOWN": 3, "RIGHT": 2}

    def __init__(self):
        """ Initialize a 2048 game """
        b = [[0] * 4 for i in range(4)]
        # self.b = Game.spawn(b, 2)

    @staticmethod
    def __swipe_row_left___(row: list):
        last_non_zero = -1
        first_free_cell = 0
        new_row = [0] * len(row)

        for cell in row:
            if cell != 0:
                if cell == last_non_zero:
                    new_row[first_free_cell - 1] = last_non_zero + cell
                    last_non_zero = -1
                else:
                    last_non_zero = cell
                    new_row[first_free_cell] = cell
                    first_free_cell += 1

        return new_row

    @staticmethod
    def swipe_grid(grid, direction):
        new_grid = np.rot90(grid, Game.direction_to_rotation[direction])
        for i, row in enumerate(new_grid):
            new_grid[i] = Game.__swipe_row_left___(row)
        return np.rot90(new_grid, 4 - Game.direction_to_rotation[direction])

    @staticmethod
    def is_valid_move(grid, direction):
        grid_to_check = np.rot90(grid, Game.direction_to_rotation[direction])
        for row in grid_to_check:
            for x, y in zip(row[:-1], row[1:]):
                if y != 0 and (x == y or x == 0):
                    return True
        return False

    @staticmethod
    def is_game_over(grid):
        for direction in Game.directions:
            if Game.is_valid_move(grid, direction):
                return False
        return True

    @staticmethod
    def spawn_tile(grid):
        rows, cols = list(range(len(grid))), list(range(len(grid[0])))
        random.shuffle(rows)
        random.shuffle(cols)

        new_grid = np.copy(grid)
        dist = [2] * 9 + [4]
        for i, j in itertools.product(rows, cols):
            if new_grid[i][j] == 0:
                new_grid[i][j] = random.sample(dist, 1)[0]
                return new_grid
        return new_grid
