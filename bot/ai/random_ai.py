import random
from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class RandomAi(AiAbc):
    @staticmethod
    def get_next_move(board: BoardABC):
        moves = board.get_moves()
        return moves[int(len(moves) * random.random())]
