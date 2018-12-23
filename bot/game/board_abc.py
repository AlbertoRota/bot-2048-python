from abc import ABC


class BoardABC(ABC):
    def __init__(self):
        pass

    def clone(self) -> "BoardABC":
        pass

    def do_move(self, move):
        raise NotImplementedError

    def get_moves(self) -> [int]:
        raise NotImplementedError

    def get_result(self) -> float:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
