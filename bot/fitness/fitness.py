import math
from bot.game.board import Board


class Fitness:
    @staticmethod
    def get_fitness(board: Board) -> float:
        if board.is_game_over:
            return -float("inf")

        snake = []
        for i, col in enumerate(zip(*board.grid)):
            snake.extend(reversed(col) if i % 2 == 0 else col)

        m = max(snake)
        return sum(x / 10 ** n for n, x in enumerate(snake)) - \
               math.pow((board.grid[3][0] != m) * abs(board.grid[3][0] - m), 2)
