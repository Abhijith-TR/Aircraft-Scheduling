import unittest
from unittest.mock import Mock, MagicMock
from optimisation.bee_colony_optimiser import BeeColonyOptimiser, BeeType, Bee, Problem


class BeeTest(unittest.TestCase):
    def test_bee_init(self):
        """Test Bee initialisation"""
        test_solution = [1, 0, 1, 0, 1]
        bee = Bee(test_solution, None, BeeType.EMPLOYED, 1)
        self.assertEqual(bee.solution, test_solution)
        self.assertEqual(bee.fitness, None)
        self.assertEqual(bee.type, BeeType.EMPLOYED)
        self.assertEqual(bee.trials, 0)

    def test_bee_update_solution(self):
        """Test Bee solution update"""
        test_solution = [1, 0, 1, 0, 1]
        bee = Bee(test_solution, None, BeeType.EMPLOYED, 1)
        new_solution = [1, 1, 1, 0, 1]
        bee.update_solution(new_solution, 0.5)
        self.assertEqual(bee.solution, new_solution)
        self.assertEqual(bee.fitness, 0.5)


class OptimiserTest(unittest.TestCase):
    def test_optimiser_init(self):
        mock_problem = Mock(Problem)
        fitness = [i / 10 for i in range(1000)].__iter__()

        mock_problem.generate_solution = MagicMock(return_value=[1, 0, 1, 1, 1])
        mock_problem.evaluate.side_effect = lambda x: next(fitness)
        mock_problem.next = MagicMock(return_value=[1, 1, 1, 0, 1])

        bco = BeeColonyOptimiser(
            problem=mock_problem, number_of_bees=10, max_iter=100, trial_limit=10
        )

        self.assertEqual(bco.problem, mock_problem)
        num_employed = len([bee for bee in bco.bees if bee.type == BeeType.EMPLOYED])
        num_onlookers = len([bee for bee in bco.bees if bee.type == BeeType.UNEMPLOYED])

        self.assertEqual(num_employed, 5)
        self.assertEqual(num_onlookers, 5)

        bco.optimise_iter(1)

        self.assertEqual(num_employed, 5)
        self.assertEqual(num_onlookers, 5)
        self.assertEqual(mock_problem.next.call_count, 5)
        self.assertEqual(mock_problem.evaluate.call_count, 20)
        self.assertEqual(bco.best_solution.fitness, 0.0)
