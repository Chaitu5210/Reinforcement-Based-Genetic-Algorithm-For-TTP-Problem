from typing import List, Tuple
from ttp_solver import TTPSolver
def calculate_fitness(solution: Tuple[List[int], List[int]], ttp_solver: 'TTPSolver') -> float:
    route, picking_plan = solution
    total_value = 0
    current_weight = 0
    total_time = 0
    
 
    base_fitness = 1000000
    
  
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        
   
        for item_idx in range(len(picking_plan)):
            if picking_plan[item_idx] == 1:
                weight, value = ttp_solver.items[item_idx]
                if current_weight + weight <= ttp_solver.capacity:
                    current_weight += weight
                    total_value += value * 100  # Scale up values
                
        distance = ttp_solver.calculate_distance(ttp_solver.cities[current_city], 
                                              ttp_solver.cities[next_city])
        speed = ttp_solver.calculate_speed(current_weight)
        time = distance / speed
        total_time += time
    
    # Penalize but don't completely invalidate overweight solutions
    if current_weight > ttp_solver.capacity:
        penalty = (current_weight - ttp_solver.capacity) * 1000
        return base_fitness - penalty
    
  
    objective = base_fitness + (total_value * 10) - (ttp_solver.renting_ratio * total_time * 5)
    return max(100, objective)  # Ensure meaningful minimum value