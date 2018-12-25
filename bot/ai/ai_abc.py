from abc import ABC
from bot.game.board_2048 import Board2048


class AiAbc(ABC):
    @staticmethod
    def get_next_move(board: Board2048):
        raise NotImplementedError
