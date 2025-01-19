# Description: This file contains the implementation of the genetic algorithm used to solve the TTP problem.

'''File Contains:
1. GeneticAlgorithm class: This class
    - Initializes the genetic algorithm with population size, mutation rate, and number of generations.    
    - Initializes the population with random picking plans and routes.
    - Selects parents using tournament selection.
    - Performs crossover and mutation operations.'''

'''2. check_weight_status function: This function is used to check if the weight exceeds the capacity and 
                                if it does, it removes the items with the highest weight.'''



# Importing required libraries
import random
from typing import List, Tuple
from route_generator import generate_route, calculate_total_distance
from ttp_solver import TTPSolver

# check_weight_status function is used to check if the weight exceeds the capacity and if it does, it removes the items with the highest weight
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


# GeneticAlgorithm class is used to implement the genetic algorithm for solving the TTP problem
class GeneticAlgorithm:

    # Initialize the genetic algorithm with population size, mutation rate, and number of generations
    def __init__(self, population_size: int, mutation_rate: float, generations: int):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations


    # Initialize the population with random picking plans and routes
    def initialize_population(self, num_cities, num_items: int, items, ttp_solver) -> List[Tuple[List[int], List[int]]]:
        population = []
        route = generate_route(num_cities)
        distance = calculate_total_distance(route,num_cities)
        for _ in range(self.population_size):
            picking_plan = [random.randint(0, 1) for _ in range(num_items)]
            
            # check weight status checks if the weight exceeds the capacity and if it does, it removes the items with the highest weight
            final_picking_plan, weight = check_weight_status(picking_plan, items, ttp_solver, route)
            population.append((route, final_picking_plan))

        return population, distance
    
    
    # truncation_selection
    def select_parents(self, population: List[List[int]], fitness_scores: List[float]) -> List[Tuple[List[int], List[int]]]:
        def truncation_selection(population, fitness_scores, truncation_size=2):
            sorted_population = sorted(zip(fitness_scores, population), key=lambda x: x[0])
            selected_parents = [individual for _, individual in sorted_population[:truncation_size]]
            return selected_parents 
        parents = truncation_selection(population, fitness_scores)
        return parents
    

    def mutate(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        for i in range(len(items)):
            if random.random() < self.mutation_rate:
                items[i] = 1 - items[i]
        return route, items


    # Two Point Crossover
    def crossover(self, parent1: Tuple[List[int], List[int]], 
                parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2
        child_route = route1  
        point1 = random.randint(0, len(items1) - 1)
        point2 = random.randint(0, len(items1) - 1)
        if point1 > point2:
            point1, point2 = point2, point1
        child_items = (
            items1[:point1] +       
            items2[point1:point2] +  
            items1[point2:]          
        )
        return child_route, child_items
