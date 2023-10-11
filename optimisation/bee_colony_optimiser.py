from optimisation.problem import Problem
from optimisation.optimiser import Optimiser
from enum import Enum
from typing import Any
import random


class BeeType(Enum):
    EMPLOYED = "EMPLOYED"
    EXPLORER = "EXPLORER"


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
        return f"<{self.__class__.__name__} {self.solution}:{self.type}:{self.trials}>"

    def __hash__(self):
        return hash(self._id)


class BeeColonyOptimiser(Optimiser):
    """
    Class to represent the Bee Colony Optimiser
    ---
    Attributes:
        number_of_bees: Number of bees
        max_iter: Maximum number of iterations
        max_scouts: Maximum number of scouts
        trail_limits: Trail limit
        bees: List of bees
    """

    def __int__(
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
        self.bees = []

        for _ in range(self.number_of_bees):
            solution = self.problem.generate_solution()
            if _ < self.number_of_bees / 2:
                self.bees.append(
                    Bee(solution, self.problem.evaluate(solution), BeeType.EMPLOYED)
                )
            else:
                self.bees.append(
                    Bee(solution, self.problem.evaluate(solution), BeeType.EXPLORER)
                )

    def employed_exploit(self) -> None:
        """
        Function to exploit the employed bees

        :return: None
        """
        for bee in self.bees:
            next_solution = self.problem.next(bee.solution)
            if self.problem.evaluate(next_solution) < self.problem.evaluate(
                bee.solution
            ):
                bee.update_solution(next_solution, self.problem.evaluate(next_solution))
                bee.trials = 0
            else:
                bee.trials += 1

    def onlooker_exploit(self, probabilities: list[(Bee, float)]) -> None:
        """
        Function to simulate onlooker bees selecting the food sources based on probability

        :param probabilities: List of probabilities of each bee(solution)
        :return: None
        """
        onlookers = [bee for bee in self.bees if bee.type == BeeType.EXPLORER]
        probabilities.sort(key=lambda x: x[1], reverse=True)

        index = 0
        probability_index = 0

        while index < len(onlookers):
            bee, probability = probabilities[probability_index]

            if random.random() >= probability:
                onlookers[index].update_solution(bee.solution)
                bee.type = BeeType.EXPLORER
                onlookers[index].type = BeeType.EMPLOYED
                onlookers[index].trials = bee.trials
                index += 1

            probability_index = (probability_index + 1) % len(probabilities)

    def explore(self) -> None:
        """
        Function to simulate bees exploring food sources as scouts once they have exhausted their trials

        :return: None
        """
        scout_candidates = [bee for bee in self.bees if bee.type == BeeType.EMPLOYED]
        scout_candidates.sort(key=lambda x: x.trials, reverse=True)
        scouts_produced = 0

        for scout_candidate in scout_candidates:
            if scouts_produced >= self.max_scouts:
                break
            if scout_candidate.trials > self.trail_limits:
                scout_candidate.update_solution(self.problem.generate_solution())
                scout_candidate.trials = 0
                scouts_produced += 1

    def optimise(self):
        """
        Function to optimise the problem

        :return: Solution to the problem in the form of a problem solution
        """
        for _ in range(self.max_iter):
            self.employed_exploit()
            probabilities = [
                (bee, self.problem.evaluate(bee.solution)) for bee in self.bees
            ]
            self.onlooker_exploit(probabilities)
            self.explore()
            self.best_solution = min(
                min(self.bees, key=lambda x: x.fitness).solution,
                self.best_solution,
                key=lambda x: x.fitness,
            )

        return self.best_solution
