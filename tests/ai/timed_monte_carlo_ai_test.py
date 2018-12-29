import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi


class TestTimedMonteCarloAi(unittest.TestCase):
    def test_monte_carlo_ai(self):
        ai = TimedMonteCarloAi(max_runs=800, max_sec=0.05)
        Benchmark.run(ai, board_size=3, max_secs=10)
