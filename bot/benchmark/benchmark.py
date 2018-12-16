import sys
import time
from collections import Counter

import numpy as np
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class Benchmark(object):

    @staticmethod
    def run(ai: AiAbc, max_runs: int = 100, max_secs: int = 300):
        accumulated_score = 0
        accumulated_moves = 0
        max_tiles = Counter()
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
            max_tiles[max(map(max, board.grid))] += 1
            print("\r", end="", flush=True)
            print("Played {} games, {:4.2f}%, ETA: {} seconds)".format(
                runs,
                100 * runs/max_runs,
                int((secs / runs) * (max_runs - runs))
            ), end="", flush=True)

        print("Runs: " + str(runs))
        print("Secs: " + str(secs))
        print("Avg score: " + str(accumulated_score / runs))
        print("Avg moves: " + str(accumulated_moves / runs))
        print("Moves per sec: " + str(accumulated_moves / secs))
        print("Max tile distribution: ")
        for number, times in max_tiles.items():
            print(str(number) + ": " + str(times))
