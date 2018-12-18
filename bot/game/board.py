from __future__ import annotations
import random
import copy
import itertools


class Board(object):
    # All possible moves in a 2048 game.
    all_moves = ["LEFT", "UP", "DOWN", "RIGHT"]

    # A relation between swipe direction and number of rotations needed, used in "swipe_grid"
    __direction_to_rotation__ = {"LEFT": 0, "UP": 3, "DOWN": 1, "RIGHT": 2}

    def __init__(self, grid: [[int]], score: int = 0, initialize: bool = False):
        # Initialize current grid
        self.grid = grid
        if initialize:
            self.grid = Board.__spawn_tile__(self.grid)
            self.grid = Board.__spawn_tile__(self.grid)

        # Pre-calculate valid moves
        self.valid_moves = Board.__get_valid_moves__(self.grid)

        # Check if the game over, in our case, when we have no further valid moves
        self.is_game_over = not bool(self.valid_moves)

        # Set the current score
        self.score = score

    def swipe_grid(self, direction: str, spawn_tile: bool = False) -> Board:
        """
        Swipes the grid in the specified direction.
        Once done, return
        """
        new_grid = Board.__rotate_grid__(self.grid, Board.__direction_to_rotation__[direction])
        new_score = self.score
        for i, row in enumerate(new_grid):
            new_grid[i], score_inc = Board.__swipe_row_left___(row)
            new_score += score_inc
        new_grid = Board.__rotate_grid__(new_grid, 4 - Board.__direction_to_rotation__[direction])

        if spawn_tile:
            new_grid = Board.__spawn_tile__(new_grid)

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

    @staticmethod
    def __rotate_grid__(grid: [[int]], times: int) -> [[int]]:
        if times == 0 or times == 4:
            new_grid = grid.copy()
        elif times == 1:
            new_grid = list(map(list, zip(*grid[::-1])))
        elif times == 2:
            new_grid = list(map(list, zip(*grid[::-1])))
            new_grid = list(map(list, zip(*new_grid[::-1])))
        elif times == 3:
            new_grid = list(map(list, zip(*grid[::-1])))
            new_grid = list(map(list, zip(*new_grid[::-1])))
            new_grid = list(map(list, zip(*new_grid[::-1])))
        else:
            raise NotImplementedError("Only values between 0 and 4 are supported.")
        return new_grid

    @staticmethod
    def __get_valid_moves__(grid: [[int]]) -> [str]:
        valid_moves = {}
        for row in grid:
            for i in range(len(row) - 1):
                first_tile, second_tile = row[i], row[i + 1]
                if first_tile != 0:
                    if first_tile == second_tile:
                        valid_moves["LEFT"] = True
                        valid_moves["RIGHT"] = True
                        break

                if first_tile != 0 and second_tile == 0:
                    valid_moves["RIGHT"] = True

                if second_tile != 0 and first_tile == 0:
                    valid_moves["LEFT"] = True

            if "LEFT" in valid_moves and "RIGHT" in valid_moves:
                break

        for row in Board.__rotate_grid__(grid, 1):
            for i in range(len(row) - 1):
                first_tile, second_tile = row[i], row[i + 1]
                if first_tile != 0:
                    if first_tile == second_tile:
                        valid_moves["UP"] = True
                        valid_moves["DOWN"] = True
                        break

                if first_tile != 0 and second_tile == 0:
                    valid_moves["UP"] = True

                if second_tile != 0 and first_tile == 0:
                    valid_moves["DOWN"] = True

            if "UP" in valid_moves and "DOWN" in valid_moves:
                break

        return list(valid_moves.keys())

    @staticmethod
    def __spawn_tile__(grid: [[int]]) -> [[int]]:
        new_grid = grid.copy()
        tile_to_spawn = random.choice([2] * 9 + [4])

        zero_list = list()
        for i in range(len(new_grid)):
            for j in range(len(new_grid[0])):
                if new_grid[i][j] == 0:
                    zero_list.append((i, j))

        chosen_zero = random.choice(zero_list)
        new_grid[chosen_zero[0]][chosen_zero[1]] = tile_to_spawn

        return new_grid
