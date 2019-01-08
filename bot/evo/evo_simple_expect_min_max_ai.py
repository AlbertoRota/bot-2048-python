from bot.ai.ai_abc import AiAbc
from bot.game.board_2048 import Board2048

INF = 10000000000


class SimpleExpectMinMaxAi(AiAbc):
    def __init__(self, eval_func, depth: int = 2, min_chance: float = 0.05, max_acc_chance: float = 0.75):
        super().__init__()
        self.eval_func = eval_func
        self.depth = depth
        self.min_chance = min_chance
        self.max_acc_chance = max_acc_chance
        self.score_table = {}

    def get_next_move(self, board: Board2048):
        best_movement, _ = self.simple_expect_min_max(board, self.depth, True, None)
        self.score_table = {}
        return best_movement

    def simple_expect_min_max(self, board: Board2048, depth: int, is_move: bool = True, move: int = None) -> (int, float):
        if depth == 0:
            # Leaf node reached, run evaluation function
            key = self.encode(board, depth)
            if key in self.score_table:
                return move, self.score_table[key]
            else:
                score_free, score_monotone_lr, score_monotone_ud, score_smoothness_lr, score_smoothness_ud = board.get_raw_fitness()
                fitness = self.eval_func(
                    score_free, score_monotone_lr, score_monotone_ud, score_smoothness_lr, score_smoothness_ud
                )
                self.score_table[key] = fitness
                return move, fitness

        elif is_move:
            # Move node, pick the best move.
            max_move, max_score = None, -INF
            for move in Board2048.ALL_MOVES:
                move_board = board.clone()
                move_board.do_move(move, False)
                if move_board.grid != board.grid:
                    _, move_score = self.simple_expect_min_max(move_board, depth, False, move)
                    if move_score >= max_score:
                        max_score = move_score
                        max_move = move
            return max_move, max_score

        else:
            # Chance node, calculate the average.
            key = self.encode(board, depth)
            if key in self.score_table:
                return None, self.score_table[key]
            else:
                i, acc_chance, mean_score = 0, 0., 0.
                chance_moves = board.get_chance_moves()
                while acc_chance < self.max_acc_chance and i <= len(chance_moves):
                    chance_move = chance_moves[i]
                    if chance_move[0] > self.min_chance:
                        acc_chance += chance_move[0]
                        chance_board = board.clone()
                        chance_board.do_chance_move(chance_move)
                        mean_score += chance_move[0] * self.simple_expect_min_max(chance_board, depth - 1, True)[1]
                    i += 1
                mean_score /= acc_chance
                self.score_table[key] = mean_score
                return None, mean_score

    @staticmethod
    def encode(board: Board2048, depth: int):
        grid = board.grid
        return tuple(grid[0]) + tuple(grid[1]) + tuple(grid[2]) + tuple(grid[3]), depth

    def __repr__(self) -> str:
        return "SimpleExpectMinMaxAi(depth = {}, min_chance = {}, max_acc_chance = {})".format(
            self.depth, self.min_chance, self.max_acc_chance
        )
