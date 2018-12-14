from __future__ import annotations
import random
import numpy as np


class Board(object):
    # All possible moves in a 2048 game.
    all_moves = ["LEFT", "UP", "DOWN", "RIGHT"]

    # A relation between swipe direction and number of rotations needed, used in "swipe_grid"
    __direction_to_rotation__ = {"LEFT": 0, "UP": 1, "DOWN": 3, "RIGHT": 2}

    def __init__(self, grid: np.ndarray = np.zeros((4, 4)), score: int = 0):
        # Initialize current grid
        self.grid = grid

        # Pre-calculate valid moves
        self.valid_moves = []
        for move in self.all_moves:
            if self.__is_valid_move__(move):
                self.valid_moves.append(move)

        # Check if the game over, in our case, when we have no further valid moves
        self.is_game_over = not bool(self.valid_moves)

        # Set the current score
        self.score = score

    def swipe_grid(self, direction: str) -> Board:
        """
        Swipes the grid in the specified direction.
        Once done, return
        """
        new_grid = np.rot90(np.copy(self.grid), Board.__direction_to_rotation__[direction])
        new_score = self.score
        for i, row in enumerate(new_grid):
            new_grid[i], score_inc = Board.__swipe_row_left___(row)
            new_score += score_inc
        new_grid = np.rot90(new_grid, 4 - Board.__direction_to_rotation__[direction])
        return Board(new_grid, new_score)

    @staticmethod
    def __swipe_row_left___(row: list):
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

    def __is_valid_move__(self, direction):
        grid_to_check = np.rot90(self.grid, Board.__direction_to_rotation__[direction])
        for row in grid_to_check:
            for x, y in zip(row[:-1], row[1:]):
                if y != 0 and (x == y or x == 0):
                    return True
        return False

    def spawn_tile(self) -> Board:
        new_grid = np.copy(self.grid)
        tile_to_spawn = random.sample([2] * 9 + [4], 1)[0]

        zero_index = np.argwhere(new_grid == 0)
        np.random.shuffle(zero_index)

        new_grid[zero_index[0][0], zero_index[0][1]] = tile_to_spawn
        return Board(new_grid, self.score)