from collections import Counter

from bot.ai.ai_abc import AiAbc
from bot.game.board_2048 import Board2048


class DynamicExpectMinMaxAi(AiAbc):
    def __init__(self):
        super().__init__()
        self.min_search_depth = 3
        self.depth_limit = 3
        self.min_cprob = 0.0001
        self.cache_depth_limit = 15
        self.score_table = {}

    def get_next_move(self, board: Board2048):
        valid_movements = board.get_moves()
        if len(valid_movements) == 1:
            return valid_movements[0]

        best_movement, best_score = None, 0
        self.score_table = {}
        self.depth_limit = max(3, self.count_distinct_tiles(board) - 2)
        self.depth_limit = self.depth_limit // 2 + 1
        for move in valid_movements:
            move_score = self.score_toplevel_move(board, move)
            if move_score >= best_score:
                best_score = move_score
                best_movement = move

        return best_movement

    @staticmethod
    def count_distinct_tiles(board: Board2048) -> int:
        counter = Counter()
        grid = board.grid
        for row in grid:
            for cell in row:
                counter[cell] += 1

        return len(counter.keys())

    def score_toplevel_move(self, board: Board2048, move: int) -> float:
        new_board = board.clone()
        new_board.do_move(move, False)

        return self.score_tilechoose_node(new_board, 0, 1.0) + 1e-6

    def score_tilechoose_node(self, board: Board2048, curr_depth: int, cprob: float):
        if cprob < self.min_cprob or curr_depth >= self.depth_limit:
            return board.get_fitness()

        if curr_depth < self.cache_depth_limit:
            key = self.encode(board)
            if key in self.score_table:
                score, score_depth = self.score_table[key]
                if score_depth <= curr_depth:
                    return score

        mean = 0
        chance_moves = board.get_chance_moves()
        for chance_move in chance_moves:
            new_board = board.clone()
            new_board.do_chance_move(chance_move)
            mean += self.score_move_node(new_board, curr_depth, cprob * chance_move[0]) * chance_move[0]

        if curr_depth < self.cache_depth_limit:
            key = self.encode(board)
            self.score_table[key] = mean, curr_depth

        return mean

    @staticmethod
    def encode(board: Board2048):
        grid = board.grid
        return tuple(grid[0]) + tuple(grid[1]) + tuple(grid[2]) + tuple(grid[3])

    def score_move_node(self, board: Board2048, curr_depth: int, cprob: float):
        best = 0.
        for move in Board2048.ALL_MOVES:
            new_board = board.clone()
            new_board.do_move(move, False)
            if new_board.grid != board.grid:
                best = max(best, self.score_tilechoose_node(new_board, curr_depth + 1, cprob))

        return best

    def __repr__(self) -> str:
        return "DynamicExpectMinMaxAi()"
