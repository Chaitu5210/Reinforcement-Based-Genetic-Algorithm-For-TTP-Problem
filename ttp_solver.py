# DESCRIPTION: This file contains the implementation of the TTPSolver class which is responsible for solving the TTP problem using the Genetic Algorithm.

'''File Contains:
    1. TTPSolver class: This class is used to solve the TTP problem by implementing the necessary functions.'''

''' Inside TTPSolver class
    1. __init__ function: This function initializes the TTPSolver class with the given parameters.
    2. calculate_distance function: This function calculates the distance between two cities.
    3. calculate_total_distance function: This function calculates the total distance of the route.
    4. calculate_speed function: This function calculates the speed based on the current weight.'''


# Importing required libraries
import numpy as np
from typing import List, Tuple

# TTPSolver class is used to solve the TTP problem
class TTPSolver:
    def __init__(self, cities: List[Tuple[int, int]], items: List[Tuple[float, float]], 
                 capacity: float, min_speed: float, max_speed: float, renting_ratio: float):
        self.cities = cities
        self.items = items  
        self.capacity = capacity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.renting_ratio = renting_ratio
        self.num_cities = len(cities)
        self.num_items = len(items)

    # calculate_distance function is used to calculate the distance between two cities
    def calculate_distance(self, city1: Tuple[int, int], city2: Tuple[int, int]) -> float:
        return np.ceil(np.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2))
    
    # calculate_total_distance function is used to calculate the total distance of the route
    def calculate_total_distance(self, route: List[int]) -> float:
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.calculate_distance(self.cities[route[i]], self.cities[route[i+1]])
        return total_distance + self.calculate_distance(self.cities[route[-1]], self.cities[route[0]])
    
    # calculate_speed function is used to calculate the speed based on the current weight
    def calculate_speed(self, current_weight: float) -> float:
        weight_ratio = current_weight / self.capacity
        return max(self.min_speed, self.max_speed - weight_ratio * (self.max_speed - self.min_speed))
