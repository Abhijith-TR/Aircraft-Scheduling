import math
from optimisation.problem import Problem
from optimisation.optimiser import Optimiser
from enum import Enum
from typing import Any
import random


class BeeType(Enum):
    EMPLOYED = "EMPLOYED"
    UNEMPLOYED = "UNEMPLYOYED"


class Bee:
    """
    Class to represent a bee

    Attributes:
        solution: Solution of the bee
        fitness: Fitness of the solution
        type: Type of the bee
        trials: Number of trials
        _id: Unique id of the bee
    """

    def __init__(
        self, solution: Any, fitness: float, bee_type: BeeType, _id: int = None
    ):
        """
        Constructor for Bee class

        :param solution: solution of the bee
        :param fitness: fitness of the solution
        :param bee_type: type of the bee
        :param _id: unique id of the bee
        """
        self.solution = solution
        self.fitness = fitness
        self.type = bee_type
        self.trials = 0
        self._id = _id

    def update_solution(self, solution, fitness: float = None) -> None:
        """
        Function to update the solution of the bee

        :param solution: new solution
        :param fitness: fitness of the new solution
        :return: None
        """
        self.solution = solution
        self.fitness = fitness

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.solution}:{self.type}:{self.fitness}:{self.trials}>"

    def __hash__(self):
        return hash(self._id)


class BeeColonyOptimiser(Optimiser):
    """
    Class to represent the Bee Colony Optimiser
    ---
    Attributes:
        problem: Problem to optimise
        number_of_bees: Number of bees
        max_iter: Maximum number of iterations
        max_scouts: Maximum number of scouts
        trial_limits: Trial limit
        max_scouts: Maximum number of scouts
    """

    def __init__(
        self,
        problem: Problem,
        number_of_bees: int,
        max_iter: int,
        trial_limit: int,
        max_scouts: int = 1,
    ):
        """
        Constructor for Bee Colony Optimiser

        :param problem: Problem to optimise
        :param number_of_bees: Number of bees
        :param max_iter: maximum number of iterations (stopping condition)
        :param trial_limit: maximum number of trials before abandoning food source
        :param max_scouts: maximum number of scouts
        """
        super().__init__(problem)
        self.number_of_bees = number_of_bees
        self.max_iter = max_iter
        self.max_scouts = max_scouts
        self.trail_limits = trial_limit
        self.best_solution = Bee(None, math.inf, BeeType.EMPLOYED)
        self.bees = []

        for i in range(self.number_of_bees):
            solution = self.problem.generate_solution()
            if i < self.number_of_bees / 2:
                self.bees.append(
                    Bee(solution, self.problem.evaluate(solution), BeeType.EMPLOYED, i)
                )
            else:
                self.bees.append(Bee(None, math.inf, BeeType.UNEMPLOYED, i))

    def employed_exploit(self) -> None:
        """
        Function to exploit the employed bees

        :return: None
        """
        employed_bees = [bee for bee in self.bees if bee.type == BeeType.EMPLOYED]
        for bee in employed_bees:
            other_bees = [
                other_bee
                for other_bee in self.bees
                if other_bee != bee and other_bee.solution != None
            ]
            next_solution = self.problem.next(
                bee.solution, random.choice(other_bees).solution
            )

            fitness_next = self.problem.evaluate(next_solution)

            if fitness_next < bee.fitness:
                bee.update_solution(next_solution, fitness_next)
                bee.trials = 0
            else:
                bee.trials += 1

    def onlooker_exploit(self, probabilities: list[(Bee, float)]) -> None:
        """
        Function to simulate onlooker bees selecting the food sources based on
        probability

        :param probabilities: List of probabilities of each bee(solution)
        :return: None
        """
        onlookers: list[Bee] = [
            bee for bee in self.bees if bee.type == BeeType.UNEMPLOYED
        ]
        probabilities.sort(key=lambda x: x[1], reverse=True)

        index = 0
        probability_index = 0

        while index < len(onlookers):
            bee, probability = probabilities[probability_index]

            if random.random() <= probability:
                onlookers[index].update_solution(
                    bee.solution, self.problem.evaluate(bee.solution)
                )
                bee.type = BeeType.UNEMPLOYED

                onlookers[index].type = BeeType.EMPLOYED
                onlookers[index].trials = bee.trials
                index += 1

            probability_index = (probability_index + 1) % len(probabilities)

    def explore(self) -> None:
        """
        Function to simulate bees exploring food sources as scouts once they have
        exhausted their trials

        :return: None
        """
        scout_candidates = [bee for bee in self.bees if bee.type == BeeType.EMPLOYED]
        scout_candidates.sort(key=lambda x: x.trials, reverse=True)
        scouts_produced = 0

        for scout_candidate in scout_candidates:
            if scouts_produced >= self.max_scouts:
                break
            if scout_candidate.trials > self.trail_limits:
                new_solution = self.problem.generate_solution()
                new_fitness = self.problem.evaluate(new_solution)
                scout_candidate.update_solution(new_solution, new_fitness)
                scout_candidate.trials = 0
                scouts_produced += 1

    def get_probablility_array(self) -> list[(Bee, float)]:
        return [
            (bee, 1 / (1 + self.problem.evaluate(bee.solution)))
            for bee in self.bees
            if bee.type == BeeType.EMPLOYED
        ]

    def optimise(self):
        """
        Function to optimise the problem

        :return: Solution to the problem in the form of a problem solution
        """
        self.optimise_iter(self.max_iter)
        return self.best_solution

    def optimise_iter(self, num_iter: int):
        """
        Run the optimiser for a given number of iterations

        :param num_iter: Number of iterations
        """
        for _ in range(num_iter):
            self.employed_exploit()
            probabilities = self.get_probablility_array()
            self.onlooker_exploit(probabilities)
            self.explore()
            assert self.bees.count(None) == 0, f"None in bees: {self.bees}"
            current_best = min(self.bees, key=lambda x: x.fitness)
            self.best_solution = min(
                current_best,
                self.best_solution,
                key=lambda x: x.fitness,
            )
