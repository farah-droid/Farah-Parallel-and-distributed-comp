import multiprocessing
import threading
import time

# Function for multiprocessing to calculate the sum of a range of numbers
def process_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def parallel_sum_multiprocessing(n, num_processes=6):  # Changed to 6 processes
    step = n // num_processes
    processes = []
    result = multiprocessing.Array('i', num_processes)  # Shared memory array for storing results
    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step if i < num_processes - 1 else n + 1
        process = multiprocessing.Process(target=process_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  # Ensure all processes complete

    return sum(result)

# Function for threading to calculate the sum of a range of numbers
def thread_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def parallel_sum_threading(n, num_threads=6):  # Changed to 6 threads
    step = n // num_threads
    threads = []
    result = [0] * num_threads  # Store results from each thread
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step if i < num_threads - 1 else n + 1
        thread = threading.Thread(target=thread_sum, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Ensure all threads complete

    return sum(result)

def main():
    n = 10**6  # Large number
    
    # Run multiprocessing
    start_time = time.time()
    total_sum_parallel_multiprocessing = parallel_sum_multiprocessing(n)
    end_time = time.time()
    
    execution_time_multiprocessing = end_time - start_time
    speedup_multiprocessing = 0.011043 / execution_time_multiprocessing  # Sequential time = 0.011043
    efficiency_multiprocessing = speedup_multiprocessing / 6  # 6 processes
    
    print("\nMultiprocessing Results:")
    print(f"Sum: {total_sum_parallel_multiprocessing}")
    print(f"Execution Time (Multiprocessing): {execution_time_multiprocessing:.6f} seconds")
    print(f"Speedup (Multiprocessing): {speedup_multiprocessing:.2f}")
    print(f"Efficiency (Multiprocessing): {efficiency_multiprocessing:.4f}")
    
    # Run threading
    start_time = time.time()
    total_sum_parallel_threading = parallel_sum_threading(n)
    end_time = time.time()
    
    execution_time_threading = end_time - start_time
    speedup_threading = 0.011043 / execution_time_threading  # Sequential time = 0.011043
    efficiency_threading = speedup_threading / 6  # 6 threads
    
    print("\nThreading Results:")
    print(f"Sum: {total_sum_parallel_threading}")
    print(f"Execution Time (Threading): {execution_time_threading:.6f} seconds")
    print(f"Speedup (Threading): {speedup_threading:.2f}")
    print(f"Efficiency (Threading): {efficiency_threading:.4f}")

if __name__ == "__main__":
    main()
