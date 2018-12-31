import time
from collections import Counter

from bot.ai.ai_abc import AiAbc
from bot.game.board_abc import BoardABC
from bot.game.board_2048 import Board2048


class Benchmark(object):

    @staticmethod
    def run(ai: AiAbc, max_runs: int = 100, max_secs: int = 300):
        # Initialize variables
        runs, secs = 0, 0
        acc_score, acc_moves = 0, 0
        max_tiles = Counter()
        print("AI: " + str(ai))

        # Run all possible games
        while runs < max_runs and secs <= max_secs:
            # Run one game
            start = time.time()
            output = Benchmark.__run_game__(ai)
            secs += time.time() - start

            # Add game results to the accumulated ones
            board, num_of_movements = output
            runs += 1
            acc_score += board.score
            acc_moves += num_of_movements
            max_tiles[max(map(max, board.grid))] += 1

            # Print progress
            print("\r", end="", flush=True)
            print("Played {} games, {:.2f}%, ETA: {:.2f} seconds)".format(
                runs, 100 * runs / max_runs, (secs / runs) * (max_runs - runs)
            ), end="", flush=True)

        # Print final results
        print("\r", end="", flush=True)
        print("Runs: {0} - Secs: {1:.2f} - Avg score: {2:.2f} - Avg moves: {3:.2f} - Moves/sec: {4:.2f}".format(
            runs, secs, acc_score / runs, acc_moves / runs, acc_moves / secs
        ))
        for number, times in sorted(max_tiles.items()):
            print(str(number) + ": " + str(times) + " - ({0:.2f}%)".format((times/runs)*100))
        print(flush=True)

    @staticmethod
    def __run_game__(ai: AiAbc) -> (BoardABC, int, float):
        # Initialize variables
        num_of_movements = 0
        board = Board2048(initialize=True)

        # Run a game to it's end
        while board.get_moves():
            board.do_move(ai.get_next_move(board), spawn_tile=True)
            num_of_movements += 1

        # Return relevant info
        return board, num_of_movements
