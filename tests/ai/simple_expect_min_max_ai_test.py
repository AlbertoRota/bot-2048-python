import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi


class TestSimpleExpectMinMaxAi(unittest.TestCase):
    def test_simple_expect_min_max_ai(self):
        ai = SimpleExpectMinMaxAi(depth=3, min_chance=0.05, max_acc_chance=0.3)
        Benchmark.run(ai, max_secs=10)
