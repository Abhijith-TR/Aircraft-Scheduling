from turtle import pos
from typing import List, Tuple, TypeVar
from optimisation.optimiser import Optimiser
from optimisation.problem import Problem
from problem.acs_solution import ACSolution
import random


T = TypeVar("T", bound="ACSolution")


class GeneticOptimiser(Optimiser[T]):
    def __init__(self, problem: Problem[T], population_size: int, generations: int):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations

    def generate_population(self) -> List[T]:
        population = []
        for _ in range(self.population_size):
            solution = self.problem.generate_solution()
            population.append(solution)
        return population

    def select(self, population: List[T]) -> T:
        return random.choices(population, [1 / (1+x.fitness) for x in population])[0]

    def crossover(self, parent1: T, parent2: T) -> Tuple[T, T]:
        child1 = self.problem.generate_solution()
        child2 = self.problem.generate_solution()

        index = random.randint(0, len(child1.value))
        child1.value = parent1.value[:index] + parent2.value[index:]
        child2.value = parent2.value[:index] + parent1.value[index:]

        child1.fitness = self.problem.evaluate_solution(child1)
        child2.fitness = self.problem.evaluate_solution(child2)

        return (child1, child2)

    def mutate(self, solution: T) -> T:
        pos1, pos2 = random.sample(range(len(solution.value)), 2)
        solution.value[pos1], solution.value[pos2] = (
            solution.value[pos2],
            solution.value[pos1],
        )
        solution.fitness = self.problem.evaluate_solution(solution)
        return solution

    def generate_new_population(self, population: List[T]) -> List[T]:
        new_population = []
        for _ in range(self.population_size//2):
            parent1 = self.select(population)
            parent2 = self.select(population)
            (child1, child2) = self.crossover(parent1, parent2)
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            new_population.extend((child1, child2))
        return new_population

    def optimise(self) -> T:
        population = self.generate_population()
        best_solution = self.problem.generate_empty_solution()
        for i in range(self.generations):
            population = self.generate_new_population(population)
            best_solution = min(population, key=lambda x: x.fitness)

        return best_solution
