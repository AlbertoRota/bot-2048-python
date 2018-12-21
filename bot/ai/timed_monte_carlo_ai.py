import random
import time

from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class TimedMonteCarloAi(AiAbc):
    @staticmethod
    def get_next_move(board: Board, max_iter: int = 99999999, max_sec: float = 0.5):
        results = TimedMonteCarloAi.run_random_games(board, max_iter, max_sec)
        best_move = TimedMonteCarloAi.analyze_games(results)
        return best_move

    @staticmethod
    def run_random_games(board: Board, max_iter: int, max_sec: float) -> {str: [int, int]}:
        results = {move: [0, 0] for move in board.valid_moves}
        current_iter, current_sec, start_time = 0, 0, time.time()

        while current_iter < max_iter and current_sec < max_sec:
            initial_move = random.choice(board.valid_moves)
            run_board = board.swipe_grid(initial_move, spawn_tile=True)

            while not run_board.is_game_over:
                run_board = run_board.swipe_grid(random.choice(run_board.valid_moves), spawn_tile=True)

            pre_score, pre_count = results[initial_move]
            results[initial_move] = [pre_score + run_board.score, pre_count + 1]

            current_iter, current_sec = current_iter + 1, time.time() - start_time

        return results

    @staticmethod
    def analyze_games(results: {str: [int, int]}) -> str:
        best_score, best_move = 0, None

        for move, score in results.items():
            if score[1] != 0:
                avg_move_score = score[0]/score[1]
                if avg_move_score > best_score:
                    best_score, best_move = avg_move_score, move

        return best_move
