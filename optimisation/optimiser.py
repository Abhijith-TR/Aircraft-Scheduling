from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from optimisation.problem import Problem, Solution

T = TypeVar("T", bound="Solution")

class Optimiser(ABC, Generic[T]):
    """
    Optimiser class to represent an optimiser

    Attributes
    ----------
    problem : Problem[T]
        The problem to be optimised
    best_solution : T
        The best solution found
    """

    def __init__(self, problem: Problem[T]):
        """
        Optimiser class to represent an optimiser

        :param problem: The problem to be optimised
        """
        self.problem = problem
        self.best_solution = None

    @abstractmethod
    def optimise(self) -> T:
        """
        Method to optimise the problem

        :return: The best solution found
        """
