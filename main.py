import random
import argparse
from ttp_solver import TTPSolver
from genetic_algorithm import GeneticAlgorithm
from fitness_function import calculate_fitness
from ttp_benchmark_solver import read_benchmark_file, generate_items

def run_genetic_algorithm(name: str, filename: str, population_size: int, mutation_rate: float, generations: int):
    benchmark_data = read_benchmark_file(filename)
    num_items = len(benchmark_data.get('items', [])) or 2790
    
    items = generate_items(benchmark_data['dimension'], num_items)
    
    ttp_solver = TTPSolver(
        cities=benchmark_data['cities'],
        items=items,
        capacity=benchmark_data['capacity'],
        min_speed=benchmark_data['min_speed'],
        max_speed=benchmark_data['max_speed'],
        renting_ratio=benchmark_data['renting_ratio']
    )
    
    ga = GeneticAlgorithm(population_size, mutation_rate, generations)
    population = ga.initialize_population(len(benchmark_data['cities']), len(items))
    
    best_fitness_history = []
    best_solution = None
    best_overall_fitness = float('-inf')
    
    for generation in range(ga.generations):
        fitness_scores = [calculate_fitness(solution, ttp_solver) for solution in population]
        best_fitness = max(fitness_scores)
        best_fitness_history.append(best_fitness)

        if best_fitness > best_overall_fitness:
            best_overall_fitness = best_fitness
            best_solution = population[fitness_scores.index(best_fitness)]
        
        print(f"{name} - Generation {generation}: Best Fitness = {best_fitness}")
        
        # Select parents based on fitness
        parents = ga.select_parents(population, fitness_scores)
        
        new_population = []
        for i in range(0, len(parents), 2):  # Process in pairs
            parent1 = parents[i]
            parent2 = parents[i + 1] if i + 1 < len(parents) else parents[0]
            child = ga.crossover(parent1, parent2)
            child = ga.mutate(child)
            new_population.append(child)

        # Fill the remaining slots in the new population with parents if needed
        while len(new_population) < ga.population_size:
            new_population.append(random.choice(parents))

        population = new_population
        
    return best_fitness_history, best_overall_fitness, best_solution




def main():
    parser = argparse.ArgumentParser(description='TTP Solver with Genetic Algorithm')
    parser.add_argument('--files', nargs='+', required=True, help='Input benchmark files')
    parser.add_argument('--population', type=int, default=200, help='Population size')
    parser.add_argument('--mutation', type=float, default=0.05, help='Mutation rate')
    parser.add_argument('--generations', type=int, default=2, help='Number of generations')
    
    args = parser.parse_args()
    
    results = []
    for idx, file in enumerate(args.files):
        ga_results = run_genetic_algorithm(
            f"GA-{idx+1}",
            file,
            args.population,
            args.mutation,
            args.generations
        )
        results.append(ga_results)
    
    # Plot comparison
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    for idx, result in enumerate(results):
        plt.plot(result[0], label=f'GA-{idx+1}')
        print(f"\nGA-{idx+1} Best Fitness: {result[1]}")
    
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Genetic Algorithm Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('ga_comparison.png')
    plt.show()

if __name__ == "__main__":
    main()





# when we are comparing the same single benchmark with various population size, mutation rate, generations
# import random
# from ttp_solver import TTPSolver
# from genetic_algorithm import GeneticAlgorithm
# from fitness_function import calculate_fitness
# from ttp_benchmark_solver import read_benchmark_file,generate_items
# def run_genetic_algorithm(name: str, population_size: int, mutation_rate: float, generations: int):
#     benchmark_data = read_benchmark_file('a280_n.txt')
#     items = generate_items(benchmark_data['dimension'], 2790)
    
#     ttp_solver = TTPSolver(
#         cities=benchmark_data['cities'],
#         items=items,
#         capacity=benchmark_data['capacity'],
#         min_speed=benchmark_data['min_speed'],
#         max_speed=benchmark_data['max_speed'],
#         renting_ratio=benchmark_data['renting_ratio']
#     )
    
#     ga = GeneticAlgorithm(population_size, mutation_rate, generations)
#     population = ga.initialize_population(len(benchmark_data['cities']), len(items))
    
#     best_fitness_history = []
#     best_solution = None
#     best_overall_fitness = float('-inf')
    
#     for generation in range(ga.generations):
#         fitness_scores = [calculate_fitness(solution, ttp_solver) for solution in population]
#         best_fitness = max(fitness_scores)
#         best_fitness_history.append(best_fitness)
        
#         if best_fitness > best_overall_fitness:
#             best_overall_fitness = best_fitness
#             best_solution = population[fitness_scores.index(best_fitness)]
            
#         print(f"{name} - Generation {generation}: Best Fitness = {best_fitness}")
        
#         parents = random.choices(population, weights=fitness_scores, k=ga.population_size)
#         new_population = []
#         for i in range(0, ga.population_size, 2):
#             parent1 = parents[i]
#             parent2 = parents[i + 1] if i + 1 < ga.population_size else parents[0]
#             child = ga.crossover(parent1, parent2)
#             child = ga.mutate(child)
#             new_population.append(child)
#         population = new_population
        
#     return best_fitness_history, best_overall_fitness, best_solution

# def main():
#     # Run multiple GA variants
#     ga1_results = run_genetic_algorithm("GA-1", population_size=200, mutation_rate=0.05, generations=2)
#     ga2_results = run_genetic_algorithm("GA-2", population_size=300, mutation_rate=0.02, generations=2)
    
#     # Compare results
#     print("\nComparison Results:")
#     print(f"GA-1 Best Fitness: {ga1_results[1]}")
#     print(f"GA-2 Best Fitness: {ga2_results[1]}")
    
#     # Plot comparison
#     import matplotlib.pyplot as plt
#     plt.figure(figsize=(12, 6))
#     plt.plot(ga1_results[0], label='GA-1')
#     plt.plot(ga2_results[0], label='GA-2')
#     plt.xlabel('Generation')
#     plt.ylabel('Best Fitness')
#     plt.title('Genetic Algorithm Performance Comparison')
#     plt.legend()
#     plt.grid(True)
#     plt.savefig('ga_comparison.png')
#     plt.show()

# if __name__ == "__main__":
#     main()
