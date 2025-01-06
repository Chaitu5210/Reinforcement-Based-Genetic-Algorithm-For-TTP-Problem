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

    pareto_front = []

    items = generate_items(f'{filename}')

    ttp_solver = TTPSolver(
        cities=benchmark_data['cities'],
        items=items,
        capacity=benchmark_data['capacity'],
        min_speed=benchmark_data['min_speed'],
        max_speed=benchmark_data['max_speed'],
        renting_ratio=benchmark_data['renting_ratio']
    )

    ga = GeneticAlgorithm(population_size, mutation_rate, generations)
    population, distance = ga.initialize_population(benchmark_data['cities'], len(items))
    
    best_fitness_history = []
    best_solution = None
    best_overall_fitness = float('-inf')

    prev_population = None 
    prev_best_fitness = float('-inf')
    
    # Reset all_weights for each iteration
    all_weights = []

    for generation in range(ga.generations):
        scores = [calculate_fitness(solution, ttp_solver, distance) for solution in population]
        pareto_front.append(scores)
        fitness, weight = zip(*scores)
        
        # Convert to lists if necessary
        fitness_scores = list(fitness)
        weights = list(weight)
        all_weights.append(max(weights))

        best_fitness = max(fitness_scores)
        best_fitness_history.append(best_fitness)

        if best_fitness > best_overall_fitness:
            best_overall_fitness = best_fitness
            best_solution = population[fitness_scores.index(best_fitness)]

        print(f"{name} - Generation {generation}: Best Fitness = {best_fitness}")

        if best_fitness < prev_best_fitness:
            print(f"{name} - Generation {generation}: Reverting to previous generation's population")
            population = prev_population  
            best_fitness_history[-1] = prev_best_fitness  
            continue 

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
        required_population = ga.population_size - len(new_population)
        random_population = ga.random_population_generator(benchmark_data['cities'], required_population, len(items))
        random_population.append(new_population[0])
        population = random_population

    pareto_front_plot(pareto_front)

    return best_fitness_history, best_overall_fitness, best_solution, max(all_weights)

def pareto_front_plot(pareto_front, title="Pareto Front"):
    plt.figure(figsize=(8, 6))
    for generation_index, generation in enumerate(pareto_front):
        weights, profits = zip(*generation)
        # plt.scatter(weights, profits, label=f'Generation {generation_index + 1}', marker='o')
        plt.scatter(weights, profits, marker='o')

    plt.xlabel('Weight')
    plt.ylabel('Profit')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='TTP Solver with Genetic Algorithm')
    parser.add_argument('--files', nargs='+', default=['DATASET/eil51_n50_bounded-strongly-corr_01.ttp'], help='Input benchmark files')
    parser.add_argument('--population', type=int, default=200, help='Population size')
    parser.add_argument('--mutation', type=float, default=0.05, help='Mutation rate')
    parser.add_argument('--generations', type=int, default=2000, help='Number of generations')
    parser.add_argument('--itrations', type=int, default=1, help='Number of iterations')

    args = parser.parse_args()

    final_results = []

    # Open a file to log the results
    with open("results_log.txt", "w") as log_file:
        log_file.write("Iteration\tBest Fitness\tMax Weight\n")  # Header

        for run in range(args.itrations):  
            run_results = []
            main_weights = []  # Reset main_weights for each iteration

            for idx, file in enumerate(args.files):
                ga_results = run_genetic_algorithm(  
                    f"GA-{idx+1}",
                    file,
                    args.population,
                    args.mutation,
                    args.generations
                )
                run_results.append(ga_results)
                main_weights.append(run_results[0][3])  # Collect the max weight for this run

            best_fitness = max([result[1] for result in run_results])  # Best fitness in this iteration
            max_weight = max(main_weights)  # Max weight in this iteration
            main_weights = []

            # Log the best fitness and max weight to the file
            log_file.write(f"{run + 1}\t{best_fitness}\t{max_weight}\n")
            log_file.flush()  # Ensure the data is written to the file immediately

            print(f'Final weight for iteration {run + 1} is {max_weight}')

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

            final_results.append(best_fitness)


        print("\nFinal Results are:", final_results)

if __name__ == "__main__":
    main()
