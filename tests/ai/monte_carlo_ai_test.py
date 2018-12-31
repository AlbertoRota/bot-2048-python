import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.monte_carlo_ai import MonteCarloAi


class TestMonteCarloAi(unittest.TestCase):
    def test_monte_carlo_ai(self):
        ai = MonteCarloAi(runs=15)
        Benchmark.run(ai, max_secs=10)
