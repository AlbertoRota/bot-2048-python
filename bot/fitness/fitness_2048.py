import math
from bot.game.board_2048 import Board2048


class Fitness2048:
    snake_pattern = []

    @staticmethod
    def create_snake_pattern(board: Board2048):
        rows = len(board.grid) - 1
        cols = len(board.grid[0]) - 1

        for i in range(rows):
            is_reversed = i % 2 == 0
            for j in range(cols):
                idx = (i, j if not is_reversed else cols - j)
                Fitness2048.snake_pattern.append(idx)

    @staticmethod
    def get_fitness(board: Board2048) -> float:
        if not board.get_moves():
            return -float("inf")

        if not Fitness2048.snake_pattern:
            Fitness2048.create_snake_pattern(board)

        grid = board.grid
        sum_score, max_tile = 0, 0
        for i, coord in enumerate(Fitness2048.snake_pattern):
            tile = grid[coord[0]][coord[1]]
            sum_score = tile / 10 ** i
            if tile > max_tile:
                max_tile = tile


        score2 = sum_score - math.pow((grid[3][0] != max_tile) * abs(grid[3][0] - max_tile), 2)

        return score2
