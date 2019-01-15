# cython: language_level=3
from libc.math cimport pow

cdef dict get_fitness_table():
    cdef short max_cell, cell_1, cell_2, cell_3, cell_4
    cdef short row[4]
    cdef short values[17]

    fitness_table = {}

    for cell_1 in range(17):
        for cell_2 in range(17):
            for cell_3 in range(17):
                for cell_4 in range(17):
                    row = [cell_1, cell_2, cell_3, cell_4]
                    fitness_table[row] = calculate_row_fitness(row)


cdef double calculate_row_fitness(short[:] row):
        cdef double SCORE_LOST_PENALTY = 200000.0
        cdef double SCORE_MONOTONICITY_POWER = 4.0
        cdef double SCORE_MONOTONICITY_WEIGHT = 47.0
        cdef double SCORE_SUM_POWER = 3.5
        cdef double SCORE_SUM_WEIGHT = 11.0
        cdef double SCORE_MERGES_WEIGHT = 700.0
        cdef double SCORE_EMPTY_WEIGHT = 270.0

        cdef double progress = 0
        cdef double empty = 0
        cdef double merges = 0

        cdef double prev = 0
        cdef double counter = 0

        for cell in row:
            progress += pow(cell, SCORE_SUM_POWER)

            if cell == 0:
                empty += 1
            else:
                if cell == prev:
                    counter += 1
                elif counter > 0:
                    merges += 1 + counter
                    counter = 0
                prev = cell

        if counter > 0:
            merges += 1 + counter

        cdef double monotonicity_left = 0
        cdef double monotonicity_right = 0
        for i in range(1, len(row)):
            if row[i - 1] > row[i]:
                monotonicity_left += pow(row[i - 1], SCORE_MONOTONICITY_POWER) - pow(row[i], SCORE_MONOTONICITY_POWER)
            else:
                monotonicity_right += pow(row[i], SCORE_MONOTONICITY_POWER) - pow(row[i - 1], SCORE_MONOTONICITY_POWER)

        return SCORE_LOST_PENALTY + SCORE_EMPTY_WEIGHT * empty + SCORE_MERGES_WEIGHT * merges - SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right) - SCORE_SUM_WEIGHT * progress
