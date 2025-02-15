# Description: Main file to run the Genetic Algorithm for the TTP problem

'''File Contains:
    1. run_genetic_algorithm function: This function is used to run the Genetic Algorithm for the given benchmark file.
    2. pareto_front_plot function: This function is used to plot the Pareto Front for the given data.
    3. main function: This function is used to parse command line arguments and run the Genetic Algorithm.'''


# Importing required libraries
import argparse
from ttp_solver import TTPSolver
from genetic_algorithm import GeneticAlgorithm
from fitness_function import calculate_fitness
from ttp_benchmark_solver import read_benchmark_file, generate_items
import matplotlib.pyplot as plt 
from genetic_algorithm import check_weight_status
import random
import time
from child_to_population import ChildToPopulationTypes
from Q_learning import QLearning


# Runs the Genetic Algorithm for the given benchmark file
def run_genetic_algorithm(name: str, filename: str, population_size: int, mutation_rate: float, generations: int):



    # Read benchmark data
    benchmark_data = read_benchmark_file(filename)

    # Initialize pareto front
    pareto_front = []

    items = generate_items(f'{filename}')

    # Initialize TTPSolver
    ttp_solver = TTPSolver(
        cities=benchmark_data['cities'],
        items=items,
        capacity=benchmark_data['capacity'],
        min_speed=benchmark_data['min_speed'],
        max_speed=benchmark_data['max_speed'],
        renting_ratio=benchmark_data['renting_ratio']
    )


    # Initialize Genetic Algorithm
    ga = GeneticAlgorithm(population_size, mutation_rate, generations)

    # Initialize population
    population, distance = ga.initialize_population(benchmark_data['cities'], len(items),items, ttp_solver)
    
    best_fitness_history = []
    best_solution = None
    best_overall_fitness = float('-inf')

    prev_population = None
    prev_best_fitness = float('-inf')
    
    # Reset all_weights for each iteration
    all_weights = []


    # Initialize Q-Learning(Reinforcement Learning) Algorithm
    QL = QLearning(learning_rate=0.1, discount_factor=0.95, epsilon=0.1)
    current_state = (0, 0, 0, 0)


    # Run the Genetic Algorithm
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

        # Update best overall fitness and solution
        if best_fitness > best_overall_fitness:
            best_overall_fitness = best_fitness
            best_solution = population[fitness_scores.index(best_fitness)]

        # Check if the algorithm has converged
        if generation >= 150000 and all(x == best_fitness_history[generation - 500] for x in best_fitness_history[generation - 500: generation + 1]):
            evolution = False
        else:
            evolution = True

        print(f"{name} - Generation {generation}: Best Fitness = {best_fitness}")

        # Check if the best fitness has improved from the previous generation
        if best_fitness < prev_best_fitness:
            print(f"{name} - Generation {generation}: Reverting to previous generation's population")
            population = prev_population  
            best_fitness_history[-1] = prev_best_fitness  
            continue 

        # Store the current population and best fitness for the next iteration
        prev_population = population[:]
        prev_best_fitness = best_fitness


        # Select parents based on fitness
        parents = ga.select_parents(population, fitness_scores, evolution, current_state[0])
        parent1 = parents[0]
        parent2 = parents[1]

        # Generate new population using crossover and mutation
        child = ga.crossover(parent1, parent2, evolution, current_state[1])
        child = ga.mutate(child, evolution, current_state[2])
        route = child[0]
        # Check weight status and add to new population
        final_child, weight = check_weight_status(child[1], items, ttp_solver, route)
        temp_final_child = (route, final_child)



        diff_strategy = ["replace_bottom_20_percent","replace_lowest_fitness","replace_based_on_fitness_probability", "replace_lowest_fitness"]
        strategy = diff_strategy[current_state[3]]
        population_manager = ChildToPopulationTypes(ga)
        new_population = population_manager.replace(strategy, population, fitness_scores, temp_final_child)

        population = new_population

        if generation == 0:
            before_fitness = best_fitness
        else:

            action = QL.choose_action(current_state)
            next_state = QL.get_next_state(current_state, action)

            # Allocating Reward
            reward = best_fitness - before_fitness
            QL.update(current_state, action, reward, next_state)

            current_state = next_state
            before_fitness = best_fitness
        

    best_strategies = QL.get_best_strategies()
    print(f"Best Strategies: {best_strategies}")

    # pareto_front_plot(pareto_front)

    return best_fitness_history, best_overall_fitness, best_solution, max(all_weights)



# Plots the Pareto Front for the given data
def pareto_front_plot(pareto_front, title="Pareto Front"):
    plt.figure(figsize=(8, 6))
    for generation_index, generation in enumerate(pareto_front):
        weights, profits = zip(*generation)
        plt.scatter(weights, profits, marker='o')
    plt.xlabel('Weight')
    plt.ylabel('Profit')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()


# Main function to run the Genetic Algorithm
def main():
    start_time = time.time()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='TTP Solver with Genetic Algorithm')

    # # Eil76 (DATASET - 1) (CAT-1)
    parser.add_argument('--files', nargs='+', default=['DATASET/eil76.txt'], help='Input benchmark files')

    # # KroA100 (DATASET - 2) (CAT-2)
    # parser.add_argument('--files', nargs='+', default=['DATASET/KroA100.txt'], help='Input benchmark files')

    # # ch130 (DATASET - 3) (CAT-3)
    # parser.add_argument('--files', nargs='+', default=['DATASET/ch130.txt'], help='Input benchmark files')

    # # U159 (DATASET - 4) (CAT-3)
    # parser.add_argument('--files', nargs='+', default=['DATASET/U159.txt'], help='Input benchmark files')

    # # A280 (DATASET - 5) (CAT-1)
    # parser.add_argument('--files', nargs='+', default=['DATASET/A280.txt'], help='Input benchmark files')

    


    # # eil 51 is used for testing
    # these are all the inputs that can be used
    # parser.add_argument('--files', nargs='+', default=['DATASET/eil51_n50_bounded-strongly-corr_01.ttp'], help='Input benchmark files')
    parser.add_argument('--population', type=int, default=200, help='Population size')
    parser.add_argument('--mutation', type=float, default=0.05, help='Mutation rate')
    parser.add_argument('--generations', type=int, default=2000, help='Number of generations')
    parser.add_argument('--itrations', type=int, default=1, help='Number of iterations')

    args = parser.parse_args()

    final_results = []

    # Open a file to log the results
    with open("results_log.txt", "w") as log_file:
        log_file.write("Iteration\tBest Fitness\tMax Weight\n")  
        for run in range(args.itrations):  
            run_results = []
            main_weights = []

            for idx, file in enumerate(args.files):
                # from here we will call the genetic algorithm
                ga_results = run_genetic_algorithm(  
                    f"GA-{idx+1}",
                    file,
                    args.population,
                    args.mutation,
                    args.generations
                )
                run_results.append(ga_results)
                main_weights.append(run_results[0][3]) 

            # Get the best fitness and max weight for the run
            best_fitness = max([result[1] for result in run_results])  
            max_weight = max(main_weights)
            main_weights = []

            # Log the best fitness and max weight to the file
            log_file.write(f"{run + 1}\t{best_fitness}\t{max_weight}\n")
            log_file.flush()

            print(f'Final weight for iteration {run + 1} is {max_weight}')

            # Plot the results for the run
            plt.figure(figsize=(12, 6))
            for idx, result in enumerate(run_results):
                plt.plot(result[0], label=f'GA-{idx+1} (Run {run+1})')
                print(f"\nRun {run+1}, GA-{idx+1} Best Fitness: {result[1]}")
            plt.xlabel('Generation')
            plt.ylabel('Best Fitness')
            plt.title(f'Genetic Algorithm Performance Comparison - Run {run+1}')
            plt.legend()
            # plt.grid(True)
            plt.savefig(f'ga_comparison_run_{run+1}.png')
            plt.show()


            # Append the best fitness to the final results
            final_results.append(best_fitness)

        # Calculate the average best fitness over all runs
        print("\nFinal Results are:", final_results)
        print("max value is ",max(final_results))
        end_time = time.time()
        print(f'total time taken was {end_time-start_time}')


if __name__ == "__main__":
    main()