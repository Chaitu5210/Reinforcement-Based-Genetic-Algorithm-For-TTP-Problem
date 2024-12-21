
# Reinforcement-Based Genetic Algorithm for the Travelling Thief Problem (TTP)

This academic project focuses on developing a **Hybrid Evolutionary Algorithm** to solve the **Travelling Thief Problem (TTP)**. TTP is a challenging optimization problem that combines two classical problems: the Traveling Salesman Problem (TSP) and the Knapsack Problem (KP). The goal is to optimize travel routes and item selection by balancing distance and profit constraints.

Our approach uses **genetic operators** and **local search techniques** to achieve efficient and effective solutions. Contributions are welcome, and we look forward to seeing your input!

---

## Problem Overview

Given a set of **points X**, where **X-1** represent cities, each with the following attributes:

- **Profit**: The profit the thief can earn by collecting items from the city.
- **Weight**: The weight of items available in the city.
- **X, Y Coordinates**: Geographical position of the city.

And one point representing the starting position of the thief, the objective is to calculate the **maximum profit** achievable under specific conditions.

---

## Constraints

1. The thief operates with a **knapsack** of defined capacity.
2. The thief's **initial speed** is **100**.
3. The speed decreases as the weight of the knapsack increases, governed by the following formula:

### Speed Reduction Formula

```
Speed Reduction = (Current Knapsack Weight + Current Node Weight) / Knapsack Capacity) * 100
```

The challenge is to determine the **maximum profit** while considering the effects of knapsack weight on the thief's speed and the travel route optimization.

---

## Key Features

- **Hybrid Evolutionary Algorithm**:
  - Combines **Genetic Algorithms (GA)** with **Reinforcement Learning** to enhance performance.
  - Implements genetic operators such as **selection, crossover, and mutation**.
  - Includes a **local search mechanism** for fine-tuning solutions.

- **Multi-Objective Optimization**:
  - Balances the trade-off between maximizing profit and minimizing travel time.
  - Adapts dynamically to varying knapsack capacities and item weights.

- **Real-World Applications**:
  - Logistics and supply chain optimization.
  - Path planning in robotics.

---

## Input File Format

The algorithm accepts benchmark files containing:

- A list of cities with their respective attributes:
  - **City ID**
  - **X, Y Coordinates**
  - **Item Profit**
  - **Item Weight**

### Example
```
City 1: X=10, Y=20, Profit=15, Weight=5
City 2: X=30, Y=50, Profit=25, Weight=10
```

---

## How to Run the Code

To execute the code, use the following command:

```bash
python3 main.py --files a29.txt --population 200 --mutation 0.01 --generations 200
```

### Command-Line Arguments

- `--files`: Input benchmark file(s).
- `--population`: Population size for the genetic algorithm (default: 200).
- `--mutation`: Mutation rate for the genetic algorithm (default: 0.05).
- `--generations`: Number of generations to evolve (default: 2).

---

## Example Execution

```bash
python3 main.py --files a29.txt --population 200 --mutation 0.01 --generations 200
```

The above command runs the algorithm on the benchmark file `a29.txt` with:
- **Population size**: 200
- **Mutation rate**: 0.01
- **Generations**: 200

---

## Contributing

We welcome contributions to enhance this project! Here’s how you can help:

1. **Fork the repository** and create a feature branch.
2. Make your changes and submit a **pull request**.
3. Provide detailed documentation for any new features or enhancements.

---

## Contact

If you have any questions or feedback, feel free to reach out. Contributions and suggestions are highly appreciated!

Happy coding and solving!

---

### Acknowledgments

This project is a part of academic research on hybrid evolutionary algorithms. Special thanks to the contributors and reviewers for their valuable input and support.
