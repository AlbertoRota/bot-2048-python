from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC


class OrderedAi(AiAbc):
    def __init__(self):
        super().__init__()

    def get_next_move(self, board: BoardABC):
        return min(board.get_moves())

    def __repr__(self) -> str:
        return "OrderedAi()"
