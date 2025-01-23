import random
from typing import List, Tuple


class MutationTypes:
    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def bit_flip_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        for i in range(len(items)):
            if random.random() < self.mutation_rate:
                items[i] = 1 - items[i]  # Flip the bit (0 -> 1, 1 -> 0)
        return route, items

    def random_item_swap_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(items)), 2)
            items[idx1], items[idx2] = items[idx2], items[idx1]
        return route, items

    def scramble_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        if random.random() < self.mutation_rate:
            start = random.randint(0, len(items) - 2)
            end = random.randint(start + 1, len(items))
            sub_items = items[start:end]
            random.shuffle(sub_items)
            items[start:end] = sub_items
        return route, items

    def inversion_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        if random.random() < self.mutation_rate:
            start = random.randint(0, len(items) - 2)
            end = random.randint(start + 1, len(items))
            items[start:end] = items[start:end][::-1]
        return route, items

    def reset_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(items) - 1)
            items[idx] = random.choice([0, 1])
        return route, items

    def block_flip_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        if random.random() < self.mutation_rate:
            start = random.randint(0, len(items) - 2)
            end = random.randint(start + 1, len(items))
            for i in range(start, end):
                items[i] = 1 - items[i]
        return route, items

    def gaussian_mutation(self, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        route, items = solution
        if random.random() < self.mutation_rate:
            for i in range(len(items)):
                if random.random() < self.mutation_rate:
                    items[i] = max(0, min(1, items[i] + random.gauss(0, 0.1)))  # Clamping to [0,1]
        return route, items

    def apply_mutation(self, mutation_name: str, solution: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
        """
        Apply a mutation method based on its name.

        :param mutation_name: The name of the mutation method as a string.
        :param solution: A tuple containing route and items.
        :return: Mutated solution.
        """
        # Retrieve the method by name using `getattr`
        if hasattr(self, mutation_name):
            mutation_method = getattr(self, mutation_name)
            if callable(mutation_method):
                return mutation_method(solution)
        raise ValueError(f"Mutation method '{mutation_name}' not found or not callable.")
