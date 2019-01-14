import random

from bot.tables.move_table import MoveTable
from bot.tables.fitness_table import FitnessTable

move_table = MoveTable.get_simple_move_table()
fitness_table = FitnessTable.get_fitness_table()
MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP = 0, 1, 2, 3
ALL_MOVES = (MOVE_LEFT, MOVE_DOWN, MOVE_RIGHT, MOVE_UP)


def do_move(grid: [[int]], move: int):
    rotated_grid = rotate_grid(grid, move)
    for i, row in enumerate(rotated_grid):
        rotated_grid[i] = list(move_table[tuple(row)])
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


def rotate_grid(grid: [[int]], times: int) -> [[int]]:
    if times == 0 or times == 4:
        rotated_grid = grid.copy()
    elif times == 1:
        rotated_grid = rot_90(grid)
    elif times == 2:
        rotated_grid = rot_180(grid)
    elif times == 3:
        rotated_grid = rot_270(grid)
    else:
        raise NotImplementedError("Only values between 0 and 4 are supported.")
    return rotated_grid


def rot_90(grid: [[int]]):
    g = grid
    return [
        [g[3][0], g[2][0], g[1][0], g[0][0]],
        [g[3][1], g[2][1], g[1][1], g[0][1]],
        [g[3][2], g[2][2], g[1][2], g[0][2]],
        [g[3][3], g[2][3], g[1][3], g[0][3]]
    ]


def rot_180(grid: [[int]]):
    g = grid
    return [
        [g[3][3], g[3][2], g[3][1], g[3][0]],
        [g[2][3], g[2][2], g[2][1], g[2][0]],
        [g[1][3], g[1][2], g[1][1], g[1][0]],
        [g[0][3], g[0][2], g[0][1], g[0][0]]
    ]


def rot_270(grid: [[int]]):
    g = grid
    return [
        [g[0][3], g[1][3], g[2][3], g[3][3]],
        [g[0][2], g[1][2], g[2][2], g[3][2]],
        [g[0][1], g[1][1], g[2][1], g[3][1]],
        [g[0][0], g[1][0], g[2][0], g[3][0]]
    ]


def get_fitness(grid: [[int]]) -> float:
    fitness = 0
    for row in grid:
        fitness_table_entry = fitness_table[tuple(row)]
        fitness += fitness_table_entry.fitness

    for col in rot_270(grid):
        fitness_table_entry = fitness_table[tuple(col)]
        fitness += fitness_table_entry.fitness

    return fitness
