from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi
from bot.ai.greedy_ai import GreedyAi
from bot.ai.expect_min_max_ai import ExpectMinMaxAi
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi
from bot.ai.monte_carlo_ai import MonteCarloAi
from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi


def main():
    print("Random AI:")
    Benchmark.run(RandomAi, board_size=4, max_secs=10)
    print()

    print("Ordered AI:")
    Benchmark.run(OrderedAi, board_size=4, max_secs=10)
    print()

    print("Greedy AI:")
    Benchmark.run(GreedyAi, board_size=4, max_secs=10)
    print()

    print("ExpectMinMax AI:")
    Benchmark.run(ExpectMinMaxAi, board_size=4, max_secs=10)
    print()

    print("SimpleExpectMinMax AI:")
    Benchmark.run(SimpleExpectMinMaxAi, board_size=4, max_secs=10)
    print()

    print("NewMonteCarlo AI:")
    Benchmark.run(MonteCarloAi, board_size=4, max_secs=10)
    print()

    print("TimedMonteCarlo AI:")
    Benchmark.run(TimedMonteCarloAi, board_size=4, max_secs=10)
    print()


if __name__ == '__main__':
    main()
