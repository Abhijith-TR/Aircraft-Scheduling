from typing import List, Optional
from optimisation.problem import Solution
from problem.airplane import Airplane


class ACSolution(Solution):
    """
    Sub class of a solution to represent the solution of the ACS problem

    Attributes
    ----------
    value : Optional[List[int]]
        The value of the solution
    fitness : float
        The fitness of the solution
    aircraft_sequence : list[Airplane]
        The sequence of aircrafts
    """
    def __init__(
        self, value: Optional[List[int]], fitness: float, aircraft_sequence: list[Airplane]
    ):
        super().__init__(value, fitness)
        self.aircraft_sequence = aircraft_sequence
