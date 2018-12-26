import multiprocessing as mp

from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi
from bot.ai.greedy_ai import GreedyAi
from bot.ai.expect_min_max_ai import ExpectMinMaxAi
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi
from bot.ai.monte_carlo_ai import MonteCarloAi
from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi


def main():
    mp.freeze_support()

    # print("Random AI:")
    # Benchmark.run(RandomAi, max_secs=10, parallel=False)
    # print()
    #
    # print("Ordered AI:")
    # Benchmark.run(OrderedAi, max_secs=10, parallel=False)
    # print()
    #
    # print("Greedy AI:")
    # Benchmark.run(GreedyAi, max_secs=10, parallel=False)
    # print()
    #
    print("ExpectMinMax AI:")
    Benchmark.run(ExpectMinMaxAi, max_secs=10, parallel=False)
    print()

    print("SimpleExpectMinMax AI:")
    Benchmark.run(SimpleExpectMinMaxAi, max_secs=10, parallel=False)
    print()

    print("NewMonteCarlo AI:")
    Benchmark.run(MonteCarloAi, max_secs=10, parallel=False)
    print()

    print("TimedMonteCarlo AI:")
    Benchmark.run(TimedMonteCarloAi, max_secs=10, parallel=False)
    print()


if __name__ == '__main__':
    main()
