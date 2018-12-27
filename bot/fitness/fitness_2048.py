class Fitness2048:
    @staticmethod
    def calculate_fitness(grid: [[int]], moves: [int]) -> float:
        if not moves:
            return -float("inf")

        score_monotone = Fitness2048.eval_monotone(grid)
        score_smooth = Fitness2048.eval_smoothness(grid)
        score_free = Fitness2048.eval_free(grid)

        score = 0
        score += score_smooth
        score += score_monotone
        score += score_free

        return score

    @staticmethod
    def eval_monotone(grid):
        grid_rows = len(grid)
        grid_cols = len(grid[0])

        left = right = 0
        for x in range(grid_rows):
            m = 0
            for y in range(grid_cols - 1):
                if grid[x][y] and grid[x][y] >= grid[x][y + 1]:
                    m += 1
                    left += m ** 2 * 4
                else:
                    left -= abs((grid[x][y] or 0) - (grid[x][y + 1] or 0)) * 1.5
                    m = 0

            m = 0
            for y in range(grid_cols - 1):
                if grid[x][y] <= grid[x][y + 1] and grid[x][y + 1]:
                    m += 1
                    right += m ** 2 * 4
                else:
                    right -= abs((grid[x][y] or 0) - (grid[x][y + 1] or 0)) * 1.5
                    m = 0
        left_right = max(left, right)

        up = down = 0
        for y in range(grid_cols):
            m = 0
            for x in range(grid_rows - 1):
                if grid[x][y] and grid[x][y] >= grid[x + 1][y]:
                    m += 1
                    up += m ** 2 * 4
                else:
                    up -= abs((grid[x][y] or 0) - (grid[x + 1][y] or 0)) * 1.5
                    m = 0

            m = 0
            for x in range(grid_rows - 1):
                if grid[x][y] <= grid[x + 1][y] and grid[x + 1][y]:
                    m += 1
                    down += m ** 2 * 4
                else:
                    down -= abs((grid[x][y] or 0) - (grid[x + 1][y] or 0)) * 1.5
                    m = 0
        up_down = max(up, down)

        return left_right + up_down

    @staticmethod
    def eval_smoothness(grid):
        grid_rows = len(grid)
        grid_cols = len(grid[0])

        score_smooth = 0
        for x in range(grid_rows):
            for y in range(grid_cols):
                s = 99999999999
                if x > 0:
                    s = min(s, abs((grid[x][y] or 2) - (grid[x - 1][y] or 2)))
                if y > 0:
                    s = min(s, abs((grid[x][y] or 2) - (grid[x][y - 1] or 2)))
                if x < grid_rows - 1:
                    s = min(s, abs((grid[x][y] or 2) - (grid[x + 1][y] or 2)))
                if y < grid_cols - 1:
                    s = min(s, abs((grid[x][y] or 2) - (grid[x][y + 1] or 2)))
                score_smooth -= s
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
