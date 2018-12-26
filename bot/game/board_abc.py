from abc import ABC


class BoardABC(ABC):
    def __init__(self, initialize: bool = False):
        pass

    def clone(self) -> "BoardABC":
        pass

    def do_move(self, move: int, spawn_tile: bool):
        raise NotImplementedError

    def get_moves(self) -> [int]:
        raise NotImplementedError

    def do_chance_move(self, chance_move: (float, (int, int), int)):
        raise NotImplementedError

    def get_chance_moves(self) -> [(float, (int, int), int)]:
        raise NotImplementedError

    def get_result(self) -> float:
        raise NotImplementedError

    def get_fitness(self) -> float:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
