import random
import math
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class MonteCarloAi(AiAbc):
    @staticmethod
    def get_next_move(board: Board):
        best_score = 0
        best_move = None

        for move in board.valid_moves:
            move_score = MonteCarloAi.run_random_games(board, 5)
            if move_score > best_score:
                best_score = move_score
                best_move = move

        return best_move

    @staticmethod
    def run_random_games(board: Board, runs: int) -> float:
        return math.fsum([MonteCarloAi.run_random_game(board) for _ in range(runs)])/runs

    @staticmethod
    def run_random_game(board: Board) -> int:
        while not board.is_game_over:
            board = board.swipe_grid(random.sample(board.valid_moves, 1)[0], spawn_tile=True)
        return board.score
