from abc import ABC, abstractmethod
from typing import Any


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
