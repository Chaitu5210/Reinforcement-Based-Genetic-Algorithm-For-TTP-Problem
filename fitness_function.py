from typing import List, Tuple
from ttp_solver import TTPSolver

def calculate_fitness(solution: Tuple[List[int], List[int]], ttp_solver: 'TTPSolver') -> float:
    route, picking_plan = solution
    total_value = 0
    current_weight = 0
    total_time = 0
    
    # Base fitness value
    base_fitness = 1000000
    
    # Constants for velocity calculation
    MAX_VELOCITY = 1.0
    MIN_VELOCITY = 0.1
    VELOCITY_REDUCTION_FACTOR = 0.001  # How much each item's weight reduces velocity
    
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        
        # Calculate item value and weight for current city
        city_value = 0
        for item_idx in range(len(picking_plan)):
            if picking_plan[item_idx] == 1:
                weight, value = ttp_solver.items[item_idx]
                if current_weight + weight <= ttp_solver.capacity:
                    current_weight += weight
                    city_value += value
                    total_value += value
        
        # Calculate velocity based on current weight
        # Velocity decreases as weight increases
        velocity = max(MIN_VELOCITY, 
                      MAX_VELOCITY - (current_weight * VELOCITY_REDUCTION_FACTOR))
        
        # Calculate distance and time for this segment
        distance = ttp_solver.calculate_distance(ttp_solver.cities[current_city], 
                                              ttp_solver.cities[next_city])
        time = distance / velocity
        total_time += time
    
    # Calculate rental cost based on total time
    rental_cost = ttp_solver.renting_ratio * total_time
    
    # Calculate total profit (value - rent)
    total_profit = (total_value * 100) - rental_cost  # Scale up values
    
    # Apply weight penalty if over capacity
    if current_weight > ttp_solver.capacity:
        weight_penalty = (current_weight - ttp_solver.capacity) * 1000
        return base_fitness - weight_penalty
    
    # Final fitness calculation combining base fitness and profit
    objective = base_fitness + total_profit
    
    return max(100, objective)  # Ensure meaningful minimum value
