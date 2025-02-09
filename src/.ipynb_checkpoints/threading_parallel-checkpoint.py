# threading_parallel.py
import threading

# Function to calculate the sum of a range of numbers
def thread_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def parallel_sum_threading(n, num_threads=6):  # Set to 6 threads
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
