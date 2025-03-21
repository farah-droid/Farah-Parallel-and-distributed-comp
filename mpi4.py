import sys
import os
sys.path.append(os.path.abspath('./src'))  # Add 'src' folder to Python path

from mpi4py import MPI
import numpy as np
import pandas as pd
import time
import random

from src.genetic_algorithm_trial import distance_matrix  # Import the distance matrix from the trial file
from src.genetic_algorithms_functions import (
    calculate_fitness,
    generate_unique_population,
    select_in_tournament,
    order_crossover,
    mutate,
)

def main():
    # Start timing
    start_time = time.time()
    
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Load the distance matrix
    distance_matrix = pd.read_csv('data/city_distances.csv').to_numpy()
    num_nodes = distance_matrix.shape[0]
    
    # Parameters
    population_size = 10000
    chunk_size = population_size // size  # Divide population evenly among processes
    num_tournaments = 4
    mutation_rate = 0.1
    num_generations = 200
    stagnation_limit = 5
    
    # Set random seed for reproducibility, different for each process
    np.random.seed(42 + rank)
    
    # Each process generates its own chunk of the population
    local_population = generate_unique_population(chunk_size, num_nodes)
    
    # Initialize tracking variables
    best_fitness = float('-inf')
    stagnation_counter = 0
    best_route = None
    
    # Main GA loop
    for generation in range(num_generations):
        # Evaluate fitness (negative distance since we want to minimize distance)
        local_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in local_population])
        
        # Find local best solution (highest fitness = shortest distance)
        local_best_idx = np.argmax(local_fitness_values)
        local_best_fitness = local_fitness_values[local_best_idx]
        local_best_route = [int(node) for node in local_population[local_best_idx]]
        
        # Gather all local best solutions to rank 0
        all_best_fitness = comm.gather(local_best_fitness, root=0)
        all_best_routes = comm.gather(local_best_route, root=0)
        
        # Process 0 finds the global best
        if rank == 0:
            global_best_idx = np.argmax(all_best_fitness)
            global_best_fitness = all_best_fitness[global_best_idx]
            global_best_route = all_best_routes[global_best_idx]
            
            # Check for stagnation
            if global_best_fitness > best_fitness:
                best_fitness = global_best_fitness
                best_route = global_best_route
                stagnation_counter = 0
                # Print with the negative to show the actual distance
                print(f"Generation {generation}: Best distance = {-global_best_fitness}")
            else:
                stagnation_counter += 1
        
        # Broadcast stagnation counter and global best route to all processes
        stagnation_counter = comm.bcast(stagnation_counter, root=0)
        global_best_route = comm.bcast(global_best_route if rank == 0 else None, root=0)
        
        # Check for stagnation
        if stagnation_counter >= stagnation_limit:
            # Regenerate population, keeping the global best
            local_population = generate_unique_population(chunk_size - 1, num_nodes)
            local_population.append(global_best_route)
            stagnation_counter = 0
            if rank == 0:
                print(f"Regenerating population at generation {generation} due to stagnation")
            continue
        
        # Selection, crossover, and mutation
        selected = select_in_tournament(local_population, local_fitness_values)
        
        # Create offspring through crossover
        offspring = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):  # Ensure we have pairs
                parent1, parent2 = selected[i], selected[i + 1]
                child = [0] + order_crossover(parent1[1:], parent2[1:])
                offspring.append(child)
        
        # Apply mutation
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
        
        # Replace worst individuals with new offspring
        worst_indices = np.argsort(local_fitness_values)[:len(mutated_offspring)]
        for i, idx in enumerate(worst_indices):
            local_population[idx] = mutated_offspring[i]
        
        # Exchange some individuals between processes (migration)
        if size > 1 and generation % 5 == 0:  # Migrate every 5 generations
            # Simple ring topology: send to rank+1, receive from rank-1
            dest = (rank + 1) % size
            source = (rank - 1) % size
            
            # Select a random individual to send
            send_idx = np.random.randint(len(local_population))
            send_data = [int(node) for node in local_population[send_idx]]
            
            # Send and receive
            recv_data = comm.sendrecv(send_data, dest=dest, source=source)
            
            # Replace a random individual with the received one
            replace_idx = np.random.randint(len(local_population))
            local_population[replace_idx] = recv_data
    
    # Final gathering of results - only for MPI process 0
    local_fitness = [calculate_fitness(route, distance_matrix) for route in local_population]
    local_routes = [[int(node) for node in route] for route in local_population]
    
    all_fitness = comm.gather(local_fitness, root=0)
    all_routes = comm.gather(local_routes, root=0)
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Find and print the global best solution - only for MPI process 0
    if rank == 0:
        # Flatten lists
        flat_fitness = []
        flat_routes = []
        for fitness_list, routes_list in zip(all_fitness, all_routes):
            flat_fitness.extend(fitness_list)
            flat_routes.extend(routes_list)
        
        global_best_idx = np.argmax(flat_fitness)
        global_best_route = flat_routes[global_best_idx]
        global_best_fitness = flat_fitness[global_best_idx]
        
        # Verify the route is valid before printing
        actual_distance = -calculate_fitness(global_best_route, distance_matrix)
        
        print("\nFinal Results (MPI Distributed Algorithm):")
        print("Best Route:", global_best_route)
        print("Total Distance:", actual_distance)
        print(f"Number of processes used: {size}")
        print(f"Total execution time: {execution_time:.4f} seconds")

if __name__ == "__main__":
    main()