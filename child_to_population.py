import random
from typing import List

class ChildToPopulationTypes:
    def __init__(self, ga):
        self.ga = ga  # Assuming ga is an object that has the `calculate_similarity` method

    def replace(self, method_name: str, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        method_mapping = {
            "replace_lowest_fitness": self.replace_lowest_fitness,
            "replace_bottom_20_percent": self.replace_bottom_20_percent,
            "replace_based_on_fitness_probability": self.replace_based_on_fitness_probability,
        }
        
        if method_name in method_mapping:
            return method_mapping[method_name](population, fitness_scores, temp_final_child)
        else:
            raise ValueError(f"Method '{method_name}' not found in method mapping.")
    
    # Strategy 1: Replace the individual with the lowest fitness (original approach)
    def replace_lowest_fitness(self, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        min_fitness_index = fitness_scores.index(min(fitness_scores))
        population[min_fitness_index] = temp_final_child
        return population

    # Strategy 2: Replace a randomly selected individual from the bottom 20% of the population
    def replace_bottom_20_percent(self, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        bottom_20_percent = int(len(fitness_scores) * 0.2)
        bottom_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])[:bottom_20_percent]
        random_index = random.choice(bottom_indices)
        population[random_index] = temp_final_child
        return population

    # Strategy 4: Replace an individual based on a weighted probability of fitness
    def replace_based_on_fitness_probability(self, population: List[List[int]], fitness_scores: List[float], temp_final_child: List[int]) -> List[List[int]]:
        fitness_weights = [1 / (fitness + 1e-6) for fitness in fitness_scores]  # Avoid division by zero
        cumulative_weights = [sum(fitness_weights[:i+1]) for i in range(len(fitness_weights))]
        total_weight = cumulative_weights[-1]
        random_value = random.uniform(0, total_weight)
        selected_index = next(i for i, weight in enumerate(cumulative_weights) if weight > random_value)
        population[selected_index] = temp_final_child
        return population
