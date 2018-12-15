import sys
import time

import numpy as np
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class Benchmark(object):

    @staticmethod
    def run(ai: AiAbc, max_runs: int = 100, max_secs: int = 300):
        accumulated_score = 0
        accumulated_moves = 0
        runs = 0
        secs = 0

        while runs < max_runs and secs <= max_secs:
            board = Board(np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]),
                initialize=True
            )

            start_time = time.time()
            num_of_movements = 0
            while not board.is_game_over:
                direction = ai.get_next_move(board)
                board = board.swipe_grid(direction, spawn_tile=True)
                num_of_movements += 1

            runs += 1
            secs += time.time() - start_time
            accumulated_score += board.score
            accumulated_moves += num_of_movements

        print("Runs: " + str(runs))
        print("Secs: " + str(secs))
        print("Avg score: " + str(accumulated_score / runs))
        print("Avg moves: " + str(accumulated_moves / runs))
        print("Moves per sec: " + str(accumulated_moves / secs))
