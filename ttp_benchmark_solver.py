
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
            elif 'NUMBER OF ITEMS' in line:
                items = int(line.split(':')[1].strip())
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
        'items': items,
        'capacity': capacity,
        'min_speed': min_speed,
        'max_speed': max_speed,
        'renting_ratio': renting_ratio,
        'cities': cities
    }



def generate_items(filename: str) -> List[Tuple[int, float, float, int]]:
    items = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    in_items_section = False

    for line in lines:
        line = line.strip()
        if line.startswith('ITEMS SECTION'):
            in_items_section = True
            continue  # Skip the 'ITEMS SECTION' line itself

        if in_items_section:
            if not line:  # Exit if the section ends (empty line)
                break
            
            parts = line.split()
            if len(parts) == 3:
                profit = float(parts[1])
                weight = float(parts[2])
                items.append((profit, weight))
    
    return items