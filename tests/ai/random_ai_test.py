import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi


class TestGameMethods(unittest.TestCase):
    def test_random_ai(self):
        print("Random AI:")
        Benchmark.run(RandomAi, max_secs=10, parallel=False)
        print()
