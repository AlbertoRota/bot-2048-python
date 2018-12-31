import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.expect_min_max_ai import ExpectMinMaxAi


class TestExpectMinMaxAi(unittest.TestCase):
    def test_expect_min_max_ai(self):
        ai = ExpectMinMaxAi(search_depth=2)
        Benchmark.run(ai, max_secs=10)
