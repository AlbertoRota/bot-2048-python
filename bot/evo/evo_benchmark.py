from bot.ai.ai_abc import AiAbc
from bot.game.board_2048 import Board2048


class Benchmark(object):

    @staticmethod
    def run(ai: AiAbc) -> float:
        # Initialize variables
        runs = 0
        scores = []

        # Initialize board outside loop.
        _ = Board2048()

        # Run all possible games
        while runs < 5:
            # Run one game
            score = Benchmark.__run_game__(ai)

            # Add game results to the accumulated ones
            scores.append(score)
            runs += 1

        # Analyze final results
        scores.sort()
        return (scores[1] + scores[2] + scores[3]) / 3


    @staticmethod
    def __run_game__(ai: AiAbc) -> int:
        # Initialize variables
        board = Board2048(initialize=True)

        # Run a game to it's end
        while board.get_moves():
            board.do_move(ai.get_next_move(board), spawn_tile=True)

        # Return relevant info
        return board.score
