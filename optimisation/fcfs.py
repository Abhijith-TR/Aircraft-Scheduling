from optimisation.optimiser import Optimiser
from problem.acs import ACS
from optimisation.problem import Solution
from problem.acs_solution import ACSolution


class FCFS(Optimiser[ACSolution]):
    """
    Class to implement First Come First Serve algorithm. The algorithm assigns
    the first available runway to the airplane that arrives first. If the runway
    is not available, the airplane is delayed until the runway is available.

    Attributes
    ----------
    problem : ACS
        The problem to be solved
    """

    def __init__(self, problem: ACS):
        self.problem = problem

    def optimise(self):
        runway_delay = [0 for i in range(self.problem.no_of_runways)]
        runway_type = [0 for i in range(self.problem.no_of_runways)]
        all_ac = self.problem.all_ac
        solution = []

        for ac in all_ac:
            min_runway = -1
            min_delay = float("inf")
            for i in range(self.problem.no_of_runways):
                if runway_type[i] == 0:
                    landing_time = ac.eta_etd[i]
                    if landing_time < min_delay:
                        min_delay = landing_time
                        min_runway = i + 1
                    continue

                current_ac_type = ac.ac_type
                previous_ac_type = runway_type[i]
                delay = runway_delay[i]
                min_runway_landing_time = (
                    delay
                    + self.problem.separation_matrix[previous_ac_type - 1][
                        current_ac_type - 1
                    ]
                )

                landing_time = max(min_runway_landing_time + 1, ac.eta_etd[i])

                if landing_time < min_delay:
                    min_delay = landing_time
                    min_runway = i + 1

            runway_type[min_runway - 1] = ac.ac_type
            runway_delay[min_runway - 1] = int(min_delay)
            solution.append(min_runway)

        fcfs_solution = Solution(solution, self.problem.evaluate(solution))
        return fcfs_solution
