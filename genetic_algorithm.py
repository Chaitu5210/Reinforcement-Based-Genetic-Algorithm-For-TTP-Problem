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
from crossover import CrossoverMethods
from mutation import MutationTypes
from parent_selection import ParentSelectionStrategies

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

    def select_parents(self, population: List[List[int]], fitness_scores: List[float], evalution) -> List[Tuple[List[int], List[int]]]:
        selector = ParentSelectionStrategies()
        if evalution:
            method_name = "truncation_selection"
        else:
            method_name = random.choice(["truncation_selection", "tournament_top_10", "roulette_wheel_selection", "tournament_selection", "rank_selection", "stochastic_universal_sampling"])
        selected_parents = selector.call_method(method_name, population, fitness_scores)
        return selected_parents



    def mutate(self, solution: Tuple[List[int], List[int]], evalution) -> Tuple[List[int], List[int]]:
        mutation_types = MutationTypes(mutation_rate=self.mutation_rate)
        if evalution:
            mutation_name = "scramble_mutation"
        else:
            mutation_name = random.choice(["bit_flip_mutation", "random_item_swap_mutation","scramble_mutation","inversion_mutation","reset_mutation","block_flip_mutation", "gaussian_mutation"])
        mutated_solution = mutation_types.apply_mutation(mutation_name, solution)
        return mutated_solution


    # Two Point Crossover
    def crossover(self, parent1: Tuple[List[int], List[int]], 
                parent2: Tuple[List[int], List[int]], evalution) -> Tuple[List[int], List[int]]:
        # return child_route, child_items
        crossover_methods = CrossoverMethods()
        if evalution:
            method_name = "two_point"
        else:
            method_name = random.choice(["single_point", "two_point", "uniform","arithmetic"])
        child = crossover_methods.crossover(method_name, parent1, parent2)
        return child