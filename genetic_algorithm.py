import random
import numpy as np
from typing import List, Tuple
from route_generator import generate_route, calculate_total_distance


class GeneticAlgorithm:
    def __init__(self, population_size: int, mutation_rate: float, generations: int):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def initialize_population(self, num_cities, num_items: int) -> List[Tuple[List[int], List[int]]]:
        population = []
        for _ in range(self.population_size):
            route = generate_route(num_cities)
            distance = calculate_total_distance(route,num_cities)
            picking_plan = [random.randint(0, 1) for _ in range(num_items)]
            population.append((route, picking_plan))
        return population, distance
    
    def random_population_generator(self, num_cities, required_population ,num_items: int) -> List[Tuple[List[int], List[int]]]:

        population = []
        route = generate_route(num_cities)

        for _ in range(required_population):
            picking_plan = [random.randint(0, 1) for _ in range(num_items)]
            population.append((route, picking_plan))
        return population
    


    # Using tournament selection
    def select_parents(self, population, fitness_scores, tournement_size=2) -> List[Tuple[List[int], List[int]]]:

        top_two_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:tournement_size]
        parents = [population[i] for i in top_two_indices]
        return parents

    # Using uniform crossover for only the items as route is already optimized
    def crossover(self, parent1: Tuple[List[int], List[int]], 
              parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2

        child_route = route1 

        child_items = [items1[i] if random.random() < 0.5 else items2[i] 
                    for i in range(len(items1))]
        
        return child_route, child_items


    def mutate(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        
        # Swap mutation for route
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        
        for i in range(len(items)):
            if random.random() < self.mutation_rate:
                items[i] = 1 - items[i]
                
        return route, items
