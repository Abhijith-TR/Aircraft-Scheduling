from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound="Solution")


class Solution:
    def __init__(self, value: Any, fitness: float):
        self.value = value
        self.fitness = fitness

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.value} : {self.fitness}>"


class Problem(ABC, Generic[T]):
    def __init__(self):
        pass

    @abstractmethod
    def next(self, solution: T, companion: T) -> T:
        pass

    @abstractmethod
    def generate_solution(self) -> T:
        """
        Generates a random solution to begin with.

        :return: A solution to the problem
        """
        pass

    @abstractmethod
    def generate_empty_solution(self) -> T:
        """
        Generates an empty solution.

        :return: A solution to the problem
        """
        pass
