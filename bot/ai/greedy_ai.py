from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC
from bot.fitness.fitness_2048 import Fitness2048


class GreedyAi(AiAbc):
    @staticmethod
    def get_next_move(board: BoardABC):
        all_moves = board.get_moves()
        best_movement = all_moves[0]
        best_movement_score = -float("inf")
        for move in all_moves:
            moved_board = board.clone()
            moved_board.do_move(move)

            movement_score = Fitness2048.get_fitness(board)
            if movement_score > best_movement_score:
                best_movement_score = movement_score
                best_movement = move

        return best_movement
