from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class OrderedAi(AiAbc):

    @staticmethod
    def get_next_move(board: Board):
        if "LEFT" in board.valid_moves:
            return "LEFT"
        if "UP" in board.valid_moves:
            return "UP"
        if "RIGHT" in board.valid_moves:
            return "RIGHT"
        else:
            return "DOWN"
