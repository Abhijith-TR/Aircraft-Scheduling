from optimisation.problem import Problem
from problem.airplane import Airplane

import random


class ACS(Problem):
    """
    Class for the Airplane Scheduling Problem that extends the Problem class.

    Attributes
    ----------
    no_of_runways : int
        The number of runways available at the airport.
    no_ac_types : int
        The number of different types of airplanes.
    separation_matrix : list[list[float]]
        The separation matrix between the different types of airplanes.
    landing_ac : list[Airplane]
        The list of airplanes that are landing.
    takeoff_ac : list[Airplane]
        The list of airplanes that are taking off.
    all_ac : list[Airplane]
        The list of all airplanes.
    """

    def __init__(
        self,
        no_of_runways: int,
        no_of_ac_types: int,
        separation_matrix: list[list[float]],
        landing_ac: list[Airplane],
        takeoff_ac: list[Airplane],
    ):
        """
        Constructor for the ACS class.

        :param no_of_runways: The number of runways available at the airport.
        :param no_ac_types: The number of different types of airplanes.
        :param separation_matrix: The separation matrix between the different types of airplanes.
        :param landing_ac: The list of airplanes that are landing.
        :param takeoff_ac: The list of airplanes that are taking off.
        """
        super().__init__()
        self.no_of_runways = no_of_runways
        self.no_ac_types = no_of_ac_types
        self.separation_matrix = separation_matrix
        self.landing_ac = landing_ac
        self.takeoff_ac = takeoff_ac
        self.all_ac = self.landing_ac + self.takeoff_ac
        self.all_ac.sort(key=lambda x: x.ending_time)
        for ac in self.all_ac:
            assert len(ac.eta_etd) == self.no_of_runways

    def evaluate(self, solution: list[int]) -> int:
        """
        Function that evaluates the solution. The cost of the solution is the sum of
        the delay costs of all landing airplanes.

        :param solution: The solution to be evaluated.
        :return: The cost of the solution.
        """
        cost = 0
        current_runway_times = [0] * self.no_of_runways
        ac_type_on_runway = [0] * self.no_of_runways

        for i in range(len(solution)):
            if ac_type_on_runway[solution[i] - 1] == 0:
                ac_type_on_runway[solution[i] - 1] = self.all_ac[i].ac_type
                current_runway_times[solution[i] - 1] += (self.all_ac[i].eta_etd)[solution[i] - 1]
                continue

            current_ac_type = self.all_ac[i].ac_type
            previous_ac_type = ac_type_on_runway[solution[i] - 1]
            runway_delay = current_runway_times[solution[i] - 1]
            min_runway_landing_time = (
                runway_delay
                + self.separation_matrix[previous_ac_type - 1][current_ac_type - 1]
            )
            landing_time = max((self.all_ac[i].eta_etd)[solution[i] - 1], min_runway_landing_time)
            cost += (landing_time - (self.all_ac[i].eta_etd)[solution[i] - 1]) * self.all_ac[i].delay_cost
            current_runway_times[solution[i] - 1] = landing_time
        if cost == None: print("None dsu:",solution)
        return cost

    def next(self, solution, companion):
        """
        Uses the next neighbour function to generate a new solution. The next neighbour
        function is to swap the runways of two airplanes.

        :param solution: The solution to be changed.
        :param companion: The companion solution used to generate the new solution.
        :return: A new solution.
        """
        new_solution = solution.copy()
        index = random.randint(0, len(new_solution) - 1)
        phi = 2 * random.random() - 1
        new_solution[index] = int(
            round(solution[index] + phi * (solution[index] - companion[index]))
        )
        new_solution[index] = max(1, new_solution[index])
        new_solution[index] = min(self.no_of_runways, new_solution[index])
        return new_solution

    def generate_solution(self):
        """
        Generates a random solution to the problem. The solution is a list of integers,
        where the index of the list represents the airplane and the value at that
        index represents the runway. The order of the airplanes in the list is the
        order in which they are scheduled on a specific runway.
        """
        # solution = [
        #     (airplane, random.randint(1, self.no_of_runways))
        #     for airplane in self.all_ac
        # ]
        solution = [
            random.randint(1, self.no_of_runways)
            for airplane in self.all_ac
        ]
        return solution

    def __repr__(self) -> str:
        return f"ACS < {self.no_of_runways} : {self.no_ac_types} : {self.separation_matrix}: {len(self.all_ac)} Airplanes>"