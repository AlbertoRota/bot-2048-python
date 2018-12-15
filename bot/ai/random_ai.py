import random
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class RandomAi(AiAbc):
    @staticmethod
    def get_next_move(board: Board):
        return random.sample(board.valid_moves, 1)[0]
