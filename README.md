# Farah-Parallel-and-Distributed-Computing

## DSAI 3202 - Assignment 1: Part 2: Navigating the City (Genetic Algorithm for Fleet Management)

### Overview
This project implements a **Genetic Algorithm (GA)** to optimize delivery routes for a fleet of vehicles in a city. The primary objective is to minimize the total distance traveled by all vehicles while ensuring that each delivery node is visited exactly once by any vehicle. The solution leverages **parallel computing** techniques using MPI4PY to distribute the workload across multiple machines, improving efficiency, especially for large datasets.

### Objectives
- Implement a **genetic algorithm** to optimize delivery routes
- Minimize the total distance traveled by all vehicles in a fleet
- Parallelize the genetic algorithm using **MPI4PY** for efficient computation
- Extend the solution to handle multiple vehicles and large-scale problems

### Key Concepts
- **Genetic Algorithms (GAs)**: An optimization technique inspired by natural selection, where solutions evolve over time using operators like **selection**, **crossover**, and **mutation**
- **Parallel Computing**: Distribution of computation tasks across multiple machines to speed up execution
- **Fleet Management**: Optimizing routes for a fleet of vehicles while minimizing total distance traveled

### Implementation Details

#### 1. Genetic Algorithm Functions

- **Calculate Fitness**: This function evaluates the total distance of a given route and returns the fitness score, with a penalty for infeasible routes.
- **Tournament Selection**: This function selects individuals for reproduction based on fitness through tournament-style selection, comparing a subset of individuals.
- **Order Crossover**: Combines genetic material from two parent solutions to create a new offspring route while preserving the order of the nodes.
- **Mutation**: Introduces random changes to a solution to maintain genetic diversity and prevent premature convergence.
- **Population Generation**: Creates an initial population of unique solutions by randomly generating routes.

#### 2. Sequential Implementation Explanation

The sequential implementation in `genetic_algorithm_trial.py` follows these steps:

1. Load the distance matrix from CSV
2. Initialize algorithm parameters (population size, mutation rate, etc.)
3. Generate an initial population of unique route solutions
4. For each generation:
   - Evaluate fitness of all routes
   - Check for stagnation and regenerate population if needed
   - Perform selection, crossover, and mutation operations
   - Replace worst individuals with new offspring
   - Ensure population uniqueness
5. Return the best solution found

#### 3. Parallel Implementation with MPI4PY

The parallelized version in `mpi4.py` distributes the genetic algorithm across multiple processes:

1. Each process generates and manages its own chunk of the population
2. Fitness evaluation is parallelized, with each process calculating fitness for its local population
3. Local best solutions are gathered and compared to find the global best
4. Migration of individuals between processes occurs periodically (every 5 generations)
5. Stagnation detection and population regeneration are coordinated across all processes

### Parts to be Distributed and Parallelized

For efficient parallelization, the following components were chosen:

1. **Population Management**: Each process manages a subset of the total population
2. **Fitness Evaluation**: This is the most computationally intensive part of the algorithm and benefits greatly from parallelization
3. **Selection Process**: Each process conducts tournament selection on its local population
4. **Migration**: Periodic exchange of individuals between processes introduces diversity

These choices maximize parallel efficiency while minimizing communication overhead between processes.

### Performance Metrics

#### Sequential Execution
- **Best Solution**: [0, 25, 20, 30, 29, 31, 19, 28, 11, 9, 24, 27, 3, 14, 10, 12, 18, 23, 7, 22, 5, 4, 13, 15, 2, 8, 17, 1, 6, 26, 21, 16]
- **Total Distance**: 1187.0
- **Execution Time**: 19.4297 seconds

#### Distributed/Parallelized Execution (4 processes)
- **Best Solution**: [0, 14, 24, 29, 6, 25, 2, 22, 27, 31, 7, 4, 23, 28, 30, 16, 12, 5, 8, 11, 10, 19, 20, 3, 17, 21, 26, 18, 15, 9, 1, 13]
- **Total Distance**: 1180.0
- **Execution Time**: 6.1924 seconds

This represents a **68.1% reduction in execution time** while also finding a slightly better solution (lower total distance).

### Enhancements

The following improvements were implemented:

1. **Population Migration**: Implemented a ring topology for migration where processes exchange individuals periodically
2. **Stagnation Detection**: Added global stagnation detection and population regeneration to prevent early convergence
3. **Adaptive Penalty**: In the large-scale version, an adaptive penalty is used instead of a fixed penalty for infeasible routes

After these enhancements, the algorithm shows:
- Better convergence to global optima
- More resilience to getting stuck in local optima
- Better handling of large-scale problems

### Large Scale Problem

The algorithm was successfully run on the extended city map with 100 nodes and 4000 routes. The parallelized version was able to handle this larger dataset efficiently, showing the scalability of the approach.

### How to Add More Cars

To extend the solution for multiple vehicles:

1. **Divide the City into Regions**: Split the city into logical regions, assigning each vehicle to a region.
2. **Vehicle Assignment**: Each vehicle starts and ends at the depot (node 0). Assign nodes to vehicles based on proximity or divide them evenly.
3. **Independent Optimization**: Optimize each vehicle's route independently using the same genetic algorithm approach.
4. **Balancing Workload**: Add constraints to ensure balanced workloads across vehicles.
5. **Global Optimization**: After local optimization, perform a global optimization step to minimize the total distance traveled by all vehicles.

Implementation approach:
- Modify the chromosome representation to include vehicle assignments
- Adjust the fitness function to evaluate multiple vehicle routes
- Implement specialized crossover and mutation operators that respect vehicle assignments

### Conclusion

This project demonstrates the effective use of genetic algorithms and parallel computing for solving fleet management optimization problems. The parallel implementation significantly reduces execution time while maintaining or improving solution quality. The approach is scalable to larger problems and can be extended to handle multiple vehicles.
