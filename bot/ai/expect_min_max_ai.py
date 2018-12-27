from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class ExpectMinMaxAi(AiAbc):
    def __init__(self, search_depth: int = 3):
        super().__init__()
        self.search_depth = search_depth

    def get_next_move(self, board: BoardABC):
        valid_moves = board.get_moves()
        best_movement = valid_moves[0]
        best_movement_score = -float("inf")
        for move in valid_moves:
            move_board = board.clone()
            move_board.do_move(move, False)
            movement_score = self.__expect_min_max__(move_board, self.search_depth, False)
            if movement_score > best_movement_score:
                best_movement_score = movement_score
                best_movement = move

        return best_movement

    def __repr__(self) -> str:
        return "ExpectMinMaxAi(search_depth = {})".format(self.search_depth)

    def __expect_min_max__(self, board: BoardABC, depth: int, is_move: bool) -> float:
        valid_moves = board.get_moves()
        if not valid_moves or depth == 0:
            return board.get_fitness()
        elif is_move:
            max_alpha = -float("inf")
            for move in valid_moves:
                max_board = board.clone()
                max_board.do_move(move, False)
                max_alpha = max(max_alpha, self.__expect_min_max__(max_board, depth - 1, False))
            return max_alpha
        else:
            mean_alpha = 0.
            chance_moves = board.get_chance_moves()
            for chance_move in chance_moves:
                chance_board = board.clone()
                chance_board.do_chance_move(chance_move)
                mean_alpha += chance_move[0] * self.__expect_min_max__(chance_board, depth - 1, True)

            return mean_alpha
