import numpy as np
from typing import List, Tuple
import random

class TTPSolver:
    def __init__(self, cities: List[Tuple[int, int]], items: List[Tuple[float, float]], 
                 capacity: float, min_speed: float, max_speed: float, renting_ratio: float):
        self.cities = cities
        self.items = items  # (weight, value) pairs
        self.capacity = capacity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.renting_ratio = renting_ratio
        self.num_cities = len(cities)
        self.num_items = len(items)
        
    def calculate_distance(self, city1: Tuple[int, int], city2: Tuple[int, int]) -> float:
        # print(f"Calculating distance between {city1} and {city2}")
        return np.ceil(np.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2))
    
    def calculate_total_distance(self, route: List[int]) -> float:
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.calculate_distance(self.cities[route[i]], self.cities[route[i+1]])
        return total_distance + self.calculate_distance(self.cities[route[-1]], self.cities[route[0]])
    
    def calculate_speed(self, current_weight: float) -> float:
        weight_ratio = current_weight / self.capacity
        return max(self.min_speed, self.max_speed - weight_ratio * (self.max_speed - self.min_speed))
