import sys
import os
sys.path.append(os.path.abspath('./src'))  # Add 'src' folder to Python path
from mpi4py import MPI
import numpy as np
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

# Import distance matrix and required functions
try:
    from src.genetic_algorithm_trial import distance_matrix
except ImportError:
    # Fallback if import fails
    distance_matrix = pd.read_csv('data/city_distances.csv').to_numpy()

num_nodes = distance_matrix.shape[0]

from src.genetic_algorithms_functions import (
    calculate_fitness,
    generate_unique_population,
    select_in_tournament,
    order_crossover,
    mutate,
)

# Set up MPI environment
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Configuration parameters
POPULATION_SIZE = 10000  # Increased for better exploration
NUM_GENERATIONS = 200
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 3
ELITISM_RATE = 0.05  # Keep top 5% of individuals
STAGNATION_LIMIT = 5
MIGRATION_INTERVAL = 10  # How often to share individuals between processes

# Track performance metrics
fitness_history = []
best_route_history = []
time_per_generation = []

def parallel_fitness_evaluation(population, distance_matrix):
    """Distribute fitness evaluation across processes"""
    # Determine local chunk size for each process
    chunk_size = len(population) // size
    start = rank * chunk_size
    end = start + chunk_size
    
    # Last process takes any remaining individuals
    if rank == size - 1:
        end = len(population)
    
    # Calculate fitness for local chunk
    local_population = population[start:end]
    local_fitness = np.array([calculate_fitness(ind, distance_matrix) for ind in local_population])
    
    # Gather results from all processes
    local_counts = np.array([len(local_fitness)], dtype=np.int)
    counts = comm.allgather(local_counts[0])
    
    # Prepare receive buffer for gathering results
    if rank == 0:
        all_fitness = np.empty(sum(counts), dtype=np.float64)
    else:
        all_fitness = None
    
    # Use Gatherv to handle variable chunk sizes
    displacements = np.array([sum(counts[:i]) for i in range(len(counts))])
    comm.Gatherv(sendbuf=local_fitness, recvbuf=[all_fitness, counts, displacements, MPI.DOUBLE], root=0)
    
    # Broadcast complete results to all processes
    all_fitness = comm.bcast(all_fitness, root=0)
    
    return all_fitness

def local_search(route, distance_matrix, max_iterations=10):
    """Improve a route using 2-opt local search"""
    best_route = route.copy()
    best_fitness = calculate_fitness(route, distance_matrix)
    improved = True
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        # Try swapping edges (2-opt)
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                # Create new route with 2-opt swap
                new_route = route.copy()
                new_route[i:j+1] = reversed(new_route[i:j+1])
                
                # Check if improvement
                new_fitness = calculate_fitness(new_route, distance_matrix)
                if new_fitness < best_fitness:
                    best_route = new_route.copy()
                    best_fitness = new_fitness
                    improved = True
                    break
            
            if improved:
                break
        
        if improved:
            route = best_route.copy()
    
    return best_route

def migrate_individuals(population, fitness):
    """Share best individuals between processes using a ring topology"""
    # Number of individuals to migrate
    num_migrants = max(1, int(0.05 * len(population) // size))
    
    if rank == 0:
        print(f"Migration: Exchanging {num_migrants} individuals between processes")
    
    # Select best individuals to migrate
    indices = np.argsort(fitness)
    migrants = [population[i] for i in indices[:num_migrants]]
    
    # Determine source and destination in ring topology
    dest = (rank + 1) % size
    source = (rank - 1) % size
    
    # Exchange migrants
    received_migrants = comm.sendrecv(migrants, dest=dest, source=source)
    
    # Replace worst individuals with received migrants
    worst_indices = indices[-num_migrants:]
    for i, idx in enumerate(worst_indices):
        population[idx] = received_migrants[i]
    
    return population

def diversify_population(population, best_individual, population_size, num_nodes):
    """Regenerate population while preserving the best individual"""
    # Keep the best individual and generate new random individuals
    new_population = [best_individual]
    new_individuals = generate_unique_population(population_size - 1, num_nodes)
    new_population.extend(new_individuals)
    
    return new_population

def run_parallel_ga():
    """Main function for running the parallel genetic algorithm"""
    # Initialize population
    if rank == 0:
        print(f"Starting Parallel GA with {size} processes")
        print(f"Population size: {POPULATION_SIZE}, Generations: {NUM_GENERATIONS}")
        print(f"Problem size: {num_nodes} cities")
        
        # Generate initial population
        population = generate_unique_population(POPULATION_SIZE, num_nodes)
        start_time = time.time()
    else:
        population = None
        start_time = time.time()
    
    # Broadcast initial population to all processes
    population = comm.bcast(population, root=0)
    
    # Track best solution and stagnation
    global_best_fitness = float('-inf')
    global_best_individual = None
    stagnation_counter = 0
    
    # Main GA loop
    for gen in range(NUM_GENERATIONS):
        gen_start_time = time.time()
        
        # Evaluate fitness in parallel
        fitness = parallel_fitness_evaluation(population, distance_matrix)
        
        # Find best individual
        best_idx = np.argmin(fitness)
        current_best_fitness = fitness[best_idx]
        current_best_individual = population[best_idx]
        
        # Track progress
        if rank == 0:
            fitness_history.append(-current_best_fitness)  # Store as positive distance
            best_route_history.append(current_best_individual.copy())
            
            print(f"Generation {gen}: Best fitness = {current_best_fitness}")
            
            # Track time per generation
            gen_time = time.time() - gen_start_time
            time_per_generation.append(gen_time)
        
        # Check for improvement
        if current_best_fitness < global_best_fitness or global_best_individual is None:
            global_best_fitness = current_best_fitness
            global_best_individual = current_best_individual.copy()
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        # Migration between processes
        if gen % MIGRATION_INTERVAL == 0 and gen > 0:
            population = migrate_individuals(population, fitness)
        
        # Check for stagnation
        if stagnation_counter >= STAGNATION_LIMIT:
            if rank == 0:
                print(f"Generation {gen}: Stagnation detected. Diversifying population.")
            
            # Diversify population while keeping best individual
            population = diversify_population(population, global_best_individual, POPULATION_SIZE, num_nodes)
            stagnation_counter = 0
            
            # Synchronize population across all processes
            population = comm.bcast(population, root=0)
            continue
        
        # Selection and reproduction
        if rank == 0:
            # Calculate number of elites
            num_elites = int(ELITISM_RATE * POPULATION_SIZE)
            
            # Select elites
            elite_indices = np.argsort(fitness)[:num_elites]
            elites = [population[i] for i in elite_indices]
            
            # Tournament selection
            selected = select_in_tournament(
                population, fitness,
                number_tournaments=POPULATION_SIZE - num_elites,
                tournament_size=TOURNAMENT_SIZE
            )
            
            # Create offspring through crossover and mutation
            offspring = []
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    p1, p2 = selected[i], selected[i + 1]
                    
                    # Perform crossover
                    c1 = [0] + order_crossover(p1[1:], p2[1:])
                    c2 = [0] + order_crossover(p2[1:], p1[1:])
                    
                    # Apply mutation
                    c1 = mutate(c1, MUTATION_RATE)
                    c2 = mutate(c2, MUTATION_RATE)
                    
                    offspring.extend([c1, c2])
            
            # Apply local search to a few individuals (5%)
            num_local_search = max(1, int(0.05 * len(offspring)))
            for i in range(num_local_search):
                idx = random.randint(0, len(offspring) - 1)
                offspring[idx] = local_search(offspring[idx], distance_matrix)
            
            # Combine elites and offspring
            new_population = elites + offspring
            
            # Ensure we have exactly POPULATION_SIZE individuals
            if len(new_population) > POPULATION_SIZE:
                new_population = new_population[:POPULATION_SIZE]
            elif len(new_population) < POPULATION_SIZE:
                # Add random individuals if needed
                additional = generate_unique_population(POPULATION_SIZE - len(new_population), num_nodes)
                new_population.extend(additional)
            
            population = new_population
        
        # Broadcast new population to all processes
        population = comm.bcast(population, root=0)
    
    # Final evaluation
    final_fitness = parallel_fitness_evaluation(population, distance_matrix)
    final_best_idx = np.argmin(final_fitness)
    final_best_fitness = final_fitness[final_best_idx]
    final_best_individual = population[final_best_idx]
    
    # Print final results from rank 0
    if rank == 0:
        total_time = time.time() - start_time
        
        print("\n==== Final Results ====")
        print(f"Best Solution: {final_best_individual}")
        print(f"Total Distance: {-final_best_fitness}")
        print(f"Total Runtime: {total_time:.2f} seconds")
        print(f"Average time per generation: {np.mean(time_per_generation):.4f} seconds")
        
        
        return final_best_individual, -final_best_fitness, total_time


# Execute the main function if this script is run directly
if __name__ == "__main__":
    run_parallel_ga()