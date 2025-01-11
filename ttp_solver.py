# DESCRIPTION: This file contains the implementation of the TTPSolver class which is responsible for solving the TTP problem using the Genetic Algorithm.

'''File Contains:
    1. TTPSolver class: This class is used to solve the TTP problem by implementing the necessary functions.'''

''' Inside TTPSolver class
    1. __init__ function: This function initializes the TTPSolver class with the given parameters.'''


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