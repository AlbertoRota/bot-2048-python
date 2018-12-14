from abc import ABC
import bot.game.game as Game


class AiAbc(ABC):
    @staticmethod
    def get_next_move(game: Game):
        raise NotImplementedError
