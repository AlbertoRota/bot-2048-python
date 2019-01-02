import time

from bot.ai.ai_abc import AiAbc
from bot.game.board_2048 import Board2048

INF = 100000000


class IterativeDeepeningExpectMinMaxAi(AiAbc):
    def __init__(self, max_sec: float = 1.0):
        super().__init__()
        self.max_sec = max_sec
        self.score_table = {}
        self.sec_limit = 0

    def get_next_move(self, board: Board2048):
        best_movement, depth = None, 1
        self.sec_limit = time.time() + self.max_sec
        try:
            while True:
                best_movement, _ = self.expect_min_max(board, depth, True, None)
                depth += 1
        except TimeoutError:
            pass

        self.score_table = {}
        return best_movement

    def expect_min_max(self, board: Board2048, depth: int, is_move: bool = True, move: int = None) -> (int, float):
        key = self.encode(board, depth)
        if self.sec_limit < time.time():
            raise TimeoutError()

        if depth == 0:
            if key in self.score_table:
                return move, self.score_table[key]
            else:
                fitness = board.get_fitness()
                self.score_table[key] = fitness
                return move, fitness

        elif is_move:
            max_move, max_score = None, -INF
            for move in Board2048.ALL_MOVES:
                move_board = board.clone()
                move_board.do_move(move, False)
                if move_board.grid != board.grid:
                    _, move_score = self.expect_min_max(move_board, depth, False, move)
                    if move_score >= max_score:
                        max_score = move_score
                        max_move = move
            return max_move, max_score

        else:
            if key in self.score_table:
                return None, self.score_table[key]
            else:
                mean_score = 0.
                chance_moves = board.get_chance_moves()
                for chance_move in chance_moves:
                    chance_board = board.clone()
                    chance_board.do_chance_move(chance_move)
                    mean_score += chance_move[0] * self.expect_min_max(chance_board, depth - 1, True, None)[1]
                self.score_table[key] = mean_score
                return None, mean_score

    def __repr__(self) -> str:
        return "IterativeDeepeningExpectMinMaxAi(max_sec = {})".format(self.max_sec)

    @staticmethod
    def encode(board: Board2048, depth: int):
        grid = board.grid
        return tuple(grid[0]) + tuple(grid[1]) + tuple(grid[2]) + tuple(grid[3]), depth
