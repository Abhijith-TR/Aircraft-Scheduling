from typing import Any, Dict, Tuple, Type
from copy import deepcopy
from optimisation.optimiser import Optimiser
from problem.acs import ACS

from problem.acs_solution import ACSolution
from problem.airplane import Airplane


class RHCSolver(Optimiser[ACSolution]):
    """
    Class to represent the RHCSolver
    Solves the aircraft scheduling problem using REceding Horizon control.

    Attributes:
        problem: The problem to be solved
        max_iter_per_horizon: The maximum number of iterations per horizon
        time_window: The time window for the horizon
        num_windows: The number of windows in the horizon
        trial_limit: The trial limit for the bee colony optimiser
        max_scouts: The maximum number of scouts for the bee colony optimiser
    """

    def __init__(
        self,
        problem: ACS,
        time_window: int,
        num_windows: int,
        optimiser_class: Type[Optimiser[ACSolution]],
        optimiser_params: Dict[str, Any],
    ):
        # Creating a copy of the problem for reference as we may need to change the ac eta_etd
        super().__init__(problem)
        self.problem = deepcopy(problem)
        self.original_problem = problem
        self.time_window = time_window
        self.num_windows = num_windows
        self.optimiser_class = optimiser_class
        self.optimiser_params = optimiser_params
        self.scheduled = set()

        # beginning and end of the time horizon
        self.time_start = min([min(ac.eta_etd) for ac in self.problem.all_ac])
        self.time_end = max([min(ac.eta_etd) for ac in self.problem.all_ac])

    def trim_problem(self, start_time: int, end_time: int) -> ACS:
        """
        Selects the aircrafts that are to be scheduled in the current horizon

        :param start_time: The start time of the horizon
        :param end_time: The end time of the horizon
        :return: The trimmed problem
        """
        # selecting acs to be scheduled
        landing_ac = [
            ac
            for ac in self.problem.landing_ac
            if min(ac.eta_etd) >= start_time
            and min(ac.eta_etd) < end_time
            and ac not in self.scheduled
        ]

        new_acs = ACS(
            self.problem.no_of_runways,
            self.problem.no_ac_types,
            self.problem.separation_matrix,
            landing_ac,
            [],
        )

        return new_acs

    def construct_solution(
        self, solution_map: Dict[Airplane, Tuple[int, int]]
    ) -> ACSolution:
        """
        Constructs an ACS Solution from the solution map

        :param solution_map: The solution map
        :return: The ACS Solution
        """
        solution = self.problem.generate_empty_solution()
        solution.value = []

        for _, (_, runway) in solution_map.items():
            solution.value.append(runway)

        # Calculating the fitness of the solution based on original problem
        solution.fitness = self.original_problem.evaluate(solution.value)
        # Setting the correct aircraft sequence
        solution.aircraft_sequence = self.original_problem.all_ac
        return solution

    def optimise(self):
        # initialise the solution map key: airplane, value the time and runway assigned to it
        scheduled_acs: Dict[Airplane, Tuple[int, int]] = dict()
        run = 0
        for t in range(
            self.time_start,
            self.time_end + (self.num_windows * self.time_window) + 1,
            self.time_window,
        ):
            run += 1
            # Initialising horizon bounds
            horizon_start = t
            horizon_end = t + self.num_windows * self.time_window

            # initialise the trimmed problem: Consider only aircraft contained in the horizon
            trimmed_acs = self.trim_problem(horizon_start, horizon_end)
            if len(trimmed_acs.all_ac) == 0:
                break

            # initialise the bee colony optimiser
            optimiser = self.optimiser_class(trimmed_acs, **self.optimiser_params)

            # Finding a solution for the trimmed problem
            solution = optimiser.optimise()

            # Finding the assigned landing times and runways for the aircrafts
            landing_times = trimmed_acs.get_landing_times(solution.value)
            schedule_window_end = horizon_start + self.time_window

            # Arrays to maintain the last landing time and type for each runway
            last_runway_landing_time = [0] * trimmed_acs.no_of_runways
            last_runway_landing_type = [0] * trimmed_acs.no_of_runways

            for i in range(len(solution.value)):
                time, runway = landing_times[i]

                if time > schedule_window_end:
                    # If the landing time is outside the window, we need to update
                    # the eta_etd to lie in the next window
                    for j in range(trimmed_acs.no_of_runways):
                        trimmed_acs.all_ac[i].eta_etd[j] = int(
                            max(
                                trimmed_acs.separation_matrix[
                                    last_runway_landing_type[j] - 1
                                ][trimmed_acs.all_ac[i].ac_type - 1]
                                + last_runway_landing_time[j]
                                + 1,
                                trimmed_acs.all_ac[i].eta_etd[j],
                            )
                        )
                else:
                    # If the landing time is within the window, we can schedule the aircraft
                    scheduled_acs[trimmed_acs.all_ac[i]] = landing_times[i]
                    self.scheduled.add(trimmed_acs.all_ac[i])
                    last_runway_landing_time[runway - 1] = time
                    last_runway_landing_type[runway - 1] = trimmed_acs.all_ac[i].ac_type

        # Constructing the solution from the solution map
        return self.construct_solution(scheduled_acs)
