from bot.benchmark.benchmark import Benchmark
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi
from bot.ai.greedy_ai import GreedyAi
from bot.ai.expect_min_max_ai import ExpectMinMaxAi
from bot.ai.simple_expect_min_max_ai import SimpleExpectMinMaxAi
from bot.ai.monte_carlo_ai import MonteCarloAi
from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi


def main():
    Benchmark.run(RandomAi(), board_size=4, max_secs=10)
    Benchmark.run(OrderedAi(), board_size=4, max_secs=10)
    Benchmark.run(GreedyAi(), board_size=4, max_secs=10)

    Benchmark.run(ExpectMinMaxAi(search_depth=5), board_size=4, max_secs=10)
    Benchmark.run(SimpleExpectMinMaxAi(search_depth=7, min_chance=0.05, max_acc_chance=0.5), board_size=4, max_secs=10)

    Benchmark.run(MonteCarloAi(runs=200), board_size=4, max_secs=10)
    Benchmark.run(TimedMonteCarloAi(max_runs=400, max_sec=0.25), board_size=4, max_secs=10)


if __name__ == '__main__':
    main()
