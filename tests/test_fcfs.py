import unittest

from optimisation.fcfs import FCFS
from problem.acs import ACS
from problem.airplane import Airplane


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setting up the test case
        [
           Airplane('A345', 0, 0, 0, 100, [1,2], 5, 5),
           Airplane('A678', 1, 120, 0, 200, [1,2], 5, 5),
           Airplane('A123', 2, 120 , 0, 400, [1,2], 10, 10),
        ]
        """
        self.planes = [
            Airplane('A123', 3, 120, 0, 400, [1, 1], 10, 10),
            Airplane('A345', 1, 0, 0, 100, [1, 1], 10, 10),
            Airplane('A678', 2, 120, 0, 200, [1, 1], 10, 10),
        ]
        self.sep_matrix = [[5, 20, 30], [5, 10, 20], [5, 10, 20]]
        self.acs = ACS(2, 3, self.sep_matrix, self.planes, [])
        return super().setUp()

    def test_fcfs(self):
        """
        Testing the FCFS solver on the given problem
        """
        fcfs_solver = FCFS(self.acs)
        solution = fcfs_solver.optimise()
        # self.assertEqual(solution.value, [1, 2, 2])
        self.assertEqual(self.acs.evaluate(solution.value), 210)

if __name__ == '__main__':
    unittest.main()
