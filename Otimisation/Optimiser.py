from abc import ABC, abstractmethod
from Otimisation.Problem import Problem


class Optimiser(ABC):
    def __init__(self, problem: Problem):
        self.problem = problem
        self.best_solution = None

    @abstractmethod
    def optimise(self):
        pass
