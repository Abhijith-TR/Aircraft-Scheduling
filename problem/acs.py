from optimisation.problem import Problem
from problem.airplane import Airplane

import random


class ACS(Problem):
    def __init__(
        self,
        no_of_runways: int,
        no_of_ac_types: int,
        separation_matrix: list[list[float]],
        landing_ac: list[Airplane],
        takeoff_ac: list[Airplane],
    ):
        super().__init__()
        self.no_of_runways = no_of_runways
        self.no_ac_types = no_of_ac_types
        self.separation_matrix = separation_matrix

        self.landing_ac = landing_ac

        self.takeoff_ac = takeoff_ac
        self.all_ac = self.landing_ac + self.takeoff_ac
        self.all_ac.sort(key=lambda x: min(x.eta_etd))

    def evaluate(self, solution: list[tuple[Airplane, int]]):
        pass

    def next(self, solution):
        # [1 2 3 1 2 3 1 2 3]
        pass

    def generate_solution(self):
        solution = [
            (airplane, random.randint(1, self.no_of_runways))
            for airplane in self.all_ac
        ]
        return solution
