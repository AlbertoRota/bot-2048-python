from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi
from bot.ai.greedy_ai import GreedyAi
from bot.ai.expect_min_max_ai import ExpectMinMaxAi
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi
from bot.ai.iterative_deepenig_expect_min_max_ai import IterativeDeepeningExpectMinMaxAi
from bot.ai.monte_carlo_ai import MonteCarloAi
from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi


def main():
    # Benchmark.run(RandomAi(), max_runs=10)
    # Benchmark.run(OrderedAi(), max_runs=10)
    # Benchmark.run(GreedyAi(), max_runs=10)

    # Benchmark.run(ExpectMinMaxAi(search_depth=5), max_runs=10)
    # Benchmark.run(SimpleExpectMinMaxAi(search_depth=7, min_chance=0.05, max_acc_chance=0.75), max_runs=10)
    Benchmark.run(IterativeDeepeningExpectMinMaxAi(max_depth=20, max_sec=0.5), max_runs=1)

    # Benchmark.run(MonteCarloAi(runs=1000), max_runs=10)
    # Benchmark.run(TimedMonteCarloAi(max_runs=999999, max_sec=1), max_runs=10)


if __name__ == '__main__':
    main()
