from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC
from bot.game.board_2048 import Board2048


class SimpleExpectMinMaxAi(AiAbc):
    def __init__(self, search_depth: int = 3, min_chance: float = 0.05, max_acc_chance: float = 0.5):
        super().__init__()
        self.search_depth = search_depth
        self.min_chance = min_chance
        self.max_acc_chance = max_acc_chance

    def get_next_move(self, board: BoardABC):
        best_movement = None
        best_movement_score = -float("inf")

        for move in Board2048.ALL_MOVES:
            move_board = board.clone()
            move_board.do_move(move, False)
            if move_board.grid != board.grid:
                movement_score = self.__simple_expect_min_max__(move_board, self.search_depth, False)
                if movement_score > best_movement_score:
                    best_movement_score = movement_score
                    best_movement = move

        return best_movement

    def __repr__(self) -> str:
        return "SimpleExpectMinMaxAi(search_depth = {}, min_chance = {}, max_acc_chance = {})".format(
            self.search_depth, self.min_chance, self.max_acc_chance
        )

    def __simple_expect_min_max__(self, board: BoardABC, depth: int, is_move: bool) -> float:
        if depth == 0:
            return board.get_fitness()
        elif is_move:
            max_alpha = -90000000
            for move in Board2048.ALL_MOVES:
                max_board = board.clone()
                max_board.do_move(move, False)
                if max_board.grid != board.grid:
                    max_alpha = max(max_alpha, self.__simple_expect_min_max__(max_board, depth - 1, False))
            return max_alpha
        else:
            i = 0
            acc_chance, mean_alpha = 0., 0.
            chance_moves = board.get_chance_moves()
            while acc_chance < self.max_acc_chance and i <= len(chance_moves):
                chance_move = chance_moves[i]
                if chance_move[0] > self.min_chance:
                    acc_chance += chance_move[0]
                    chance_board = board.clone()
                    chance_board.do_chance_move(chance_move)
                    mean_alpha += chance_move[0] * self.__simple_expect_min_max__(chance_board, depth - 1, True)
                i += 1

            return mean_alpha / acc_chance
