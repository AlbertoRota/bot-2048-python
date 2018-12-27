import random
import time

from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class TimedMonteCarloAi(AiAbc):
    @staticmethod
    def get_next_move(board: BoardABC, max_iter: int = 99999999, max_sec: float = 0.1):
        results = TimedMonteCarloAi.run_random_games(board, max_iter, max_sec)
        best_move = TimedMonteCarloAi.analyze_games(results)
        return best_move

    @staticmethod
    def run_random_games(board: BoardABC, max_iter: int, max_sec: float) -> {str: [int, int]}:
        results = {move: [0, 0] for move in board.get_moves()}
        current_iter, current_sec, start_time = 0, 0, time.time()

        while current_iter < max_iter and current_sec < max_sec:
            initial_move = random.choice(board.get_moves())
            run_board = board.clone()
            run_board.do_move(initial_move, True)
            valid_moves = run_board.get_moves()
            while valid_moves:
                run_board.do_move(valid_moves[int(len(valid_moves) * random.random())], True)
                valid_moves = run_board.get_moves()

            pre_score, pre_count = results[initial_move]
            results[initial_move] = [pre_score + run_board.get_result(), pre_count + 1]

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
