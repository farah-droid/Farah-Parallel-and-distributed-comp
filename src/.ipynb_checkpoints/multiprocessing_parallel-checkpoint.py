# multiprocessing_parallel.py
import multiprocessing

# Function to calculate the sum of a range of numbers
def process_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def parallel_sum_multiprocessing(n, num_processes=6):  # Set to 6 processes
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
