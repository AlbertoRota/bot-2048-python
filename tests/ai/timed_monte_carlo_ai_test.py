import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.benchmark.benchmark import Benchmark
from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi


class TestTimedMonteCarloAi(unittest.TestCase):
    def test_monte_carlo_ai(self):
        ai = TimedMonteCarloAi(max_sec=0.01)
        Benchmark.run(ai, max_secs=10)
