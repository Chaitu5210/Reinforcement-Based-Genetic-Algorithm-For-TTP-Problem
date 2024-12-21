import random
import numpy as np
from typing import List, Tuple

class GeneticAlgorithm:
    def __init__(self, population_size: int, mutation_rate: float, generations: int):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def initialize_population(self, num_cities: int, num_items: int) -> List[Tuple[List[int], List[int]]]:
        population = []
        for _ in range(self.population_size):
            route = list(range(num_cities))
            random.shuffle(route)
            picking_plan = [random.randint(0, 1) for _ in range(num_items)]
            population.append((route, picking_plan))
        return population

    def select_parents(self, population, fitness_scores):
        """Select parents using a tournament selection."""
        parents = []
        for _ in range(self.population_size):
            # Select two random individuals
            ind1, ind2 = random.sample(range(self.population_size), 2)
            # Choose the one with the better fitness
            if fitness_scores[ind1] > fitness_scores[ind2]:
                parents.append(population[ind1])
            else:
                parents.append(population[ind2])
        return parents

    def crossover(self, parent1: Tuple[List[int], List[int]], 
                 parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2
        
        # Order Crossover for route
        point1, point2 = sorted(random.sample(range(len(route1)), 2))
        child_route = [-1] * len(route1)
        child_route[point1:point2] = route1[point1:point2]
        
        remaining = [x for x in route2 if x not in child_route[point1:point2]]
        child_route[:point1] = remaining[:point1]
        child_route[point2:] = remaining[point1:]

        # Items crossover (1-point crossover)
        child_items = [items1[i] if random.random() < 0.5 else items2[i] 
                       for i in range(len(items1))]
        
        return child_route, child_items

    def mutate(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        
        # Swap mutation for route
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        
        # Random mutation for items
        for i in range(len(items)):
            if random.random() < self.mutation_rate:
                items[i] = 1 - items[i]  # Flip between 0 and 1
                
        return route, items
