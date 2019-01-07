import time

from bot.ai.ai_abc import AiAbc
from bot.game.board_2048 import Board2048

INF = 10000000000


class MinMaxAi(AiAbc):
    def __init__(self, search_depth: int = 3):
        super().__init__()
        self.depth = search_depth
        self.score_table = {}

    def get_next_move(self, board: Board2048):
        best_movement, _ = self.min_max(board, self.depth, is_move=True)
        self.score_table = {}
        return best_movement

    def min_max(self, board: Board2048, depth: int, alpha: float = -INF, beta: float = INF, is_move: bool = True) -> (int, float):
        key = self.encode(board, depth)
        if depth == 0:
            # Leaf node reached, run evaluation function
            if key in self.score_table:
                return None, self.score_table[key]
            else:
                fitness = board.get_fitness()
                self.score_table[key] = fitness
                return None, fitness

        elif is_move:
            # Move node, pick the best move.
            max_move, max_score = None, -INF
            for move in Board2048.ALL_MOVES:
                move_board = board.clone()
                move_board.do_move(move, False)
                if move_board.grid != board.grid:
                    _, move_score = self.min_max(move_board, depth, alpha, beta, False)
                    if move_score >= max_score:
                        max_score = move_score
                        max_move = move

                    alpha = max(alpha, move_score)
                    if alpha >= beta:
                        break
            return max_move, max_score

        else:
            # Adversary node, pick the worst move.
            if key in self.score_table:
                return None, self.score_table[key]
            else:
                min_score = INF
                chance_moves = board.get_chance_moves()
                for move in chance_moves:
                    move_board = board.clone()
                    move_board.do_chance_move(move)
                    _, move_score = self.min_max(move_board, depth - 1, alpha, beta, True)
                    if move_score <= min_score:
                        min_score = move_score

                    beta = min(beta, move_score)
                    if alpha >= beta:
                        break
                self.score_table[key] = min_score
                return None, min_score

    def __repr__(self) -> str:
        return "MinMaxAi(depth = {})".format(self.depth)

    @staticmethod
    def encode(board: Board2048, depth: int):
        grid = board.grid
        return tuple(grid[0]) + tuple(grid[1]) + tuple(grid[2]) + tuple(grid[3]), depth
