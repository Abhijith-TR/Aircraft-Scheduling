from abc import ABC, abstractmethod
from typing import Any


class Solution:
    def __init__(self, solution: Any, fitness: float):
        self.solution = solution
        self.fitness = fitness

    def __str__(self):
        return str(self.solution)
    
    def __repr__(self) -> str:
        return f"Solution<{self.solution} : {self.fitness}>"

class Problem(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, solution):
        pass

    @abstractmethod
    def next(self, solution, companion):
        pass

    @abstractmethod
    def generate_solution(self) -> Any:
        """
        Generates a random solution to begin with.

        :return: A solution to the problem
        """
        pass
