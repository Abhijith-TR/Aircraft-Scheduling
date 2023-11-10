from copy import deepcopy
from typing import List, Tuple
from optimisation.problem import Problem
from problem.acs_solution import ACSolution
from problem.airplane import Airplane

import random


class ACS(Problem[ACSolution]):
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
        separation_matrix: List[List[int]],
        landing_ac: List[Airplane],
        takeoff_ac: List[Airplane],
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

    def get_landing_times(self, solution: List[int]) -> List[Tuple[int, int]]:
        """
        Returns the landing times of the airplanes in the solution.

        :param solution: The solution to be evaluated.
        :return: The landing times of the airplanes in the solution.
        """
        current_runway_times = [0] * self.no_of_runways
        ac_type_on_runway = [0] * self.no_of_runways
        landing_times = []

        for i in range(len(solution)):
            if ac_type_on_runway[solution[i] - 1] == 0:
                ac_type_on_runway[solution[i] - 1] = self.all_ac[i].ac_type
                current_runway_times[solution[i] - 1] += self.all_ac[i].eta_etd[
                    solution[i] - 1
                ]
                landing_times.append(
                    (current_runway_times[solution[i] - 1], solution[i])
                )
                continue

            current_ac_type = self.all_ac[i].ac_type
            previous_ac_type = ac_type_on_runway[solution[i] - 1]
            runway_delay = current_runway_times[solution[i] - 1]
            min_runway_landing_time = (
                runway_delay
                + self.separation_matrix[previous_ac_type - 1][current_ac_type - 1]
            )
            landing_time = max(
                self.all_ac[i].eta_etd[solution[i] - 1], min_runway_landing_time + 1
            )

            current_runway_times[solution[i] - 1] = landing_time
            ac_type_on_runway[solution[i] - 1] = self.all_ac[i].ac_type
            landing_times.append((landing_time, solution[i]))

        return landing_times

    def evaluate_solution(self, solution: ACSolution) -> float:
        return self.evaluate(solution.value)

    def evaluate(self, solution: List[int]) -> float:
        """
        Function that evaluates the solution. The cost of the solution is the sum of
        the delay costs of all landing airplanes.

        :param solution: The solution to be evaluated.
        :return: The cost of the solution.
        """
        landing_times = self.get_landing_times(solution)
        cost = 0
        for i in range(len(solution)):
            time, runway = landing_times[i]
            cost += max(
                0,
                (time - self.all_ac[i].eta_etd[runway - 1])
                * (self.all_ac[i].delay_cost),
            )

        return cost

    def next(self, solution: ACSolution, companion: ACSolution) -> ACSolution:
        """
        Uses the next neighbour function to generate a new solution. The next neighbour
        function is to swap the runways of two airplanes.

        :param solution: The solution to be changed.
        :param companion: The companion solution used to generate the new solution.
        :return: A new solution.
        """
        new_solution = ACSolution(
            solution.value.copy(), solution.fitness, solution.aircraft_sequence
        )
        # print(new_solution)
        index = random.randint(0, len(new_solution.value) - 1)
        phi = 2 * random.random() - 1
        new_solution.value[index] = int(
            round(
                solution.value[index]
                + phi * (solution.value[index] - companion.value[index])
            )
        )
        new_solution.value[index] = max(1, new_solution.value[index])
        new_solution.value[index] = min(self.no_of_runways, new_solution.value[index])

        new_solution.fitness = self.evaluate(new_solution.value)

        return new_solution

    def generate_solution(self) -> ACSolution:
        """
        Generates a random solution to the problem. The solution is a list of integers,
        where the index of the list represents the airplane and the value at that
        index represents the runway. The order of the airplanes in the list is the
        order in which they are scheduled on a specific runway.
        """
        solution = [random.randint(1, self.no_of_runways) for airplane in self.all_ac]
        acs_solution = ACSolution(solution, self.evaluate(solution), self.all_ac)
        return acs_solution

    def generate_empty_solution(self) -> ACSolution:
        """
        Generates an empty solution to the problem with value as None.
        """
        return ACSolution(None, float("inf"), [])

    def __repr__(self) -> str:
        return f"ACS < {self.no_of_runways} : {self.no_ac_types} : {self.separation_matrix}: {len(self.all_ac)} Airplanes>"
