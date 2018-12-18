import math
from bot.game.board import Board


class Fitness:
    @staticmethod
    def get_fitness(board: Board) -> float:
        if board.is_game_over:
            return -float("inf")

        sum_score, max_tile, size = 0, 0, len(board.grid)
        for i, col in enumerate(zip(*board.grid)):
            new_col = reversed(col) if i % 2 == 0 else col
            for j, tile in enumerate(new_col):
                if tile > max_tile:
                    max_tile = tile
                sum_score += tile / 10 ** (i * size + j)

        score2 = sum_score - math.pow((board.grid[3][0] != max_tile) * abs(board.grid[3][0] - max_tile), 2)

        return score2
