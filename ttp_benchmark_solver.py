# Description: This file contains the functions to read the benchmark files and generate the items for the TTP problem.
'''File Contains:
    1. read_benchmark_file function: This function is used to read the benchmark file and extract the required data.
    2. generate_items function: This function is used to generate the items from the given file.'''

# Importing required libraries
import random
from typing import List,Tuple

# read_benchmark_file function is used to read the benchmark file and extract the required data
def read_benchmark_file(filename: str):
    cities = []
    dimension = 0
    capacity = 0
    min_speed = 0.0
    max_speed = 0.0
    renting_ratio = 0.0
    
    # Read the file line by line
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
                    _, x, y = map(float, parts)
                    cities.append((x, y))
    
    # Return the extracted data
    return {
        'dimension': dimension,
        'items': items,
        'capacity': capacity,
        'min_speed': min_speed,
        'max_speed': max_speed,
        'renting_ratio': renting_ratio,
        'cities': cities
    }


# generate_items function is used to generate the items from the given file
def generate_items(filename: str) -> List[Tuple[int, float, float, int]]:
    items = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    in_items_section = False

    for line in lines:
        line = line.strip()
        if line.startswith('ITEMS SECTION'):
            in_items_section = True
            continue 

        if in_items_section:
            if not line:
                break
            
            parts = line.split()
            if len(parts) == 4:
                profit = float(parts[1])
                weight = float(parts[2])
                items.append((profit, weight))
    
    return items