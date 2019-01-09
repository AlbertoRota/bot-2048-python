class FitnessTable:
    fitness_table = {}

    def __init__(self):
        raise NotImplementedError(
            "This class should NOT be instantiated, use the static method \"get_fitness_table()\"")

    @staticmethod
    def get_fitness_table() -> {}:
        if not FitnessTable.fitness_table:
            FitnessTable.init_fitness_table()

        return FitnessTable.fitness_table

    @staticmethod
    def init_fitness_table():
        max_cell = 16
        values = range(max_cell + 1)
        fitness_table = FitnessTable.fitness_table

        for cell_1 in values:
            for cell_2 in values:
                for cell_3 in values:
                    for cell_4 in values:
                        row = cell_1, cell_2, cell_3, cell_4
                        fitness_table[row] = FitnessTableEntry(row)


class FitnessTableEntry:
    def __init__(self, row: ()):
        SCORE_LOST_PENALTY = 200000.0
        SCORE_MONOTONICITY_POWER = 4.0
        SCORE_MONOTONICITY_WEIGHT = 47.0
        SCORE_SUM_POWER = 3.5
        SCORE_SUM_WEIGHT = 11.0
        SCORE_MERGES_WEIGHT = 700.0
        SCORE_EMPTY_WEIGHT = 270.0

        progress = empty = merges = 0

        prev = counter = 0
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

        monotonicity_left = monotonicity_right = 0
        for i in range(1, len(row)):
            if row[i - 1] > row[i]:
                monotonicity_left += pow(row[i - 1], SCORE_MONOTONICITY_POWER) - pow(row[i], SCORE_MONOTONICITY_POWER)
            else:
                monotonicity_right += pow(row[i], SCORE_MONOTONICITY_POWER) - pow(row[i - 1], SCORE_MONOTONICITY_POWER)

        self.fitness = SCORE_LOST_PENALTY \
                       + SCORE_EMPTY_WEIGHT * empty \
                       + SCORE_MERGES_WEIGHT * merges \
                       - SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right) \
                       - SCORE_SUM_WEIGHT * progress
