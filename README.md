
# Reinforcement-Based Genetic Algorithm for the Travelling Thief Problem (TTP)

This academic project focuses on developing a **Hybrid Evolutionary Algorithm** to solve the **Travelling Thief Problem (TTP)**. TTP is a challenging optimization problem that combines two classical problems: the Traveling Salesman Problem (TSP) and the Knapsack Problem (KP). The goal is to optimize travel routes and item selection by balancing distance and profit constraints.

Our approach uses **genetic algorithm** and **reinforcement learning** to achieve efficient and effective solutions. Contributions are welcome, and we look forward to seeing your input!

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

## Fitness Function

The fitness function evaluates a solution for the Traveling Thief Problem (TTP) by maximizing profit while minimizing penalties and travel costs. It combines the value of collected items and the cost of traveling time and weight constraints.

---

#### **Inputs**
- **`route`**: List of cities to visit in sequence.
- **`picking_plan`**: Binary list indicating whether an item is picked (`1`) or not (`0`).

---

#### **Constants**
- **`MAX_VELOCITY`** and **`MIN_VELOCITY`**: Determine the thief's speed, which decreases with increased weight.
- **`VELOCITY_REDUCTION_FACTOR`**: Constant that reduces velocity based on the current weight.

---

#### **Process**
1. **For each segment of the route**:
   - Calculate the total weight and value of the items picked.
   - Update the thief's velocity based on the current weight.
   - Calculate the time taken for the segment and update the total time.
2. **Calculate the total profit**:
   - `Total Profit = (Item Values Collected * Scaling Factor) - Rental Cost`
3. **Penalize solutions exceeding the weight capacity**:
   - `Weight Penalty = (Overload Weight) * Penalty Constant`

---

#### **Output**
- The fitness score is computed as:  
  `Fitness = Base Fitness + Total Profit - Weight Penalty (if applicable)`
- A **minimum value of 100** is enforced to ensure the fitness score remains meaningful.

---

#### **Key Features**
- Encourages solutions that collect high-value items while respecting weight constraints.
- Penalizes excessive weight and rewards efficient routes.
- Scales up profits to highlight significant differences between solutions.

---

#### **Return Value**
- The fitness score is a **floating-point number** representing the quality of the solution.
- **Higher fitness** indicates better solutions.

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

Install the requirements using the following command:

```bash
pip install -r requirements.txt
```

To execute the code, use the following command:

```bash
python3 main.py --files DATASET/eil51_n50_bounded-strongly-corr_01.ttp --population 200 --mutation 0.01 --generations 2000 --itrations 1
```

### Command-Line Arguments

- `--files`: Input benchmark file(s).
- `--population`: Population size for the genetic algorithm (default: 200).
- `--mutation`: Mutation rate for the genetic algorithm (default: 0.05).
- `--generations`: Number of generations to evolve (default: 2).

---

## Example Execution

```bash
python3 main.py --files DATASET/eil51_n50_bounded-strongly-corr_01.ttp --population 200 --mutation 0.01 --generations 2000 --itrations 1
```

The above command runs the algorithm on the benchmark file `eil51_n50_bounded-strongly-corr_01.ttp` with default values:
- **Population size**: 200
- **Mutation rate**: 0.05
- **Generations**: 2000
- **itrations**: 1

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
