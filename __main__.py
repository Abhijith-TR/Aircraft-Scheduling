from copy import deepcopy
import time
import sys
from typing import Any

import matplotlib.pyplot as plt
from regex import F
from optimisation.bee_colony_optimiser import BeeColonyOptimiser
from problem.acs import ACS
from problem.rhc_solver import RHCSolver
from utils.input import make_input_from_csv, read_input


def generate_and_save_plot(x, y, title, x_label, y_label, file_name):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(file_name)
    plt.close()


def generate_results(
    asp: ACS,
    optimizer,
    optimizer_args: dict[str, Any],
    changing_param: str,
    lower_limit: int,
    upper_limit: int,
    step: int,
    with_rhc: bool = True,
):
    time_array = []
    cost = []

    for param in range(lower_limit, upper_limit, step):
        print(changing_param, ":", param, end=' ')
        optimizer_args[changing_param] = param
        fitness = 0
        total_time = 0
        for _ in range(10):
            start = time.perf_counter()
            if with_rhc:
                solution = RHCSolver(
                    asp, 30 * 60, 2, optimizer, optimizer_args
                ).optimise()
            else:
                solution = optimizer(asp, **optimizer_args).optimise()
            end = time.perf_counter()
            total_time += end - start
            fitness += solution.fitness
        print("Fitness :", fitness / 10, "Total time :", total_time / 10)
        time_array.append(total_time / 10)
        cost.append(fitness / 10)

    print(time_array)
    print(cost)
    x = list(range(lower_limit, upper_limit, step))
    file_name = f"{str(with_rhc)}_{changing_param}"
    generate_and_save_plot(
        x, time_array, "BCO Time", changing_param, "Time", f"./images/{file_name}_time.png"
    )
    generate_and_save_plot(
        x, cost, "BCO Cost", changing_param, "Cost", f"./images/{file_name}_cost.png"
    )


def main():
    make_input_from_csv("./dataset/ikli_codes/alp_7_50.csv", num_runways=3)
    ac_input = read_input()
    asp = ACS(*ac_input)
    print(asp)

    bco_args = {
        "number_of_bees": 500,
        "max_iter": 100,
        "trial_limit": 10,
        "max_scouts": 1,
    }

    # bco_args_copy = deepcopy(bco_args)
    # # Graphs for BCO while changing number of bees
    # generate_results(
    #     asp, BeeColonyOptimiser, bco_args_copy, "number_of_bees", 10, 501, 10, with_rhc=False
    # )
    # generate_results(
    #     asp, BeeColonyOptimiser, bco_args_copy, "number_of_bees", 10, 501, 10, with_rhc=True
    # )

    # bco_args_copy = deepcopy(bco_args)
    # # Graphs for BCO while changing max_iter
    # generate_results(
    #     asp, BeeColonyOptimiser, bco_args_copy, "max_iter", 10, 101, 5, with_rhc=True
    # )

    bco_args_copy = deepcopy(bco_args)
    # Graphs for BCO while changing trial_limit
    generate_results(
        asp, BeeColonyOptimiser, bco_args_copy, "trial_limit", 1, 26, 1, with_rhc=True
    )

    # bco_args_copy = deepcopy(bco_args)
    # # Graphs for BCO while changing max_scouts
    # generate_results(
    #     asp, BeeColonyOptimiser, bco_args_copy, "max_scouts", 1, 11, 1, with_rhc=True
    # )

if __name__ == "__main__":
    main()
    sys.exit(0)

    # ga_args = {"population_size": 50, "generations": 500}

    # fcfs_args = {}

    # print("bco")

    # without rhc the same thing - Done
    # rhc window 5, 10, 15, 20, 25, 30
    # number of iterations 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 - Done
    # initial ordering of aircrafts
    # number of runways
    # changing the maximum trials allowed for a single solution - Done
    # changing the number of scouts - Done
    # badi table with landing times
