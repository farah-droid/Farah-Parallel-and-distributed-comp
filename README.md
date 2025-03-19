# DSAI 3202 - Assignment 1 - Part 1/2: Multiprocessing and Process Synchronization

## Overview

This assignment focuses on utilizing Python's multiprocessing capabilities and process synchronization with semaphores. The tasks include:
1. Performing square calculations using different multiprocessing methods.
2. Simulating a database connection pool using semaphores to manage access to limited resources.

The following sections describe the implementation and results for both parts of the assignment.

---

## Part 1: Square Program with Multiprocessing

### Task Description
In this part of the assignment, we implemented a program that calculates the square of numbers using various approaches. The main goal was to explore different ways to parallelize the square calculation process using Python’s `multiprocessing` module and compare the performance of these approaches.

The following methods were implemented:
- **Sequential for loop**: A simple loop iterates through the list and computes the square for each number, one after another.
- **Multiprocessing (one process per number)**: Each number is processed by a separate process. This method is inefficient due to the overhead of creating individual processes for each task.
- **Multiprocessing Pool with map()**: This method uses a pool of worker processes to calculate the squares in parallel, distributing the tasks using the `map()` method. This approach is more efficient as it reuses processes.
- **Multiprocessing Pool with apply()**: Similar to the `map()` method but using the `apply()` method to process each number synchronously. This method processes each task one by one but in parallel using multiple processes.
- **ProcessPoolExecutor**: A higher-level API from `concurrent.futures` to manage processes. It allows for a more Pythonic and efficient way of parallelizing tasks.

### Performance Results

The program was tested with two different input sizes:
1. **10^6 numbers**: A list containing one million random integers.
2. **10^7 numbers**: A list containing ten million random integers.

The performance of each method was measured by recording the time taken to process the entire list of numbers. The sequential method was the slowest, as it processes each number one by one. The methods using multiprocessing pools (`map()` and `apply()`) significantly improved performance by parallelizing the work across multiple processes. The **ProcessPoolExecutor** provided the best performance in terms of speed for both small and large datasets, offering an efficient way to manage multiple worker processes.

#### Conclusions

- **Multiprocessing significantly improves performance**, especially with larger datasets. The pooling methods (`map()` and `apply()`) were more efficient than creating individual processes for each task.
- **Asynchronous execution** using `apply_async()` provided a slight performance improvement by allowing tasks to start processing without waiting for other tasks to complete.
- The **ProcessPoolExecutor** provided the most efficient approach, handling both synchronous and asynchronous execution efficiently.

---

## Part 2: Process Synchronization with Semaphores

### Task Description
In this part, we simulated a database connection pool using semaphores to control access to a limited number of resources. The task aimed to explore how semaphores can be used to synchronize processes and ensure that no more than a fixed number of processes can access a shared resource at the same time.

### Implementation
We implemented a **`ConnectionPool`** class to simulate a pool of database connections. The class uses a **semaphore** to manage the number of concurrent connections. The `get_connection()` method acquires a connection, and the `release_connection()` method releases the connection back to the pool.

A function **`access_database()`** simulates a process that acquires a connection, performs work (simulated by a sleep), and then releases the connection back to the pool.

We used multiple processes to simulate concurrent database operations. The semaphore ensured that only a limited number of processes could access the pool at any given time, effectively controlling access to the shared resource.

### Observations

1. **What happens if more processes try to access the pool than there are available connections?**
   - If more processes try to access the pool than there are available connections, they will be blocked by the semaphore. The semaphore ensures that the excess processes wait until a connection is released by another process, thereby controlling access and preventing more than the allowed number of processes from using the shared resource at once.

2. **How does the semaphore prevent race conditions and ensure safe access to the connections?**
   - The **semaphore** ensures that only a limited number of processes can access the pool at a time. It prevents **race conditions** by controlling access to the shared resource (database connection pool) and ensuring that processes acquire a connection only if there is one available. If all connections are in use, the semaphore blocks any additional processes from proceeding until a connection is released. This guarantees that no more than the allowed number of processes can access the pool concurrently, preventing any potential resource conflicts.

### Results
When more processes tried to access the connection pool than the available connections, the semaphore blocked the extra processes and ensured that they could only proceed once a connection was released. This behavior allowed for safe access to shared resources without overloading the connection pool.

---

## Conclusion

### Key Observations

1. **Multiprocessing**: Using multiprocessing helps achieve better performance for CPU-bound tasks by distributing the workload across multiple processes. Pools are more efficient than creating individual processes for each task.
2. **Semaphore Synchronization**: The semaphore is an effective tool for managing access to limited resources, ensuring that no more than the allowed number of processes can access shared resources at any given time.

### Recommendations

- Use multiprocessing pools when you need to parallelize tasks to avoid the overhead of creating too many processes.
- Employ semaphores when dealing with shared resources to ensure safe access in concurrent environments.


lsof -i :6379
---
