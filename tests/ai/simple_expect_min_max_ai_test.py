import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi


class TestGameMethods(unittest.TestCase):
    def test_random_ai(self):
        print("SimpleExpectMinMax AI:")
        Benchmark.run(SimpleExpectMinMaxAi, board_size=3, max_secs=10)
        print()
