import copy
import numpy as np
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


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
            return board.score
        elif is_move:
            max_alpha = -float("inf")
            for move in board.valid_moves:
                max_alpha = max(max_alpha, SimpleExpectMinMaxAi.__expect_min_max__(board.swipe_grid(move), depth - 1, False))
            return max_alpha
        else:
            mean_alpha = 0
            zeros = np.argwhere(board.grid == 0)
            if len(zeros) > 4:
                zeros = zeros[np.random.randint(zeros.shape[0], size=4), :]
            for zero in zeros:
                grid_two = copy.deepcopy(board.grid)
                grid_two[zero[0]][zero[1]] = 2

                mean_alpha += SimpleExpectMinMaxAi.__expect_min_max__(Board(grid_two, board.score), depth - 1, True)

            mean_alpha = mean_alpha / zeros.shape[0]
            return mean_alpha
