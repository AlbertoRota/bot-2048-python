from bot.ai.ai_abc import AiAbc
from bot.game.board_2048 import Board2048

UP = Board2048.MOVE_UP
RIGHT = Board2048.MOVE_RIGHT
LEFT = Board2048.MOVE_LEFT
DOWN = Board2048.MOVE_DOWN


class OrderedAi(AiAbc):
    @staticmethod
    def get_next_move(board: Board2048):
        moves = board.get_moves()
        if UP in moves:
            return UP
        if RIGHT in moves:
            return RIGHT
        if LEFT in moves:
            return LEFT
        else:
            return DOWN
