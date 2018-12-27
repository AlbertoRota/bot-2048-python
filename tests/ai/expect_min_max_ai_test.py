import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.expect_min_max_ai import ExpectMinMaxAi


class TestGameMethods(unittest.TestCase):
    def test_random_ai(self):
        print("ExpectMinMax AI:")
        Benchmark.run(ExpectMinMaxAi, board_size=3, max_secs=10)
        print()
