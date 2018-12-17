import multiprocessing as mp

from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi
from bot.ai.expect_min_max_ai import ExpectMinMaxAi
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi


def main():
    mp.freeze_support()

    print("Random AI:")
    Benchmark.run(RandomAi)
    print()

    print("Ordered AI:")
    Benchmark.run(OrderedAi)
    print()

    print("ExpectMinMax AI:")
    Benchmark.run(ExpectMinMaxAi, max_secs=240)
    print()

    print("SimpleExpectMinMax AI:")
    Benchmark.run(SimpleExpectMinMaxAi, max_secs=240)
    print()


if __name__ == '__main__':
    main()
