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
            move_score = MonteCarloAi.run_random_games(board, move, 50)
            if move_score > best_score:
                best_score = move_score
                best_move = move

        return best_move

    @staticmethod
    def run_random_games(board: Board, initial_move: str, runs: int) -> float:
        scores = [MonteCarloAi.run_random_game(board, initial_move) for _ in range(runs)]
        return math.fsum(scores)

    @staticmethod
    def run_random_game(board: Board, initial_move: str) -> int:
        board = board.swipe_grid(initial_move, spawn_tile=True)
        while not board.is_game_over:
            board = board.swipe_grid(random.choice(board.valid_moves), spawn_tile=True)
        return board.score
