import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.monte_carlo_ai import MonteCarloAi


class TestGameMethods(unittest.TestCase):
    def test_random_ai(self):
        print("MonteCarlo AI:")
        Benchmark.run(MonteCarloAi, board_size=3, max_secs=10)
        print()
