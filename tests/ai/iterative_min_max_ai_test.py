import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.iterative_deepenig_min_max_ai import IterativeDeepeningMinMaxAi


class TestIterativeDeepeningExpectMinMaxAi(unittest.TestCase):
    def test_iterative_deepenig_min_max_ai(self):
        ai = IterativeDeepeningMinMaxAi(max_sec=0.01)
        Benchmark.run(ai, max_secs=10)
