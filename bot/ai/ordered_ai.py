import random
from bot.ai.ai_abc import AiAbc
from bot.game.game import Game


class OrderedAi(AiAbc):

    @staticmethod
    def get_next_move(game: Game):
        if "LEFT" in game.valid_moves:
            return "LEFT"
        if "UP" in game.valid_moves:
            return "UP"
        if "RIGHT" in game.valid_moves:
            return "RIGHT"
        else:
            return "DOWN"
