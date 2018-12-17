import time
import multiprocessing as mp
from collections import Counter

import numpy as np
from bot.ai.ai_abc import AiAbc
from bot.game.board import Board


class Benchmark(object):

    @staticmethod
    def run(ai: AiAbc, max_runs: int = 100, max_secs: int = 300, parallel: bool = True):
        accumulated_score = 0
        accumulated_moves = 0
        max_tiles = Counter()
        runs = 0
        real_secs = 0
        game_secs = 0

        if parallel:
            pool = mp.Pool(mp.cpu_count())

        while runs < max_runs and real_secs <= max_secs:
            real_start = time.time()

            if parallel:
                results = [pool.apply_async(Benchmark.__run_game__, args=(ai,)) for _ in range(mp.cpu_count())]
                outputs = [p.get() for p in results]
            else:
                outputs = [Benchmark.__run_game__(ai)]

            real_secs += time.time() - real_start

            for output in outputs:
                board, num_of_movements, elapsed_time = output

                runs += 1
                game_secs += elapsed_time
                accumulated_score += board.score
                accumulated_moves += num_of_movements

                max_tiles[max(map(max, board.grid))] += 1

            print("\r", end="", flush=True)
            print("Played {} games, {:4.2f}%, ETA: {} seconds)".format(
                runs,
                100 * runs / max_runs,
                int(((game_secs / runs) * (max_runs - runs)) / mp.cpu_count())
            ), end="", flush=True)

        print("\r", end="", flush=True)
        print("Runs: " + str(runs))
        print("Real secs: {0:.2f}".format(round(real_secs)))
        print("Game secs: {0:.2f}".format(round(game_secs)))
        print("Avg score: {0:.2f}".format(round(accumulated_score / runs)))
        print("Avg moves: {0:.2f}".format(round(accumulated_moves / runs)))
        print("Moves per sec: {0:.2f}".format(round(accumulated_moves / game_secs)))
        print("Max tile distribution: ")
        for number, times in sorted(max_tiles.items()):
            print(str(number) + ": " + str(times) + " - ({0:.2f}%)".format((times/runs)*100))

    @staticmethod
    def __run_game__(ai: AiAbc) -> (Board, int, float):
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

        return board, num_of_movements, time.time() - start_time
