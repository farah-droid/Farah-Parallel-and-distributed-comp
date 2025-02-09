import multiprocessing
import time

# Function to calculate the sum of a range of numbers
def process_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def parallel_sum_multiprocessing(n, num_processes=4):
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

# Measure execution time
n = 10**6  # Large number
start_time = time.time()

total_sum_parallel_multiprocessing = parallel_sum_multiprocessing(n)

end_time = time.time()

execution_time_multiprocessing = end_time - start_time
speedup_multiprocessing = 0.011043 / execution_time_multiprocessing  # Sequential time = 0.011043

# Efficiency calculation
efficiency_multiprocessing = speedup_multiprocessing / 4  # 4 processes

print(f"Sum: {total_sum_parallel_multiprocessing}")
print(f"Execution Time (Multiprocessing): {execution_time_multiprocessing:.6f} seconds")
print(f"Speedup (Multiprocessing): {speedup_multiprocessing:.2f}")
print(f"Efficiency (Multiprocessing): {efficiency_multiprocessing:.4f}")
