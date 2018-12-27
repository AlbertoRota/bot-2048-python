import random
from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class RandomAi(AiAbc):
    def __init__(self):
        super().__init__()

    def get_next_move(self, board: BoardABC):
        valid_moves = board.get_moves()
        return valid_moves[int(len(valid_moves) * random.random())]

    def __repr__(self) -> str:
        return "RandomAi()"
