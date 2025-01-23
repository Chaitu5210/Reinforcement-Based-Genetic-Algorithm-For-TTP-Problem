import random
from typing import List

class ChildToPopulationTypes:
    def __init__(self, ga=None):
        self.ga = ga  # Optional parameter with default None

    def replace(self, method_name: str, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        method_mapping = {
            "replace_lowest_fitness": self.replace_lowest_fitness,
            "replace_bottom_20_percent": self.replace_bottom_20_percent,
            "replace_based_on_fitness_probability": self.replace_based_on_fitness_probability,
        }
        
        replace_method = method_mapping.get(method_name)
        if replace_method:
            return replace_method(population, fitness_scores, temp_final_child)
        raise ValueError(f"Method '{method_name}' not found in method mapping.")
    
    def replace_lowest_fitness(self, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        min_fitness_index = fitness_scores.index(min(fitness_scores))
        population[min_fitness_index] = temp_final_child
        return population

    def replace_bottom_20_percent(self, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        bottom_20_percent = int(len(fitness_scores) * 0.2)
        bottom_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])[:bottom_20_percent]
        random_index = random.choice(bottom_indices)
        population[random_index] = temp_final_child
        return population

    def replace_based_on_fitness_probability(self, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        fitness_weights = [1 / (fitness + 1e-6) for fitness in fitness_scores]
        total_weight = sum(fitness_weights)
        selected_index = random.choices(range(len(population)), weights=fitness_weights, k=1)[0]
        population[selected_index] = temp_final_child
        return population

