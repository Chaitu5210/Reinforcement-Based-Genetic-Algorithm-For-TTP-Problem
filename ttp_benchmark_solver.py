
import random
from typing import List,Tuple

def read_benchmark_file(filename: str):
    cities = []
    dimension = 0
    capacity = 0
    min_speed = 0.0
    max_speed = 0.0
    renting_ratio = 0.0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if 'DIMENSION' in line:
                dimension = int(line.split(':')[1].strip())
            elif 'CAPACITY OF KNAPSACK' in line:
                capacity = int(line.split(':')[1].strip())
            elif 'MIN SPEED' in line:
                min_speed = float(line.split(':')[1].strip())
            elif 'MAX SPEED' in line:
                max_speed = float(line.split(':')[1].strip())
            elif 'RENTING RATIO' in line:
                renting_ratio = float(line.split(':')[1].strip())
            elif line and line[0].isdigit():
                parts = line.split()
                if len(parts) == 3:
                    _, x, y = map(int, parts)
                    cities.append((x, y))
    
    return {
        'dimension': dimension,
        'capacity': capacity,
        'min_speed': min_speed,
        'max_speed': max_speed,
        'renting_ratio': renting_ratio,
        'cities': cities
    }



def generate_items(num_cities: int, num_items: int) -> List[Tuple[float, float]]:
    """Generate items for the TTP problem"""
    items = []
    items_per_city = num_items // num_cities
    
    for _ in range(num_items):
        weight = random.uniform(1, 100)
        value = random.uniform(10, 1000)
        items.append((weight, value))
    
    return items
    
  
