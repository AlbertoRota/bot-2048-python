from abc import ABC
from bot.game.board import Board


class AiAbc(ABC):
    @staticmethod
    def get_next_move(board: Board):
        raise NotImplementedError
