from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class GreedyAi(AiAbc):
    @staticmethod
    def get_next_move(board: BoardABC):
        valid_moves = board.get_moves()
        best_movement = valid_moves[0]
        best_movement_score = -float("inf")
        for move in valid_moves:
            moved_board = board.clone()
            moved_board.do_move(move)

            move_fitness = board.get_fitness()
            if move_fitness > best_movement_score:
                best_movement_score = move_fitness
                best_movement = move

        return best_movement
