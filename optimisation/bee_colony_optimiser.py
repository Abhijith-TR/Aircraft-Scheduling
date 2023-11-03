import math
import pprint
from optimisation.problem import Problem, Solution
from optimisation.optimiser import Optimiser
from enum import Enum
from typing import Any, Generic, List, Tuple, TypeVar
import random

T = TypeVar("T", bound="Solution")

class BeeType(Enum):
    EMPLOYED = "EMPLOYED"
    UNEMPLOYED = "UNEMPLYOYED"


class Bee(Generic[T]):
    """
    Class to represent a bee

    Attributes
    ----------
    solution : T
        The solution of the bee
    fitness : float
        The fitness of the solution
    type : BeeType
        The type of the bee
    trials : int
        The number of trials the bee has undergone
    _id : int
        The unique id of the bee
    """

    def __init__(self, solution: T, bee_type: BeeType, _id: int = -1):
        """
        Constructor for Bee class

        :param solution: solution of the bee
        :param fitness: fitness of the solution
        :param bee_type: type of the bee
        :param _id: unique id of the bee
        """
        self.solution = solution
        self.type = bee_type
        self.trials = 0
        self._id = _id

    def update_solution(self, solution: T) -> None:
        """
        Function to update the solution of the bee

        :param solution: new solution
        :param fitness: fitness of the new solution
        :return: None
        """
        self.solution = solution

    def get_solution(self) -> T:
        """
        Function to convert the bee to a solution

        :return: Solution of the bee
        """
        return self.solution

    def __repr__(self):
        return f"""<{self.__class__.__name__}\n\t{self.type}:{self.trials} \n\tSolution: {self.solution}\n>"""

    def __hash__(self):
        return hash(self._id)


class BeeColonyOptimiser(Optimiser[T]):
    """
    Class to represent the Bee Colony Optimiser

    Attributes
    ----------
    problem : Problem[T]
        The problem to be optimised
    number_of_bees : int
        The number of bees
    max_iter : int
        The maximum number of iterations
    max_scouts : int
        The maximum number of scouts
    trail_limits : int
        The maximum number of trials
    best_solution : Bee[T]
        The best solution found
    bees : List[Bee[T]]
        The list of bees
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
        self.best_solution = Bee(self.problem.generate_empty_solution(), BeeType.EMPLOYED)
        self.bees: List[Bee] = []

        for i in range(self.number_of_bees):
            if i < self.number_of_bees / 2:
                sol = problem.generate_solution()
                assert isinstance(sol, Solution)
                self.bees.append(Bee(problem.generate_solution(), BeeType.EMPLOYED, i))
            else:
                self.bees.append(
                    Bee(Solution(None, float("inf")), BeeType.UNEMPLOYED, i)
                )

    def employed_exploit(self) -> None:
        """
        Function to run the employed bees exploit phase

        :return: None
        """
        employed_bees = [bee for bee in self.bees if bee.type == BeeType.EMPLOYED]
        for bee in employed_bees:
            other_bees = [
                other_bee
                for other_bee in self.bees
                if other_bee != bee and other_bee.solution.value != None
            ]

            next_solution = self.problem.next(
                bee.solution, random.choice(other_bees).solution
            )

            fitness_next = next_solution.fitness

            if fitness_next < bee.solution.fitness:
                bee.update_solution(next_solution)
                bee.trials = 0
            else:
                bee.trials += 1

    def onlooker_exploit(self, probabilities: List[Tuple[Bee, float]]) -> None:
        """
        Function to simulate onlooker bees selecting the food sources based on
        probability

        :param probabilities: List of probabilities of each bee(solution)
        :return: None
        """
        onlookers = [bee for bee in self.bees if bee.type == BeeType.UNEMPLOYED]
        for bee, _ in probabilities:
            bee.type = BeeType.UNEMPLOYED

        probabilities.sort(key=lambda x: x[1], reverse=True)

        index = 0
        probability_index = 0

        while index < len(onlookers):
            bee, probability = probabilities[probability_index]

            if random.random() <= probability:
                onlookers[index].update_solution(bee.solution)
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
                other_bees = [
                    other_bee
                    for other_bee in self.bees
                    if other_bee != scout_candidate and other_bee.solution.value != None
                ]
                next_solution = self.problem.next(
                    scout_candidate.solution, random.choice(other_bees).solution
                )
                scout_candidate.update_solution(next_solution)
                scout_candidate.trials = 0
                scouts_produced += 1

    def get_probablility_array(self) -> List[Tuple[Bee, float]]:
        """
        Function to get the probability array of the bees. Higher the fitness, higher
        the probability

        :return: List of probabilities of each bee(solution)
        """
        return [
            (bee, 1 / (1 + bee.solution.fitness))
            for bee in self.bees
            if bee.type == BeeType.EMPLOYED
        ]

    def optimise(self) -> T:
        """
        Function to optimise the problem

        :return: Solution to the problem in the form of a problem solution
        """
        self.optimise_iter(self.max_iter)
        return self.best_solution.get_solution()

    def optimise_iter(self, num_iter: int):
        """
        Run the optimiser for a given number of iterations. Runs the employed exploit,
        onlooker exploit and explore phases for each iteration

        :param num_iter: Number of iterations
        """
        for _ in range(num_iter):
            self.employed_exploit()
            probabilities = self.get_probablility_array()
            self.onlooker_exploit(probabilities)
            self.explore()
            current_best = min(self.bees, key=lambda x: x.solution.fitness)
            self.best_solution = min(
                current_best,
                self.best_solution,
                key=lambda x: x.solution.fitness,
            )
