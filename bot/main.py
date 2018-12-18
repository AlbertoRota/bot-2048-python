import multiprocessing as mp

from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi
from bot.ai.greedy_ai import GreedyAi
from bot.ai.expect_min_max_ai import ExpectMinMaxAi
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi
from bot.ai.monte_carlo_ai import MonteCarloAi


def main():
    mp.freeze_support()

    # print("Random AI:")
    # Benchmark.run(RandomAi, max_secs=60)
    # print()

    # print("Ordered AI:")
    # Benchmark.run(OrderedAi, max_secs=60)
    # print()

    # print("Greedy AI:")
    # Benchmark.run(GreedyAi, max_secs=60, parallel=False)
    # print()

    # print("ExpectMinMax AI:")
    # Benchmark.run(ExpectMinMaxAi, max_secs=60)
    # print()

    print("SimpleExpectMinMax AI:")
    Benchmark.run(SimpleExpectMinMaxAi, max_runs=1, max_secs=60, parallel=False)
    print()

    # print("MonteCarlo AI:")
    # Benchmark.run(MonteCarloAi, max_secs=60)
    # print()


if __name__ == '__main__':
    main()
