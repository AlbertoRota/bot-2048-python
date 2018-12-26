import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.ordered_ai import OrderedAi


class TestGameMethods(unittest.TestCase):
    def test_ordered_ai(self):
        print("Ordered AI:")
        Benchmark.run(OrderedAi, max_secs=10, parallel=False)
        print()
