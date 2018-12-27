import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.ordered_ai import OrderedAi


class TestGameMethods(unittest.TestCase):
    def test_ordered_ai(self):
        ai = OrderedAi()
        Benchmark.run(ai, board_size=3, max_secs=10)
