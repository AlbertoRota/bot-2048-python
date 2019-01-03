import random
import time

from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class TimedMonteCarloAi(AiAbc):
    def __init__(self, max_sec: float = 0.5):
        super().__init__()
        self.max_sec = max_sec

    def get_next_move(self, board: BoardABC):
        results = self.run_random_games(board)
        best_move = self.analyze_games(results)
        return best_move

    def __repr__(self) -> str:
        return "TimedMonteCarloAi(max_sec = {})".format(self.max_sec)

    def run_random_games(self, board: BoardABC) -> {int: [int, int]}:
        results = {move: [0, 0] for move in board.get_moves()}
        runs, sec, start_time = 0, 0, time.time()

        while sec < self.max_sec:
            initial_move = random.choice(board.get_moves())
            run_board = board.clone()
            run_board.do_move(initial_move, True)
            valid_moves = run_board.get_moves()
            while valid_moves:
                run_board.do_move(valid_moves[int(len(valid_moves) * random.random())], True)
                valid_moves = run_board.get_moves()

            pre_score, pre_count = results[initial_move]
            results[initial_move] = [pre_score + run_board.get_result(), pre_count + 1]

            runs, sec = runs + 1, time.time() - start_time

        return results

    def analyze_games(self, results: {str: [int, int]}) -> str:
        best_score, best_move = 0, None

        for move, score in results.items():
            if score[1] != 0:
                avg_move_score = score[0]/score[1]
                if avg_move_score > best_score:
                    best_score, best_move = avg_move_score, move

        return best_move
