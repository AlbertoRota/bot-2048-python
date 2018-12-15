from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi


def main():
    print("Random AI:")
    Benchmark.run(RandomAi)
    print()

    print("Ordered AI:")
    Benchmark.run(OrderedAi)
    print()


if __name__ == '__main__':
    main()
