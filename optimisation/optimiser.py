from abc import ABC, abstractmethod
from optimisation.problem import Problem, Solution
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound="Solution")

class Optimiser(ABC, Generic[T]):
    def __init__(self, problem: Problem[T]):
        self.problem = problem
        self.best_solution = None

    @abstractmethod
    def optimise(self) -> T:
        pass
