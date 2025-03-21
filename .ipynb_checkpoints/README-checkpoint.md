# Farah-Parallel-and-distributed-comp

## DSAI 3202 - Assignment 1: Part 2: Navigating the City (Genetic Algorithm for Fleet Management)

### Overview
This project utilizes a **Genetic Algorithm (GA)** to optimize delivery routes for a fleet of vehicles in a city. The primary objective is to minimize the total distance traveled by all vehicles while ensuring that each delivery node is visited exactly once by any vehicle. The solution leverages **parallel computing** techniques to distribute the workload across multiple machines, improving efficiency, especially for large datasets.

The project includes the implementation of a genetic algorithm with **MPI4PY** for parallelization and distributed computing. The problem was first solved sequentially and then parallelized to improve performance. The solution is extended to handle multiple vehicles, and the algorithm is tested on both small and large city maps.

### Objectives
- Implement a **genetic algorithm** to optimize delivery routes.
- Minimize the total distance traveled by all vehicles in a fleet while ensuring each node is visited once.
- Parallelize the genetic algorithm using **MPI4PY** for efficient computation across multiple machines.
- Extend the solution to handle multiple vehicles and large-scale problems.

### Key Concepts
- **Genetic Algorithms (GAs)**: An optimization technique inspired by natural selection, where a population of solutions evolves over time using operators such as **selection**, **crossover**, and **mutation**.
- **Parallel Computing**: Distribution of the computation tasks (fitness evaluation, selection..) across multiple machines to speed up execution.
- **Fleet Management**: Optimizing the routes for a fleet of vehicles, ensuring each vehicle visits a subset of delivery nodes while minimizing the total distance traveled.

### Steps Taken
#### 1. Genetic Algorithm Implementation
The genetic algorithm consists of the following components:
- **Fitness Function**: This function calculates the total distance of a proposed route. If any route is infeasible (a node is unreachable), a large negative penalty is returned.
- **Selection**: A **tournament selection** method was used, where individuals compete in tournaments, and the winner is selected for crossover.
- **Crossover**: The genetic material from two parent solutions is combined to create offspring. This was implemented with a uniform crossover method.
- **Mutation**: Random changes were introduced to the offspring’s genetic makeup to maintain diversity and prevent premature convergence.

#### 2. Parallelization
The genetic algorithm was initially implemented sequentially and then parallelized using **MPI4PY**:
- **Fitness Evaluation**: The fitness calculation for each individual in the population was parallelized, enabling simultaneous evaluation of multiple individuals across different machines.
- **Selection**: Tournament selection was also parallelized to improve performance.

The parallelized version showed a significant improvement in execution time, especially when applied to larger datasets.

#### 3. Large-Scale Problem
The problem was tested on both a **small city map** and a **large city map**. The **`city_distances_extended.csv`** file represents the extended city layout, containing 100 nodes and 4000 routes. The parallelized algorithm successfully handled the larger dataset within a feasible time frame better than the small city.

For example, in the small city, the best route had a total distance of -2115.0, while the larger city map resulted in a total distance of -2697.0 in the final generation.

### Results:
### Execution Times
#### Sequential Execution Time:
- **Best Solution**: [0, np.int64(10), np.int64(7), np.int64(31), np.int64(23), np.int64(12), np.int64(9), np.int64(2), np.int64(21), np.int64(20), np.int64(29), np.int64(26), np.int64(24), np.int64(4), np.int64(3), np.int64(5), np.int64(16), np.int64(28), np.int64(18), np.int64(27), np.int64(8), np.int64(15), np.int64(19), np.int64(1), np.int64(11), np.int64(6), np.int64(22), np.int64(30), np.int64(25), np.int64(17), np.int64(13), np.int64(14)]
- **Total Distance**: -2115.0
- **Execution Time**: 7.9412 seconds&#8203;:contentReference[oaicite:0]{index=0}

#### Distributed/Parallelized Execution Time:
- **Best Solution**: [np.int64(30), np.int64(22), np.int64(14), np.int64(6), np.int64(27), np.int64(25), np.int64(28), np.int64(11), np.int64(7), np.int64(8), np.int64(18), np.int64(4), np.int64(24), np.int64(1), np.int64(20), np.int64(21), np.int64(2), np.int64(16), np.int64(15), np.int64(26), np.int64(23), np.int64(12), np.int64(9), np.int64(5), np.int64(3), 0, np.int64(17), np.int64(29), np.int64(19), np.int64(10), np.int64(13), np.int64(31)]
- **Total Distance**: 2726.0
- **Execution Time**: 0.82 seconds&#8203;:contentReference[oaicite:1]{index=1}

### Performance Metrics
The execution time and fitness of the algorithm were measured:
- **Sequential Execution**: The genetic algorithm ran for several generations to find the optimal route. For example, in Generation 0, the best fitness was -1796.0, and after several generations, the best fitness reached -2115.0.
- **Parallel Execution**: Using MPI4PY, the performance improved with a faster execution time due to distributed fitness evaluation and selection processes. The parallelized version showed a substantial reduction in computation time when applied to the extended dataset.

### How to Add More Cars
1. **Divide the City into Regions**: Split the city into regions, assigning each vehicle to a region. Each vehicle will optimize its route within its assigned region.
2. **Vehicle Assignment**: Each vehicle will start and end its route at the depot. Assign nodes to vehicles either based on proximity or evenly divided across vehicles.
3. **Independent Optimization**: Optimize each vehicle's route independently. The fitness function will evaluate each vehicle's route within its region, using crossover and mutation on individual vehicle populations.
4. **Minimizing Total Distance**: After optimizing each vehicle’s route, minimize the total distance by adjusting routes across vehicles to ensure the combined distance is as low as possible.
5. 
### Conclusion
This project successfully implemented and parallelized a genetic algorithm to solve the fleet management problem, optimizing delivery routes in a city. The algorithm was extended to handle larger problems and multiple vehicles, with performance improvements achieved through parallelization. This solution demonstrates the power of genetic algorithms and parallel computing for solving optimization problems efficiently.



