import random
from typing import List, Tuple

class ParentSelectionStrategies:
    def __init__(self):
        # Mapping method names to actual methods
        self.methods = {
            "tournament_top_10": self.tournament_top_10,
            "roulette_wheel_selection": self.roulette_wheel_selection,
            "tournament_selection": self.tournament_selection,
            "rank_selection": self.rank_selection,
            "stochastic_universal_sampling": self.stochastic_universal_sampling,
            "truncation_selection": self.truncation_selection,
        }

    def call_method(self, method_name: str, population: List[List[int]], fitness_scores: List[float], **kwargs):
        """Dynamically call a method based on its name."""
        if method_name in self.methods:
            return self.methods[method_name](population, fitness_scores, **kwargs)
        else:
            raise ValueError(f"Method {method_name} not found.")

    # Selection Methods
    def tournament_top_10(self, population: List[List[int]], fitness_scores: List[float]) -> List[Tuple[List[int], List[int]]]:
        top_10_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:10]
        top_10_parents = [population[i] for i in top_10_indices]
        parent1 = random.choice(top_10_parents)
        remaining_population = [individual for i, individual in enumerate(population) if individual not in top_10_parents]
        parent2 = random.choice(remaining_population)
        return [parent1, parent2]

    def roulette_wheel_selection(self, population: List[List[int]], fitness_scores: List[float]) -> List[Tuple[List[int], List[int]]]:
        total_fitness = sum(fitness_scores)
        selection_probs = [fitness / total_fitness for fitness in fitness_scores]
        parent1 = random.choices(population, weights=selection_probs, k=1)[0]
        parent2 = random.choices(population, weights=selection_probs, k=1)[0]
        return [parent1, parent2]

    def tournament_selection(self, population: List[List[int]], fitness_scores: List[float], tournament_size=3) -> List[Tuple[List[int], List[int]]]:
        def tournament(population, fitness_scores, tournament_size):
            tournament_indices = random.sample(range(len(population)), tournament_size)
            best_index = min(tournament_indices, key=lambda i: fitness_scores[i])
            return population[best_index]
        parent1 = tournament(population, fitness_scores, tournament_size)
        parent2 = tournament(population, fitness_scores, tournament_size)
        return [parent1, parent2]

    def rank_selection(self, population: List[List[int]], fitness_scores: List[float]) -> List[Tuple[List[int], List[int]]]:
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])
        rank_probs = [1 / (rank + 1) for rank in range(len(sorted_indices))]
        total_rank_prob = sum(rank_probs)
        normalized_probs = [rank_prob / total_rank_prob for rank_prob in rank_probs]
        parent1 = random.choices(population, weights=normalized_probs, k=1)[0]
        parent2 = random.choices(population, weights=normalized_probs, k=1)[0]
        return [parent1, parent2]

    def stochastic_universal_sampling(self, population: List[List[int]], fitness_scores: List[float], num_parents=2) -> List[Tuple[List[int], List[int]]]:
        total_fitness = sum(fitness_scores)
        distance = total_fitness / num_parents
        start_point = random.uniform(0, distance)
        pointers = [start_point + i * distance for i in range(num_parents)]
        selected_parents = []
        for pointer in pointers:
            current_sum = 0
            for i, fitness in enumerate(fitness_scores):
                current_sum += fitness
                if current_sum >= pointer:
                    selected_parents.append(population[i])
                    break
        return selected_parents

    def truncation_selection(self, population: List[List[int]], fitness_scores: List[float], truncation_size=2) -> List[Tuple[List[int], List[int]]]:
        sorted_population = sorted(zip(fitness_scores, population), key=lambda x: x[0])
        selected_parents = [individual for _, individual in sorted_population[:truncation_size]]
        return selected_parents
