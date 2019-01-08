class Fitness2048:

    @staticmethod
    def eval_row_monotone(row):
        row_cells = len(row)

        left_row = row
        left_score, left_consecutive = 0, 0
        for i in range(row_cells - 1):
            if left_row[i] and left_row[i] >= left_row[i + 1]:
                left_consecutive += 1
                left_score += left_consecutive ** 2 * 4
            else:
                left_score -= abs(left_row[i] - left_row[i + 1]) * 1.5
                left_consecutive = 0

        right_row = list(reversed(row))
        right_score, right_consecutive = 0, 0
        for i in range(row_cells - 1):
            if right_row[i] and right_row[i] >= right_row[i + 1]:
                right_consecutive += 1
                right_score += right_consecutive ** 2 * 4
            else:
                right_score -= abs(right_row[i] - right_row[i + 1]) * 1.5
                right_consecutive = 0

        return max(left_score, right_score)

    @staticmethod
    def eval_row_smoothness(row):
        row_cells = len(row)
        score_smooth = 0

        for i in range(row_cells - 1):
                score_smooth -= abs((row[i] or 2) - (row[i + 1] or 2))

        return score_smooth

    @staticmethod
    def eval_free(grid):
        free = 0
        grid_cells = len(grid) * len(grid[0])
        for row in grid:
            for cell in row:
                if cell == 0:
                    free += 1
        return -(grid_cells - free) ** 2

    @staticmethod
    def eval_snake(grid):
        snake = []
        for i, col in enumerate(zip(*grid)):
            snake.extend(reversed(col) if i % 2 == 0 else col)

        m = max(snake)
        return sum(x / 10 ** n for n, x in enumerate(snake)) - ((grid[3][0] != m) * abs(grid[3][0] - m)) ** 2
