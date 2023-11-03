from functools import partial
from optimisation.bee_colony_optimiser import BeeColonyOptimiser
from optimisation.optimiser import Optimiser
from problem.acs import ACS
from copy import deepcopy

from problem.acs_solution import ACSolution


class RHCSolver(Optimiser):
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
        max_iter_per_horizon: int,
        time_window: int,
        num_windows: int,
        trial_limit: int,
        max_scouts: int,
    ):
        # Creating a copy of the problem for reference as we may need to change the ac eta_etd
        self.problem = deepcopy(problem)
        self.original_problem = problem
        self.max_iter_per_horizon = max_iter_per_horizon
        self.time_window = time_window
        self.num_windows = num_windows
        self.trial_limit = trial_limit
        self.max_scouts = max_scouts

        # beginning and end of the time horizon
        self.time_start = min([min(ac.eta_etd) for ac in self.problem.all_ac])
        self.time_end = max([min(ac.eta_etd) for ac in self.problem.all_ac])

    def trim_problem(self, start_time: int, end_time: int) -> ACS:
        # selecting acs to be scheduled
        landing_ac = [
            ac
            for ac in self.problem.landing_ac
            if max(ac.eta_etd) <= end_time and max(ac.eta_etd) >= start_time
        ]

        new_acs = ACS(
            self.problem.no_of_runways,
            self.problem.no_ac_types,
            self.problem.separation_matrix,
            landing_ac,
            [],
        )

        return new_acs

    def optimise(self):
        partial_solution = ACSolution([], float('inf'), self.problem.all_ac)

        for t in range(
            self.time_start, self.time_end, self.num_windows * self.time_window
        ):
            start_time = t
            end_time = t + self.num_windows * self.time_window

            # initialise the trimmed problem
            trimmed_acs = self.trim_problem(start_time, end_time)

            bco = BeeColonyOptimiser[ACSolution](
                trimmed_acs,
                self.max_iter_per_horizon,
                self.trial_limit,
                self.max_scouts,
            )

            solution = bco.optimise()

            landing_times = trimmed_acs.get_landing_times(solution.value)
            schedule_window_end = start_time + self.time_window

            for i in range(len(solution.value)):
                time, runway = landing_times[i]
                if time > schedule_window_end:
                    for j in range(trimmed_acs.no_of_runways):
                        self.problem.all_ac[i].eta_etd[j] = max(
                            self.problem.all_ac[i].eta_etd[j], schedule_window_end
                        )
