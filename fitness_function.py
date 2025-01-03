from typing import List, Tuple
from ttp_solver import TTPSolver

def calculate_fitness(solution: Tuple[List[int], List[int]], ttp_solver: 'TTPSolver') -> float:
    route, picking_plan = solution
    # print(f"Route: {route}, Picking Plan: {picking_plan}")
    
    
    total_value = 0
    current_weight = 0
    total_time = 0

    # Constants for velocity adjustment
    MAX_VELOCITY = 1.0
    MIN_VELOCITY = 0.1
    VELOCITY_REDUCTION_FACTOR = 0.001
    distance = 0

    for i in range(1):  # Loop through all city transitions
        current_city = route[i]
        next_city = route[i + 1]

        # Process items in the current city
        city_value = 0
        for item_idx in range(len(picking_plan)):
            if picking_plan[item_idx] == 1:
                # print(f'item index: {item_idx}')
                weight, value = ttp_solver.items[item_idx]
                if current_weight + weight <= ttp_solver.capacity:
                    current_weight += weight
                    city_value += value
                    total_value += value
                    # print(f'updated city value: {current_weight} and item index: {item_idx}')
                else:
                    return 0,0

        # Adjust velocity based on current weight
        velocity = max(MIN_VELOCITY, MAX_VELOCITY - (current_weight * VELOCITY_REDUCTION_FACTOR))
        # print(f" Current City {current_city} next city {next_city}")
        # print("Before Distance ", distance)

        # Calculate distance and time for this segment
        distance = distance + ttp_solver.calculate_distance(
            ttp_solver.cities[current_city],
            ttp_solver.cities[next_city]
        )
        # print(f"After Distance: {distance}")
        time = distance / velocity
        total_time += time

    # Final segment: returning to the start city
    last_city = route[-1]
    first_city = route[0]
    distance = ttp_solver.calculate_distance(
        ttp_solver.cities[last_city],
        ttp_solver.cities[first_city]
    )
    velocity = max(MIN_VELOCITY, MAX_VELOCITY - (current_weight * VELOCITY_REDUCTION_FACTOR))
    time = distance / velocity
    total_time += time

    # print(f"total profit {total_value}")
    # print(f"total time {total_time}")
    # print(f"current weight {current_weight}")

    # Calculate rental cost based on total time
    # rental_cost = ttp_solver.renting_ratio * total_time
    # print(f"rental cost {rental_cost}")

    # Calculate total profit (value - rental cost)
    # total_profit = total_value - rental_cost
    total_profit = total_value

    # Penalize solutions exceeding capacity
    # if current_weight > ttp_solver.capacity:
    #     weight_penalty = (current_weight - ttp_solver.capacity) 
    #     total_profit -= weight_penalty

    # Return fitness score and current weight
    # print("-------------------")
    return max(0, round(total_profit, 2)), current_weight
