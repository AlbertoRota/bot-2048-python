import random

import bot.tables.move_table_c as move_table_c
import bot.tables.fitness_table_c as fitness_table_c

cdef dict move_table = move_table_c.get_move_table()
cdef dict fitness_table = fitness_table_c.get_fitness_table()
MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP = 0, 1, 2, 3
ALL_MOVES = (MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP)


cdef short[:, :] do_move(short[:, :] grid, int move):
    rotated_grid = rotate_grid(grid, move)
    for i in range(4):
        rotated_grid[i] = move_table[rotated_grid[i]]
    return rotate_grid(rotated_grid, 4 - move)


def get_moves(grid: [[int]]) -> [int]:
    return [move for move in ALL_MOVES if do_move(grid, move) != grid]


def spawn_tile(grid: [[int]]):
    tile_distribution = [1] * 9 + [2]
    tile_to_spawn = tile_distribution[int(len(tile_distribution) * random.random())]

    grid = grid.copy()
    zero_list = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == 0]

    chosen_zero = zero_list[int(len(zero_list) * random.random())]
    grid[chosen_zero[0]][chosen_zero[1]] = tile_to_spawn

    return grid


cdef short[:, :] rotate_grid(short[:, :] grid, int times):
    if times == 0 or times == 4:
        rotated_grid = rot_0(grid)
    elif times == 1:
        rotated_grid = rot_90(grid)
    elif times == 2:
        rotated_grid = rot_180(grid)
    elif times == 3:
        rotated_grid = rot_270(grid)
    else:
        raise NotImplementedError("Only values between 0 and 4 are supported.")
    return rotated_grid

cdef short[:, :] rot_0(short[:, :] grid):
    cdef int i, j
    cdef short out[4][4]
    for i in range(4):
        for j in range(4):
            out[i][j] = grid[i, j]
    return out

cdef short[:, :] rot_90(short[:, :] grid):
    cdef int i, j
    cdef short out[4][4]
    for i in range(4):
        for j in range(4):
            out[i][j] = grid[3 - j, i]
    return out

cdef short[:, :] rot_180(short[:, :] grid):
    cdef int i, j
    cdef short out[4][4]
    for i in range(4):
        for j in range(4):
            out[i][j] = grid[3 - i, 3 - j]
    return out

cdef short[:, :] rot_270(short[:, :] grid):
    cdef int i, j
    cdef short out[4][4]
    for i in range(4):
        for j in range(4):
            out[i][j] = grid[j, 3 - i]
    return out

cdef double get_fitness(short[:, :] grid):
    cdef double fitness = 0
    for row in grid:
        fitness += fitness_table[row]

    for col in rot_270(grid):
        fitness += fitness_table[row]

    return fitness
