import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock
from optimisation.bee_colony_optimiser import BeeColonyOptimiser, BeeType, Bee, Problem
from optimisation.problem import Solution


class BeeTest(unittest.TestCase):
    def test_bee_init(self):
        """Test Bee initialisation"""
        test_solution = [1, 0, 1, 0, 1]

        solution = Solution(test_solution, float("inf"))
        bee = Bee(solution, BeeType.EMPLOYED, 1)
        self.assertEqual(bee.solution.value, test_solution)
        self.assertEqual(bee.solution.fitness, float("inf"))
        self.assertEqual(bee.type, BeeType.EMPLOYED)
        self.assertEqual(bee.trials, 0)

    def test_bee_update_solution(self):
        """Test Bee solution update"""
        test_solution = [1, 0, 1, 0, 1]
        solution = Solution(test_solution, 1)
        bee = Bee(solution, BeeType.EMPLOYED, 1)

        new_solution = [1, 1, 1, 0, 1]
        solution = Solution(new_solution, 0.5)
        bee.update_solution(solution)
        self.assertEqual(bee.solution.value, new_solution)
        self.assertEqual(bee.solution.fitness, 0.5)


class OptimiserTest(unittest.TestCase):
    def test_optimiser_init(self):
        mock_problem = Mock(Problem)
        fitness = [i / 10 for i in range(1000)].__iter__()

        mock_problem.generate_solution = MagicMock(
            return_value=Solution([1, 0, 1, 1, 1], float("inf"))
        )
        mock_problem.next.side_effect = lambda x, y: Solution(
            [1, 1, 1, 0, 1], next(fitness)
        )
        mock_problem.generate_empty_solution = MagicMock(
            return_value=Solution(None, float("inf"))
        )

        bco = BeeColonyOptimiser(
            problem=mock_problem, number_of_bees=10, max_iter=100, trial_limit=10
        )

        self.assertEqual(bco.problem, mock_problem)
        num_employed = len(bco.employed_bees)
        num_onlookers = len(bco.unemployed_bees)

        self.assertEqual(num_employed, 5)
        self.assertEqual(num_onlookers, 5)

        bco.optimise_iter(1)

        bee_fitness = [
            bee.solution.fitness for bee in bco.unemployed_bees
        ]

        self.assertEqual(num_employed, 5)
        self.assertEqual(num_onlookers, 5)
        self.assertEqual(mock_problem.next.call_count, 5)
        self.assertCountEqual(
            bee_fitness,
            [0.0, 0.1, 0.2, 0.3, 0.4],
        )
        self.assertEqual(bco.best_solution.solution.fitness, 0.0)
