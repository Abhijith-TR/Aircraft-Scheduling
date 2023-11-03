import unittest
from problem.acs import ACS, Airplane
from problem.acs_solution import ACSolution


class PlaneTest(unittest.TestCase):
    def test_plane_init(self):
        plane = Airplane("P892", 2, 120, 0, 400, [1, 2], 10, 10)
        assert plane.ac_type == 2
        assert plane.eta_etd == [1, 2]
        assert plane.delay_cost == 10
        assert plane.pre_cost == 10


class ACSTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Is this is the best possible ordering?
        [
           Airplane('A345', 0, 0, 0, 100, [1,2], 5, 5),
           Airplane('A678', 1, 120, 0, 200, [1,2], 5, 5),
           Airplane('A123', 2, 120 , 0, 400, [1,2], 10, 10),
        ]
        """
        self.planes = [
            Airplane("A123", 3, 120, 0, 400, [1, 1], 10, 10),
            Airplane("A345", 1, 0, 0, 100, [1, 1], 10, 10),
            Airplane("A678", 2, 120, 0, 200, [1, 1], 10, 10),
        ]
        self.sep_matrix = [[5, 20, 30], [5, 10, 20], [5, 10, 20]]

        self.acs = ACS(2, 3, self.sep_matrix, self.planes, [])
        return super().setUp()

    def test_init(self):
        correct_ordering = [self.planes[1], self.planes[2], self.planes[0]]
        self.assertEqual(self.acs.no_of_runways, 2)
        self.assertEqual(self.acs.no_ac_types, 3)
        self.assertEqual(self.acs.separation_matrix, self.sep_matrix)
        self.assertEqual(self.acs.landing_ac, self.planes)
        self.assertEqual(self.acs.takeoff_ac, [])
        self.assertEqual(self.acs.all_ac, correct_ordering)

    def test_evaluate(self):
        solution = [1, 2, 1]
        score = self.acs.evaluate(solution)
        self.assertEqual(score, 310)

        solution = [1, 1, 1]
        score = self.acs.evaluate(solution)
        self.assertEqual(score, 630)

    def test_generate_solution(self):
        solution = self.acs.generate_solution()
        self.assertEqual(len(solution.value), 3)

    def test_next(self):
        seq1 = [1, 2, 1, 2, 1, 1, 1]
        seq2 = [1, 1, 1, 1, 1, 2, 1]
        ac_seq = [self.planes[i % 3] for i in range(len(seq1))]

        new_acs = ACS(2, 3, self.sep_matrix, ac_seq, [])
        solution = ACSolution(seq1, new_acs.evaluate(seq1), ac_seq)
        companion = ACSolution(seq2, new_acs.evaluate(seq2), ac_seq)

        new_solution = new_acs.next(solution, companion)
        self.assertIsInstance(new_solution, solution.__class__)
        self.assertIsInstance(new_solution.value, solution.value.__class__)
