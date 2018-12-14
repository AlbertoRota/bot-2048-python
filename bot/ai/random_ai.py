import random
from bot.ai.ai_abc import AiAbc
from bot.game.game import Game


class RandomAi(AiAbc):
    @staticmethod
    def get_next_move(game: Game):
        return random.sample(game.valid_moves, 1)[0]
