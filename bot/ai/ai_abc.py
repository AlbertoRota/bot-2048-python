from abc import ABC
from bot.game.board_abc import BoardABC


class AiAbc(ABC):
    def get_next_move(self, board: BoardABC):
        raise NotImplementedError
