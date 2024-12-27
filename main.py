import random
import argparse
from ttp_solver import TTPSolver
from genetic_algorithm import GeneticAlgorithm
from fitness_function import calculate_fitness
from ttp_benchmark_solver import read_benchmark_file, generate_items
import matplotlib.pyplot as plt 

def run_genetic_algorithm(name: str, filename: str, population_size: int, mutation_rate: float, generations: int):
    benchmark_data = read_benchmark_file(filename)
    num_items = benchmark_data.get('items')

    items = generate_items("DATASET/a29.txt")

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

    prev_population = None  # To store the population of the previous generation
    prev_best_fitness = float('-inf')

    for generation in range(ga.generations):
        fitness_scores = [calculate_fitness(solution, ttp_solver) for solution in population]
        best_fitness = max(fitness_scores)
        best_fitness_history.append(best_fitness)

        if best_fitness > best_overall_fitness:
            best_overall_fitness = best_fitness
            best_solution = population[fitness_scores.index(best_fitness)]

        print(f"{name} - Generation {generation}: Best Fitness = {best_fitness}")

        # Check if the current generation's fitness is less than the previous generation's fitness
        if best_fitness < prev_best_fitness:
            print(f"{name} - Generation {generation}: Reverting to previous generation's population")
            population = prev_population  # Revert to the previous generation's population
            best_fitness_history[-1] = prev_best_fitness  # Update fitness history with the previous best fitness
            continue  # Skip the rest of the loop to maintain the previous generation's state

        # Store the current population and fitness as the previous state for the next generation
        prev_population = population[:]
        prev_best_fitness = best_fitness

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
    parser.add_argument('--files', nargs='+', default=['DATASET/eil51_n50_bounded-strongly-corr_01.ttp'], help='Input benchmark files')
    parser.add_argument('--population', type=int, default=200, help='Population size')
    parser.add_argument('--mutation', type=float, default=0.05, help='Mutation rate')
    parser.add_argument('--generations', type=int, default=2000, help='Number of generations')
    parser.add_argument('--itrations', type=int, default=1, help='Number of iterations')

    args = parser.parse_args()

    final_results = []

    for run in range(args.itrations):  
        run_results = []

        for idx, file in enumerate(args.files):
            ga_results = run_genetic_algorithm(  
                f"GA-{idx+1}",
                file,
                args.population,
                args.mutation,
                args.generations
            )
            run_results.append(ga_results)

        # Plot comparison for this run
        plt.figure(figsize=(12, 6))
        for idx, result in enumerate(run_results):
            plt.plot(result[0], label=f'GA-{idx+1} (Run {run+1})')
            print(f"\nRun {run+1}, GA-{idx+1} Best Fitness: {result[1]}")

        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title(f'Genetic Algorithm Performance Comparison - Run {run+1}')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'ga_comparison_run_{run+1}.png')
        plt.show()

        final_results.append(result[1])

    print("\n Final Results are :", final_results)

if __name__ == "__main__":
    main()
