import random
from typing import List, Tuple

class CrossoverMethods:
    def __init__(self):
        self.methods = {
            "single_point": self.single_point_crossover,
            "two_point": self.two_point_crossover,
            "arithmetic": self.arithmetic_crossover,
            "uniform": self.uniform_crossover
        }

    def crossover(self, method_name: str, parent1: Tuple[List[int], List[int]], parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        if method_name not in self.methods:
            raise ValueError(f"Crossover method '{method_name}' is not supported.")
        return self.methods[method_name](parent1, parent2)

    def single_point_crossover(self, parent1: Tuple[List[int], List[int]], parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2
        child_route = route1  # Keep the route static
        crossover_point = random.randint(1, len(items1) - 1)
        child_items = items1[:crossover_point] + items2[crossover_point:]
        return child_route, child_items

    def two_point_crossover(self, parent1: Tuple[List[int], List[int]], parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2
        child_route = route1  # Keep the route static
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

    def arithmetic_crossover(self, parent1: Tuple[List[int], List[int]], parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2
        child_route = route1  # Keep the route static
        alpha = random.uniform(0, 1)
        child_items = [
            round(alpha * items1[i] + (1 - alpha) * items2[i])
            for i in range(len(items1))
        ]
        return child_route, child_items

    def uniform_crossover(self, parent1: Tuple[List[int], List[int]], parent2: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route1, items1 = parent1
        route2, items2 = parent2
        child_route = route1  # Keep the route static
        child_items = [
            items1[i] if random.random() < 0.5 else items2[i]
            for i in range(len(items1))
        ]
        return child_route, child_items