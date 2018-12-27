from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class GreedyAi(AiAbc):
    def __init__(self):
        super().__init__()

    def get_next_move(self, board: BoardABC):
        valid_moves = board.get_moves()
        best_movement = valid_moves[0]
        best_movement_score = -float("inf")
        for move in valid_moves:
            moved_board = board.clone()
            moved_board.do_move(move, False)

            move_fitness = board.get_fitness()
            if move_fitness > best_movement_score:
                best_movement_score = move_fitness
                best_movement = move

        return best_movement

    def __repr__(self) -> str:
        return "GreedyAi()"
