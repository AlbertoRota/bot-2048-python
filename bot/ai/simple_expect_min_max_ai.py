import itertools
import random
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board
from bot.fitness.fitness import Fitness


class SimpleExpectMinMaxAi(AiAbc):
    @staticmethod
    def get_next_move(board: Board):
        best_movement = board.valid_moves[0]
        best_movement_score = -float("inf")
        for move in board.valid_moves:
            movement_score = SimpleExpectMinMaxAi.__expect_min_max__(board.swipe_grid(move), 3, False)
            if movement_score > best_movement_score:
                best_movement_score = movement_score
                best_movement = move

        return best_movement

    @staticmethod
    def __expect_min_max__(board: Board, depth: int, is_move: bool) -> float:
        if board.is_game_over or depth == 0:
            return Fitness.get_fitness(board)
        elif is_move:
            max_alpha = -float("inf")
            for move in board.valid_moves:
                max_alpha = max(max_alpha, SimpleExpectMinMaxAi.__expect_min_max__(board.swipe_grid(move), depth - 1, False))
            return max_alpha
        else:
            mean_alpha = 0.
            num_of_zeros = 0
            grid = board.grid
            rows, cols = list(range(len(grid))), list(range(len(grid[0])))
            random.shuffle(rows)
            random.shuffle(cols)

            for i, j in itertools.product(rows, cols):
                if num_of_zeros < 4 and grid[i][j] == 0:
                    grid_two = grid.copy()
                    grid_two[i][j] = 2
                    num_of_zeros += 1

                    mean_alpha += SimpleExpectMinMaxAi.__expect_min_max__(Board(grid_two, board.score), depth - 1, True)

            mean_alpha = mean_alpha / num_of_zeros
            return mean_alpha
