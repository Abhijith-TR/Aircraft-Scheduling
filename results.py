from copy import deepcopy
import time
import numpy as np
import sys
from typing import Any

import matplotlib.pyplot as plt
from optimisation import optimiser
from optimisation.fcfs import FCFS
from optimisation.bee_colony_optimiser import BeeColonyOptimiser
from optimisation.ga import GeneticOptimiser
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


def generate_bco_results(
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
        print(changing_param, ":", param, end=" ")
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
        x,
        time_array,
        "BCO Time",
        changing_param,
        "Time",
        f"./images/{file_name}_time.png",
    )
    generate_and_save_plot(
        x, cost, "BCO Cost", changing_param, "Cost", f"./images/{file_name}_cost.png"
    )


def compare_optimizers(csv_filename: list[str], with_rhc: bool = False):
    number_of_aircrafts = []
    time_array = [[], [], []]
    cost = [[], [], []]

    for filename in csv_filename:
        make_input_from_csv(filename, num_runways=3)
        ac_input = read_input()
        asp = ACS(*ac_input)
        number_of_aircrafts.append(len(asp.all_ac))
        print(asp)

        bco_args = {
            "number_of_bees": 1000,
            "max_iter": 100,
            "trial_limit": 10,
            "max_scouts": 1,
        }

        genetic_args = {"population_size": 50, "generations": 500}

        optimizers = [
            RHCSolver(asp, 30 * 60, 2, BeeColonyOptimiser, bco_args),
            BeeColonyOptimiser(asp, **bco_args),
        ]

        for idx, optimiser in enumerate(optimizers):
            fitness = 0
            total_time = 0
            for _ in range(1):
                start = time.perf_counter()
                solution = optimiser.optimise()

                end = time.perf_counter()
                total_time += end - start
                fitness += solution.fitness
            print("Fitness :", fitness, "Total time :", total_time)
            time_array[idx].append(total_time)
            cost[idx].append(fitness)

    print(time_array)
    print(cost)
    x = np.arange(2, 2 + 4 * len(csv_filename), 4)
    number_of_aircrafts = np.array(number_of_aircrafts)
    plt.bar(x - 1, time_array[0], width=1, label="BCO", align="center")
    plt.bar(x, time_array[1], width=1, label="GA", align="center")
    plt.bar(x + 1, time_array[2], width=1, label="FCFS", align="center")
    plt.xticks(x, number_of_aircrafts)
    plt.xlabel("Number of aircrafts")
    plt.ylabel("Time")
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"./images/comparison_{str(with_rhc)}_time.png")

    plt.clf()
    plt.bar(x - 1, cost[0], width=1, label="BCO", align="center")
    plt.bar(x, cost[1], width=1, label="GA", align="center")
    plt.bar(x + 1, cost[2], width=1, label="FCFS", align="center")
    plt.xticks(x, number_of_aircrafts)
    plt.xlabel("Number of aircrafts")
    plt.ylabel("Cost")
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"./images/comparison_{str(with_rhc)}_cost.png")


def changing_rhc_window_results(asp: ACS):
    time_array = []
    cost = []

    for window in range(5, 61, 5):
        print("Window :", window, end=" ")
        fitness = 0
        total_time = 0
        for _ in range(10):
            start = time.perf_counter()
            solution = RHCSolver(
                asp,
                window * 60,
                2,
                BeeColonyOptimiser,
                {
                    "number_of_bees": 500,
                    "max_iter": 100,
                    "trial_limit": 10,
                    "max_scouts": 1,
                },
            ).optimise()
            end = time.perf_counter()
            total_time += end - start
            fitness += solution.fitness
        print("Fitness :", fitness / 10, "Total time :", total_time / 10)
        time_array.append(total_time / 10)
        cost.append(fitness / 10)

    print(time_array)
    print(cost)
    x = list(range(5, 61, 5))
    generate_and_save_plot(
        x, time_array, "RHC Time", "Window", "Time", "./images/rhc_time.png"
    )
    generate_and_save_plot(
        x, cost, "RHC Cost", "Window", "Cost", "./images/rhc_cost.png"
    )


def changing_runway_results(csv_filename, with_rhc: bool = False):
    time_array = []
    cost = []

    for runway in range(2, 6):
        make_input_from_csv(csv_filename, num_runways=4)
        ac_input = read_input()
        asp = ACS(*ac_input)
        print(asp)
        print("Runway :", runway, end=" ")
        fitness = 0
        total_time = 0
        for _ in range(10):
            start = time.perf_counter()
            if with_rhc:
                solution = RHCSolver(
                    asp,
                    30 * 60,
                    2,
                    BeeColonyOptimiser,
                    {
                        "number_of_bees": 500,
                        "max_iter": 100,
                        "trial_limit": 10,
                        "max_scouts": 1,
                    },
                ).optimise()
            else:
                solution = BeeColonyOptimiser(
                    asp, number_of_bees=500, max_iter=100, trial_limit=10, max_scouts=1
                ).optimise()
            end = time.perf_counter()
            total_time += end - start
            fitness += solution.fitness
        print("Fitness :", fitness / 10, "Total time :", total_time / 10)
        time_array.append(total_time / 10)
        cost.append(fitness / 10)

    print(time_array)
    print(cost)
    x = list(range(2, 6))
    generate_and_save_plot(
        x, time_array, "Runway Time", "Runway", "Time", "./images/runway_time.png"
    )
    generate_and_save_plot(
        x, cost, "Runway Cost", "Runway", "Cost", "./images/runway_cost.png"
    )


def get_bco_results(asp: ACS):
    bco_args = {
        "number_of_bees": 500,
        "max_iter": 100,
        "trial_limit": 10,
        "max_scouts": 1,
    }

    bco_args_copy = deepcopy(bco_args)
    # Graphs for BCO while changing number of bees
    generate_bco_results(
        asp,
        BeeColonyOptimiser,
        bco_args_copy,
        "number_of_bees",
        10,
        501,
        10,
        with_rhc=False,
    )
    generate_bco_results(
        asp,
        BeeColonyOptimiser,
        bco_args_copy,
        "number_of_bees",
        10,
        501,
        10,
        with_rhc=True,
    )

    bco_args_copy = deepcopy(bco_args)
    # Graphs for BCO while changing max_iter
    generate_bco_results(
        asp, BeeColonyOptimiser, bco_args_copy, "max_iter", 10, 101, 5, with_rhc=True
    )

    bco_args_copy = deepcopy(bco_args)
    # Graphs for BCO while changing trial_limit
    generate_bco_results(
        asp, BeeColonyOptimiser, bco_args_copy, "trial_limit", 1, 26, 1, with_rhc=True
    )

    bco_args_copy = deepcopy(bco_args)
    # Graphs for BCO while changing max_scouts
    generate_bco_results(
        asp, BeeColonyOptimiser, bco_args_copy, "max_scouts", 1, 11, 1, with_rhc=True
    )


def main():
    make_input_from_csv("./dataset/ikli_datasets/data_19_23.csv", num_runways=3)
    ac_input = read_input()
    asp = ACS(*ac_input)
    print(asp)

    compare_optimizers(
        [
            "./dataset/ikli_codes/alp_7_30.csv",
            "./dataset/ikli_codes/alp_7_40.csv",
            "./dataset/ikli_codes/alp_7_50.csv",
            "./dataset/ikli_datasets/data_7_11.csv",
            "./dataset/ikli_datasets/data_11_15.csv",
            "./dataset/ikli_datasets/data_15_19.csv",
            "./dataset/ikli_datasets/data_19_23.csv",
        ],
        with_rhc=True,
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
