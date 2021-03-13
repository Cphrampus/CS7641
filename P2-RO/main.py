import sys
from datetime import datetime
import matplotlib
import mlrose_hiive
from sklearn.model_selection import train_test_split

matplotlib.use("TKAgg")

import matplotlib.pyplot as plt
from mlrose_hiive import NeuralNetwork, random_hill_climb, simulated_annealing, genetic_alg, mimic, FlipFlop, SixPeaks, \
    Queens, DiscreteOpt, FourPeaks, MaxKColorGenerator, MaxKColor, SARunner, QueensGenerator, GeomDecay
import numpy as np
import time
from sklearn.metrics import accuracy_score

random_states = [0,50,800,35]


# def average_curves(fit_curves):
#     length = max([len(curve) for curve in fit_curves])
#     return np.stack([
#         np.pad(curve, (0, length - len(curve)), 'edge')
#         for curve in fit_curves
#     ]).mean(axis=0)


# TODO make 3 versions of each function, 1 for each problem
# just call each set of algos for each problem, each can be tuned
#    need HP tuning charts? think so, double check notes
#    tuning by grid search, mlrose equiv? or just plot fitness over a range of values for an HP that should affect it?
# probably need 3 sizes of problem for each? small, medium, large? check notes
#    would run algo for each size and plot fitness to size, maybe all algos on one plot for space

def run_RHC_1(problem, init_state, **kwargs):
    fit_vals = []
    # fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()
        _, best_fit, _, evals = random_hill_climb(problem, random_state=random_state, restarts=100, max_attempts=12,
                                                  **kwargs, curve=True, fevals=True, init_state=init_state)

        fit_vals.append(best_fit)
        # fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))

    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/rhc_{problem_name}_{len(init_state)}_{dt_string}"
    #
    # plt.plot(average_curves(fit_curves), label="rhc")
    # plt.title(f"RHC {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"RHC {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_GA_1(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()
        _, best_fit, fit_curve, evals = genetic_alg(problem, random_state=random_state, curve=True,fevals=True,
                                                    pop_size=120, mutation_prob=0.12, **kwargs)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))

    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/ga_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="ga")
    # plt.title(f"GA {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"GA {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_MIMIC_1(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()

        _, best_fit, fit_curve, evals = mimic(problem, random_state=random_state, pop_size=150, keep_pct=0.15,
                                              **kwargs, curve=True, fevals=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))


    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/mimic_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="mimic")
    # plt.title(f"MIMIC {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"MIMIC {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_SA_1(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []


    # run multiple times to get average
    for random_state in random_states:
        start = time.time()

        _, best_fit, fit_curve, evals = simulated_annealing(problem, random_state=random_state, curve=True,
                                                   init_state=init_state, fevals=True, **kwargs)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))


    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/sa_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="sa")
    # plt.title(f"SA {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"SA {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_RHC_2(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()
        _, best_fit, fit_curve, evals = random_hill_climb(problem, random_state=random_state, restarts=35,
                                                          **kwargs, curve=True,fevals=True,  init_state=init_state)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))

    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/rhc_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="rhc")
    # plt.title(f"RHC {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"RHC {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_GA_2(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()
        _, best_fit, fit_curve, evals = genetic_alg(problem, random_state=random_state, pop_size=210, mutation_prob=0.23,
                                                    **kwargs,fevals=True,  curve=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))

    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/ga_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="ga")
    # plt.title(f"GA {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"GA {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_MIMIC_2(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()

        _, best_fit, fit_curve, evals = mimic(problem, random_state=random_state, pop_size=300, keep_pct=0.2,
                                              **kwargs,fevals=True,  curve=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))


    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/mimic_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="mimic")
    # plt.title(f"MIMIC {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"MIMIC {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_SA_2(problem, init_state, **kwargs):
    start = time.time()
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []


    # run multiple times to get average
    for random_state in random_states:
        start = time.time()

        _, best_fit, fit_curve, evals = simulated_annealing(problem, random_state=random_state, **kwargs, curve=True,fevals=True,
                                                   init_state=init_state, schedule=GeomDecay(init_temp=11, decay=0.96))

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))


    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/sa_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="sa")
    # plt.title(f"SA {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"SA {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_RHC_3(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()
        _, best_fit, fit_curve, evals = random_hill_climb(problem, random_state=random_state, restarts=39,
                                                          **kwargs, curve=True, init_state=init_state, fevals=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))

    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/rhc_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="rhc")
    # plt.title(f"RHC {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"RHC {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_GA_3(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()
        _, best_fit, fit_curve, evals = genetic_alg(problem, random_state=random_state, pop_size=170, mutation_prob=0.82,
                                                    **kwargs, curve=True, fevals=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))

    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/ga_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="ga")
    # plt.title(f"GA {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"GA {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_MIMIC_3(problem, init_state, **kwargs):
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []

    # run multiple times to get average
    for random_state in random_states:
        start = time.time()

        _, best_fit, fit_curve, evals = mimic(problem, random_state=random_state, pop_size=275,
                                              **kwargs, curve=True, fevals=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))


    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/mimic_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="mimic")
    # plt.title(f"MIMIC {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"MIMIC {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_SA_3(problem, init_state, **kwargs):
    start = time.time()
    fit_vals = []
    fit_curves = []
    times = []
    fevals = []


    # run multiple times to get average
    for random_state in random_states:
        start = time.time()

        _, best_fit, fit_curve, evals = simulated_annealing(problem, random_state=random_state, schedule=GeomDecay(decay=0.94),
                                                            **kwargs, curve=True, init_state=init_state, fevals=True)

        fit_vals.append(best_fit)
        fit_curves.append(fit_curve)
        times.append(time.time() - start)
        fevals.append(sum(evals.values()))


    # plot average fitness value
    # now = datetime.now()
    # dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    # hack for ease of naming
    problem_name = str(problem.fitness_fn).split('.')[-1].split(' ')[0]
    # chart_name = f"charts/sa_{problem_name}_{len(init_state)}_{dt_string}"

    # plt.plot(average_curves(fit_curves), label="sa")
    # plt.title(f"SA {problem_name} ({len(init_state)})")
    # plt.xlabel("step")
    # plt.ylabel("fitness")
    # plt.savefig(chart_name)
    # plt.show()

    avg_fit = np.average(fit_vals)
    avg_time = round(np.mean(times), 2)
    avg_evals = np.mean(fevals)
    print(f"SA {problem_name}: {avg_fit}: {avg_time}: {avg_evals}")
    return avg_fit, avg_time, avg_evals


def run_ANN():
    # TODO use multiple random states and average values

    with open("data/wine.csv", 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:, :-1], data[:, -1]

    # split for training and testing
    data_train, data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    random_state = 0
    net = NeuralNetwork(hidden_nodes=[290], max_iters=110, algorithm="gradient_descent", curve=True,
                                          learning_rate=0.001, random_state=random_state)

    net.fit(data_train, label_train)

    label_pred = net.predict(data_train)

    train_accuracy = accuracy_score(label_train, label_pred)

    label_pred = net.predict(data_test)

    test_accuracy = accuracy_score(label_test, label_pred)




def run_ANN_RHC():
    # TODO use multiple random states and average values
    random_state = 0
    _, loss, _, fit_curve = NeuralNetwork(algorithm="random_hill_climb", curve=True, random_state=random_state)


def run_ANN_SA():
    # TODO use multiple random states and average values
    random_state = 0
    _, loss, _, fit_curve = NeuralNetwork(algorithm="simulated_annealing", curve=True, random_state=random_state)


def run_ANN_GA():
    # TODO use multiple random states and average values
    random_state = 0
    _, loss, _, fit_curve = NeuralNetwork(algorithm="genetic_alg", curve=True, random_state=random_state)


if __name__ == "__main__":
    # TODO need to break these and the functions up, since each has to be tuned to problem
    # TODO switch plotting to be only average score per problem, then the chart will be fitness over problem size
    np.random.seed(0)

    # for each problem size
    #   generate problem of size
    #   for each algo
    #       for each random state
    #           use algo runner on problem with state as seed
    #           get best fitness value, min or max depending on problem
    #       average fitness values together for algo
    #       dump average time to value
    #       dump function evals
    #   add average to list for algo
    # plot fitness per algo per problem size

    # stick with current method, easier to understand, maybe using mlrose for problems like in kcolor
    # need to tune about 5 algos a day to leave a good chunk of time for the paper
    # tune
    # RHC -> none
    # SA -> starting temp
    # GA -> Crossover?
    # mimic -> pop size? keep_pct?

    # need to run function across space of parameter and graph MC curve to tune parameter
    # average using same random state stuff as now
    # adjust run functions to take kwargs and that passed down
    # call function for each value in range, get fitness, add to plot
    # show plot, evaluate necessary value
    # mlrose grid search doesn't seem too helpful, so just coarse MC curve and narrow on areas for tuning, need the curves for report anyway

    # problem 1
    init_states = [
        np.random.randint(0, 8, 8),
        # np.random.randint(0, 15, 15),
        np.random.randint(0, 36, 36),
        np.random.randint(0, 50, 50)
    ]
    # plt.figure()
    fit_func = Queens()

    # calls for tuning
    # get medium size
    init_state = init_states[1]
    problem = DiscreteOpt(length=len(init_state), fitness_fn=fit_func, maximize=False)
    # problem = MaxKColorGenerator().generate(seed=123, number_of_nodes=len(init_state),
    #                                         max_connections_per_node=4, max_colors=None)

    # plt.figure()
    # plt.title("RHC restarts")
    # plt.xlabel("allowed restarts")
    # plt.ylabel("fitness")
    # values = []
    # fitness = []
    # evals = []
    # times = []
    # for pop_size in range(0, 51):
    #     values.append(pop_size)
    #     print(pop_size)
    #     fit, _, fevals = run_RHC_3(problem, init_state, restarts=pop_size)
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/RHC3_restarts")

    # plt.figure()
    # plt.title("SA initial temperature")
    # plt.xlabel("initial temp")
    # plt.ylabel("fitness")
    # values = []
    # fitness = []
    # evals = []
    # times = []
    # for pop_size in range(1, 21):
    #     values.append(pop_size)
    #     print(pop_size)
    #     fit, _, fevals = run_SA_3(problem, init_state, schedule=GeomDecay(decay=0.94, init_temp=pop_size))
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/SA3_init_temp_with_decay")

    # plt.figure()
    # plt.title("SA decay")
    # plt.xlabel("decay rate")
    # plt.ylabel("fitness")
    # values = []
    # fitness = []
    # evals = []
    # times = []
    #
    # for decay in np.linspace(0.01, 0.99,99):
    #     decay = round(decay, 3)
    #     values.append(decay)
    #     print(decay)
    #     fit, _, fevals = run_SA_3(problem, init_state, schedule=GeomDecay(decay=decay))
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/SA3_decay")

    # plt.figure()
    # plt.title("GA population size")
    # plt.xlabel("pop size")
    # plt.ylabel("fitness")
    # values = []
    # fitness = []
    # evals = []
    # times = []
    # for pop_size in range(100, 310, 10):
    #     values.append(pop_size)
    #     print(pop_size)
    #     fit, _, fevals = run_GA_3(problem, init_state, pop_size=pop_size)
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/GA3_pop_size")

    # plt.figure()
    # plt.title("GA mutation probability")
    # plt.xlabel("mutation prob")
    # plt.ylabel("fitness")
    #
    # values = []
    # fitness = []
    # evals = []
    # times = []
    #
    # for decay in np.linspace(0.01, 0.99,99):
    #     decay = round(decay, 3)
    #     values.append(decay)
    #     print(decay)
    #     fit, _, fevals = run_GA_3(problem, init_state, mutation_prob=decay)
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/GA3_mutation_prob_pop_170")
    #
    # plt.figure()
    # plt.title("MIMIC population size")
    # plt.xlabel("pop size")
    # plt.ylabel("fitness")
    # values = []
    # fitness = []
    # evals = []
    # times = []
    # for pop_size in range(280, 410, 10):
    #     values.append(pop_size)
    #     print(pop_size)
    #     fit, _, fevals = run_MIMIC_3(problem, init_state, pop_size=pop_size)
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/MIMIC3_pop_size_300+")
    #
    # plt.figure()
    # plt.title("MIMIC keep percentage")
    # plt.xlabel("keep %")
    # plt.ylabel("fitness")
    # values = []
    # fitness = []
    # evals = []
    # times = []
    #
    # for decay in np.linspace(0.01, 0.50,50):
    #     decay = round(decay, 3)
    #     values.append(decay)
    #     print(decay)
    #     fit, _, fevals = run_MIMIC_3(problem, init_state, pop_size=275, keep_pct=decay)
    #     fitness.append(fit)
    #     evals.append(fevals)
    #
    # plt.plot(values, fitness)
    # plt.savefig("charts/MIMIC3_keep_pct_pop_275")
    #
    #
    #
    #
    # plt.show()
    # print()

    # run_GA_1(problem, init_state)
    # run_MIMIC_1(problem, init_state)

    # plot fevals over problem sizes
    # lens = [len(init_state) for init_state in init_states]
    # RHC_vals = []
    # SA_vals = []
    # GA_vals = []
    # MIMIC_vals = []
    # for init_state in init_states:
    #     problem = MaxKColorGenerator().generate(seed=123, number_of_nodes=len(init_state),
    #                                             max_connections_per_node=4, max_colors=None)
    #     # RHC_vals.append(
    #     fit,_,evals = run_RHC_1(problem, init_state)
    #     RHC_vals.append(fit)
    #     # )
    #     # SA_vals.append(
    #     fit,_,evals = run_SA_1(problem, init_state)
    #     SA_vals.append(fit)
    #     # )
    #     # GA_vals.append(
    #     fit,_,evals = run_GA_1(problem, init_state)
    #     GA_vals.append(fit)
    #     # )
    #     # MIMIC_vals.append(
    #     fit,_,evals = run_MIMIC_1(problem, init_state)
    #     MIMIC_vals.append(fit)
    #     #)
    # plt.plot(lens, RHC_vals, label="rhc")
    # plt.plot(lens, SA_vals, label="sa")
    # plt.plot(lens, GA_vals, label="ga")
    # plt.plot(lens, MIMIC_vals, label="mimic")
    #
    # print()
    # problem_name = str(fit_func).split('.')[-1].split(' ')[0]
    # plt.title(problem_name)
    # plt.xlabel("problem size")
    # plt.ylabel("fitness")
    # plt.legend()
    # plt.savefig(f"charts/{problem_name}")
    # plt.show()
    # plt.close('all')

    # problem 2
    # init_state = init_states = [
    #     np.random.randint(0, 2, 10),
    #     np.random.randint(0, 2, 30),
    #     np.random.randint(0, 2, 50),
    #     # np.random.randint(0, 2, 100) # mimic takes a long time to run, will need to run overnight
    # ]
    # # plt.figure()
    # fit_func = SixPeaks()
    #
    # # calls for tuning
    # # get medium size
    # # init_state = init_states[1]
    # # problem = DiscreteOpt(length=len(init_state), fitness_fn=fit_func)
    # # run_RHC_2(problem, init_state)
    # # run_SA_2(problem, init_state)
    # # run_GA_2(problem, init_state)
    # # run_MIMIC_2(problem, init_state)
    #
    # # plot time over problem sizes
    # lens = [len(init_state) for init_state in init_states]
    # RHC_vals = []
    # SA_vals = []
    # GA_vals = []
    # MIMIC_vals = []
    # RHC_times = []
    # SA_times = []
    # GA_times = []
    # MIMIC_times = []
    # for init_state in init_states:
    #     problem = DiscreteOpt(length=len(init_state), fitness_fn=fit_func)
    #     fit, duration,_ = run_RHC_2(problem, init_state)
    #     RHC_vals.append(fit)
    #     RHC_times.append(duration)
    #     fit, duration,_ = run_SA_2(problem, init_state)
    #     SA_vals.append(fit)
    #     SA_times.append(duration)
    #     fit, duration,_ = run_GA_2(problem, init_state)
    #     GA_vals.append(fit)
    #     GA_times.append(duration)
    #     fit, duration,_ = run_MIMIC_2(problem, init_state)
    #     MIMIC_vals.append(fit)
    #     MIMIC_times.append(duration)
    # plt.plot(lens, RHC_vals, label="rhc")
    # plt.plot(lens, SA_vals, label="sa")
    # plt.plot(lens, GA_vals, label="ga")
    # plt.plot(lens, MIMIC_vals, label="mimic")
    #
    # print()
    # problem_name = str(fit_func).split('.')[-1].split(' ')[0]
    # plt.title(problem_name)
    # plt.xlabel("problem size")
    # plt.ylabel("fitness")
    # plt.legend()
    # plt.savefig(f"charts/{problem_name}")
    #
    # plt.figure()
    # plt.title(f"{problem_name} times")
    # plt.xlabel("problem size")
    # plt.ylabel("time (seconds)")
    # plt.plot(lens, RHC_times, label="rhc")
    # plt.plot(lens, SA_times, label="sa")
    # plt.plot(lens, GA_times, label="ga")
    # plt.plot(lens, MIMIC_times, label="mimic")
    # plt.legend()
    # plt.savefig(f"charts/{problem_name}_time")
    # plt.show()
    # plt.close('all')

    # problem 3

    init_states = [
        np.random.randint(0, 8, 8),
        # np.random.randint(0, 15, 15),
        np.random.randint(0, 36, 36),
        np.random.randint(0, 50, 50)
    ]
    # plt.figure()
    fit_func = Queens()

    # calls for tuning
    # get medium size
    # init_state = init_states[1]
    # problem = DiscreteOpt(length=len(init_state), fitness_fn=fit_func)
    # run_RHC_3(problem, init_state)
    # run_SA_3(problem, init_state)
    # run_GA_3(problem, init_state)
    # run_MIMIC_3(problem, init_state)

    # plot fitness over problem sizes
    lens = [len(init_state) for init_state in init_states]
    RHC_vals = []
    SA_vals = []
    GA_vals = []
    MIMIC_vals = []
    for init_state in init_states:
        problem = DiscreteOpt(length=len(init_state), fitness_fn=fit_func, maximize=False)
        fit, _,_ = run_RHC_3(problem, init_state)
        RHC_vals.append(fit)
        fit, _,_ = run_SA_3(problem, init_state)
        SA_vals.append(fit)
        fit, _,_ = run_GA_3(problem, init_state)
        GA_vals.append(fit)
        fit, _,_ = run_MIMIC_3(problem, init_state)
        MIMIC_vals.append(fit)
    plt.plot(lens, RHC_vals, label="rhc")
    plt.plot(lens, SA_vals, label="sa")
    plt.plot(lens, GA_vals, label="ga")
    plt.plot(lens, MIMIC_vals, label="mimic")

    print()
    problem_name = str(fit_func).split('.')[-1].split(' ')[0]
    plt.title(problem_name)
    plt.xlabel("problem size")
    plt.ylabel("fitness")
    plt.legend()
    plt.savefig(f"charts/{problem_name}")
    plt.show()
    plt.close('all')

    # ANN compare
    run_ANN()
    run_ANN_RHC()
    run_ANN_SA()
    run_ANN_GA()
