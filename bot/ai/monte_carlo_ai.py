import random
import math
from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class MonteCarloAi(AiAbc):
    def __init__(self, runs: int = 200):
        super().__init__()
        self.runs = runs

    def get_next_move(self, board: BoardABC):
        valid_moves = board.get_moves()
        best_score = 0
        best_move = None

        runs_per_move = self.runs // len(valid_moves)
        for move in valid_moves:
            move_score = MonteCarloAi.run_random_games(board, move, runs_per_move)
            if move_score > best_score:
                best_score = move_score
                best_move = move

        return best_move

    def __repr__(self) -> str:
        return "MonteCarloAi(runs = {})".format(self.runs)

    @staticmethod
    def run_random_games(board: BoardABC, initial_move: int, runs: int) -> float:
        scores = [MonteCarloAi.run_random_game(board, initial_move) for _ in range(runs)]
        return math.fsum(scores)

    @staticmethod
    def run_random_game(board: BoardABC, initial_move: int) -> float:
        run_board = board.clone()
        run_board.do_move(initial_move, True)
        valid_moves = run_board.get_moves()
        while valid_moves:
            run_board.do_move(valid_moves[int(len(valid_moves) * random.random())], True)
            valid_moves = run_board.get_moves()
        return run_board.get_result()
