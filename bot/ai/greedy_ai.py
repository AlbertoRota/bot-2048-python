from bot.ai.ai_abc import AiAbc
from bot.game.board import Board
from bot.fitness.fitness import Fitness


class GreedyAi(AiAbc):
    @staticmethod
    def get_next_move(board: Board):
        best_movement = board.valid_moves[0]
        best_movement_score = -float("inf")
        for move in board.valid_moves:
            movement_score = Fitness.get_fitness(board.swipe_grid(move))
            if movement_score > best_movement_score:
                best_movement_score = movement_score
                best_movement = move

        return best_movement
