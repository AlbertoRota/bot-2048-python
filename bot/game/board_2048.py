import random

from bot.game.board_abc import BoardABC


class Board2048(BoardABC):
    MOVE_LEFT   = 0
    MOVE_DOWN   = 1
    MOVE_RIGHT  = 2
    MOVE_UP     = 3

    def __init__(self, grid: [[int]] = None, initialize_grid: bool = False, score: int = 0):
        super().__init__()

        if not grid:
            self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        else:
            self.grid = grid

        if initialize_grid:
            self.spawn_tile()
            self.spawn_tile()

        self.score = score

        self.cached_moves = None

    def clone(self) -> "Board2048":
        return Board2048(grid=self.grid.copy(), score=self.score)

    def do_move(self, move, spawn_tile: bool = False):
        rotated_grid = self.rotate_grid(move)
        for i, row in enumerate(rotated_grid):
            self.grid[i], score_inc = Board2048.swipe_row_left(row)
            self.score += score_inc
        self.grid = self.rotate_grid(4 - move)

        if spawn_tile:
            self.spawn_tile()

        self.cached_moves = None

    def get_moves(self) -> [int]:
        if self.cached_moves is None:
            valid_moves = {}

            # 0 = LEFT and 2 = RIGHT
            for row in self.grid:
                for i in range(len(row) - 1):
                    first_tile, second_tile = row[i], row[i + 1]
                    if first_tile != 0:
                        if first_tile == second_tile:
                            valid_moves[0] = True
                            valid_moves[2] = True
                            break

                    if first_tile != 0 and second_tile == 0:
                        valid_moves[2] = True

                    if second_tile != 0 and first_tile == 0:
                        valid_moves[0] = True

                if 0 in valid_moves and 2 in valid_moves:
                    break

            # 1 = DOWN and 3 = UP
            for col in self.rotate_grid(1):
                for i in range(len(col) - 1):
                    first_tile, second_tile = col[i], col[i + 1]
                    if first_tile != 0:
                        if first_tile == second_tile:
                            valid_moves[3] = True
                            valid_moves[1] = True
                            break

                    if first_tile != 0 and second_tile == 0:
                        valid_moves[3] = True

                    if second_tile != 0 and first_tile == 0:
                        valid_moves[1] = True

                if 3 in valid_moves and 1 in valid_moves:
                    break

            self.cached_moves = list(valid_moves.keys())

        return self.cached_moves

    def get_result(self) -> float:
        return self.score

    def __repr__(self) -> str:
        return "Grid: {}\nValid moves: {}\nScore: {}".format(
            self.grid,
            self.get_moves(),
            self.get_result()
        )

    def spawn_tile(self):
        tile_to_spawn = random.choice([2] * 9 + [4])

        zero_list = list()
        grid = self.grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    zero_list.append((i, j))

        chosen_zero = random.choice(zero_list)
        self.grid[chosen_zero[0]][chosen_zero[1]] = tile_to_spawn

    def rotate_grid(self, times: int) -> [[int]]:
        grid = self.grid
        if times == 0 or times == 4:
            rotated_grid = grid.copy()
        elif times == 1:
            rotated_grid = list(map(list, zip(*grid[::-1])))
        elif times == 2:
            rotated_grid = list(map(list, zip(*grid[::-1])))
            rotated_grid = list(map(list, zip(*rotated_grid[::-1])))
        elif times == 3:
            rotated_grid = list(map(list, zip(*grid[::-1])))
            rotated_grid = list(map(list, zip(*rotated_grid[::-1])))
            rotated_grid = list(map(list, zip(*rotated_grid[::-1])))
        else:
            raise NotImplementedError("Only values between 0 and 4 are supported.")
        return rotated_grid

    @staticmethod
    def swipe_row_left(row: [int]) -> ([int], int):
        last_non_zero = -1
        first_free_cell = 0
        new_row = [0] * len(row)
        score_inc = 0

        for cell in row:
            if cell != 0:
                if cell == last_non_zero:
                    new_tile = last_non_zero + cell
                    new_row[first_free_cell - 1] = new_tile
                    score_inc += new_tile
                    last_non_zero = -1
                else:
                    last_non_zero = cell
                    new_row[first_free_cell] = cell
                    first_free_cell += 1
        return new_row, score_inc
