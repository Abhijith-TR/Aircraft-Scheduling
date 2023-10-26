import unittest
from unittest.mock import Mock, MagicMock
from problem.acs import ACS, Airplane


class PlaneTest(unittest.TestCase):
    def test_plane_init(self):
        plane = Airplane(2, 120, 0, 400, [1, 2], 10, 10)
        assert plane.ac_type == 2
        assert plane.eta_etd == [1, 2]
        assert plane.delay_cost == 10
        assert plane.pre_cost == 10


class ACSTest(unittest.TestCase):
    def setUp(self) -> None:
        self.planes = [
            Airplane(2, 120, 0, 400, [1, 1], 10, 10),
            Airplane(0, 0, 0, 100, [1, 1], 10, 10),
            Airplane(1, 120, 0, 200, [1, 1], 10, 10),
        ]

        """
        [
            Airplane(0, 0, 0, 100, [1,2], 5, 5),
            Airplane(1, 120, 0, 200, [1,2], 5, 5),
            Airplane(2, 120 , 0, 400, [1,2], 10, 10),
        ]
        """
        self.sep_matrix = [[5, 20, 30], 
                      [5, 10, 20], 
                      [5, 10, 20]]
        
        self.acs = ACS(2, 3, self.sep_matrix, self.planes, [])
        return super().setUp()

    def test_init(self):
        correct_ordering = [self.planes[1], self.planes[2], self.planes[0]]
        assert self.acs.no_of_runways == 2
        assert self.acs.no_ac_types == 3
        assert self.acs.separation_matrix == self.sep_matrix
        assert self.acs.landing_ac == self.planes
        assert self.acs.takeoff_ac == []
        assert self.acs.all_ac == correct_ordering

    def test_evaluate(self):
        #TODO: Please make it pass
        solution = [1, 2, 1]
        score = self.acs.evaluate(solution)
        assert score == 0, f"Score should be 0 was {score}"

        solution = [1, 1, 1]
        score = self.acs.evaluate(solution)
        assert score == 0, f"Score should be 0 was {score}"

    def test_generate_solution(self):
        solution = self.acs.generate_solution()
        assert len(solution) == 3, f"Solution should be of length 3 was {solution}"

    def test_next(self):
        solution = [1, 2, 1, 2, 1, 1, 1]
        companion = [1, 1, 1, 1, 1, 2, 1]
        new_solution = self.acs.next(solution, companion)
        assert new_solution != [
            1,
            2,
            1,
        ], f"Solution should not be unchanged was {new_solution}"
