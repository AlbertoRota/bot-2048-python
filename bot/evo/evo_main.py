import operator
import random
import multiprocessing

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from bot.evo.evo_simple_expect_min_max_ai import SimpleExpectMinMaxAi
from bot.evo.evo_benchmark import Benchmark


# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


pset = gp.PrimitiveSet("MAIN", 5)

pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)

pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)

pset.addPrimitive(max, 2)
pset.addPrimitive(min, 2)

pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(operator.abs, 1)

pset.addEphemeralConstant("rand32", lambda: random.randint(-32, 32))
pset.renameArguments(
    ARG0='score_free',
    ARG1='score_monotone_lr',
    ARG2='score_monotone_ud',
    ARG3='score_smoothness_lr',
    ARG4='score_smoothness_ud'
)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def target_func(x, y):
    return y * x ** 4 + 7 * y * x ** 3 + x ** 2 + x * y ** 3


def eval_symb_reg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    # Evaluate
    ai = SimpleExpectMinMaxAi(eval_func=func)
    fitness = Benchmark.run(ai)
    return 30000 / fitness,


toolbox.register("evaluate", eval_symb_reg, points=[x / 10. for x in range(-10, 10)])
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    # random.seed(318)

    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 15, stats=mstats, halloffame=hof, verbose=True)
    # print log
    for individual in hof:
        print(individual)
    return pop, log, hof


if __name__ == "__main__":
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    toolbox.register("map", pool.map)
    main()
