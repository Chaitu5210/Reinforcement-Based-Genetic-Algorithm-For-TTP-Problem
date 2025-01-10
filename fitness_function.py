from typing import List, Tuple
from ttp_solver import TTPSolver

def calculate_fitness(solution: Tuple[List[int], List[int]], ttp_solver: 'TTPSolver', distance: float) -> float:
    route, picking_plan = solution

    total_value = 0
    current_weight = 0
    
    MAX_VELOCITY = 1.0
    MIN_VELOCITY = 0.1
    VELOCITY_REDUCTION_FACTOR = 0.001


    # Process items in picking plan
    for item_idx in range(len(picking_plan)):
        if picking_plan[item_idx] == 1:
            weight, value = ttp_solver.items[route[item_idx]]
            # print(f'checked at {route[item_idx]}')
            # print(f'at index {item_idx} weight is {weight} and value is {value}')
            if current_weight + weight <= ttp_solver.capacity:
                current_weight += weight
                total_value += value
            else:
                print(f'capacity exceeded at {route[item_idx]}')

    # Calculate time based on current weight and given distance
    velocity = max(MIN_VELOCITY, MAX_VELOCITY - (current_weight * VELOCITY_REDUCTION_FACTOR))
    total_time = distance / velocity

    # Calculate rental cost
    # rental_cost = ttp_solver.renting_ratio * total_time
    
    # print(f'rental cost was {rental_cost} and profit was {total_value}')
    # Calculate total profit (value - rental cost)
    # total_profit = total_value - rental_cost
    total_profit = total_value

    # Apply weight penalty if capacity exceeded
    if current_weight > ttp_solver.capacity:
        weight_penalty = (current_weight - ttp_solver.capacity)  # Adjust penalty factor as needed
        total_profit -= weight_penalty

    return max(0, round(total_profit, 2)), current_weight