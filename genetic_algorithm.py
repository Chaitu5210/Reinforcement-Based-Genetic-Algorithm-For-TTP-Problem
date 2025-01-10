import random
import numpy as np
from typing import List, Tuple
from route_generator import generate_route, calculate_total_distance
from ttp_solver import TTPSolver


def check_weight_status(picking_plan: List[int], items, ttp_solver: 'TTPSolver', route):
        weights = [item[0] for item in items]
        weights = [weights[i] for i in route]

        total_weight = sum([weights[i] for i in range(len(picking_plan)) if picking_plan[i] == 1])
        if total_weight > ttp_solver.capacity:
            selected_indices = [i for i in range(len(picking_plan)) if picking_plan[i] == 1]
            sorted_indices = sorted(selected_indices, key=lambda x: weights[x], reverse=True)
            for idx in sorted_indices:
                if total_weight <= ttp_solver.capacity:
                    break
                picking_plan[idx] = 0
                total_weight -= weights[idx]
        return picking_plan, total_weight


class GeneticAlgorithm:

    def __init__(self, population_size: int, mutation_rate: float, generations: int):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations


    def initialize_population(self, num_cities, num_items: int, items, ttp_solver) -> List[Tuple[List[int], List[int]]]:
        population = []
        route = generate_route(num_cities)
        distance = calculate_total_distance(route,num_cities)
        for _ in range(self.population_size):
            picking_plan = [random.randint(0, 1) for _ in range(num_items)]
            final_picking_plan, weight = check_weight_status(picking_plan, items, ttp_solver, route)
            # print("picking plan outside: ", final_picking_plan)
            # print(f'after weight: {weight}')
            population.append((route, final_picking_plan))
        # print("complete picking plan: ", population)
        return population, distance
    

    
    def random_population_generator(self, num_cities, required_population ,num_items: int, items, ttp_solver) -> List[Tuple[List[int], List[int]]]:
        population = []
        route = generate_route(num_cities)
        for _ in range(required_population):
            picking_plan = [random.randint(0, 1) for _ in range(num_items)]
            # print("picking plan before: ", picking_plan)
            final_picking_plan, weight = check_weight_status(picking_plan, items, ttp_solver, route)
            population.append((route, final_picking_plan))
        return population
    

    # Using tournament selection
    def select_parents(self, population: List[List[int]], fitness_scores: List[float]) -> List[Tuple[List[int], List[int]]]:
        parents = []
        top_10_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:10]
        top_10_parents = [population[i] for i in top_10_indices]
        parent1 = random.choice(top_10_parents)
        remaining_population = [individual for i, individual in enumerate(population) if individual != parent1]
        parent2 = random.choice(remaining_population)
        parents.append(parent1)
        parents.append(parent2)
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
