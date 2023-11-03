from typing import Any, List, Optional
from optimisation.problem import Solution
from problem.airplane import Airplane


class ACSolution(Solution):
    def __init__(
        self, value: Optional[List[int]], fitness: float, aircraft_sequence: list[Airplane]
    ):
        super().__init__(value, fitness)
        self.aircraft_sequence = aircraft_sequence
