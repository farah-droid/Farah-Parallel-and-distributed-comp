import threading
import time

# Function to calculate the sum of a range of numbers
def thread_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def parallel_sum_threading(n, num_threads=4):
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

# Measure execution time
n = 10**6  # Large number
start_time = time.time()

total_sum_parallel_threading = parallel_sum_threading(n)

end_time = time.time()

execution_time_threading = end_time - start_time
speedup_threading = 0.011043 / execution_time_threading  # Sequential time = 0.011043

# Efficiency calculation
efficiency_threading = speedup_threading / 4  # 4 threads

print(f"Sum: {total_sum_parallel_threading}")
print(f"Execution Time (Threading): {execution_time_threading:.6f} seconds")
print(f"Speedup (Threading): {speedup_threading:.2f}")
print(f"Efficiency (Threading): {efficiency_threading:.4f}")
