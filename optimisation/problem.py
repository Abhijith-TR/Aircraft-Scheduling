from abc import ABC, abstractmethod


class Problem(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, solution):
        pass

    @abstractmethod
    def next(self, solution):
        pass

    @abstractmethod
    def generate_solution(self) -> Any:
        """
        Generates a random solution to begin with.

        :return:
        """
        pass
