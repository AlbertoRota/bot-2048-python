import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.greedy_ai import GreedyAi


class TestGameMethods(unittest.TestCase):
    def test_random_ai(self):
        print("Greedy AI:")
        Benchmark.run(GreedyAi, max_secs=10, parallel=False)
        print()
