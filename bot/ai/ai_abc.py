from abc import ABC


class AiAbc(ABC):
    def get_next_move(self, grid):
        raise NotImplementedError
