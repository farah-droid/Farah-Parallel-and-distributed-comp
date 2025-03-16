import time
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# Function to compute the square of a number
def square(n):
    """
    Square a given number.

    Args:
    n (int): The number to square.

    Returns:
    int: The square of the input number.
    """
    return n * n

# Function to process a chunk of numbers
def process_chunk(chunk):
    """
    Process a chunk of numbers, squaring each element.

    Args:
    chunk (list): The list of numbers to process.

    Returns:
    list: A list containing the square of each input number.
    """
    return [square(n) for n in chunk]

# Create a list of 10^6 and 10^7 random numbers
numbers_10_6 = [random.randint(1, 1000000) for _ in range(10**6)]  # List of 10^6 numbers
numbers_10_7 = [random.randint(1, 1000000) for _ in range(10**7)]  # List of 10^7 numbers

# Sequential method: A simple for loop to compute the square of each number
def sequential(numbers):
    return [square(n) for n in numbers]

# Chunking function to split data into smaller chunks
def chunkify(numbers, chunk_size):
    """
    Split the list of numbers into chunks.

    Args:
    numbers (list): The list of numbers to process.
    chunk_size (int): The size of each chunk.

    Returns:
    list of list: A list containing chunks of numbers.
    """
    return [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

# Multiprocessing Pool with map() method using chunking
def multiprocessing_pool_map(numbers, pool_size=4, chunk_size=1000):
    """
    Use multiprocessing pool with map to process a list of numbers in chunks.

    Args:
    numbers (list): The list of numbers to process.
    pool_size (int): The size of the process pool.
    chunk_size (int): The size of each chunk of numbers to process.

    Returns:
    list: A list containing the square of each input number.
    """
    chunks = chunkify(numbers, chunk_size)  # Split numbers into chunks
    with multiprocessing.Pool(pool_size) as pool:
        # Use map to process each chunk in parallel
        results = pool.map(process_chunk, chunks)
    # Flatten the list of results
    return [item for sublist in results for item in sublist]

# Multiprocessing Pool with apply() for synchronous processing using chunking
def multiprocessing_pool_apply(numbers, pool_size=4, chunk_size=1000):
    """
    Use multiprocessing pool with apply() to process each chunk of numbers synchronously.

    Args:
    numbers (list): The list of numbers to process.
    pool_size (int): The size of the process pool.
    chunk_size (int): The size of each chunk of numbers to process.

    Returns:
    list: A list containing the square of each input number.
    """
    chunks = chunkify(numbers, chunk_size)  # Split numbers into chunks
    with multiprocessing.Pool(pool_size) as pool:
        results = [pool.apply(process_chunk, (chunk,)) for chunk in chunks]
        return [item for sublist in results for item in sublist]

# Asynchronous Multiprocessing Pool using apply_async() for chunking
def multiprocessing_pool_apply_async(numbers, pool_size=4, chunk_size=1000):
    """
    Use multiprocessing pool with apply_async() to process a list of numbers asynchronously.

    Args:
    numbers (list): The list of numbers to process.
    pool_size (int): The size of the process pool.
    chunk_size (int): The size of each chunk of numbers to process.

    Returns:
    list: A list containing the square of each input number.
    """
    chunks = chunkify(numbers, chunk_size)  # Split numbers into chunks
    with multiprocessing.Pool(pool_size) as pool:
        results = [pool.apply_async(process_chunk, (chunk,)) for chunk in chunks]
        return [r.get() for r in results]  # Get the results asynchronously

# ProcessPoolExecutor from concurrent.futures using chunking
def process_pool_executor(numbers, pool_size=4, chunk_size=1000):
    """
    Use ProcessPoolExecutor to process a list of numbers in chunks.

    Args:
    numbers (list): The list of numbers to process.
    pool_size (int): The size of the process pool.
    chunk_size (int): The size of each chunk of numbers to process.

    Returns:
    list: A list containing the square of each input number.
    """
    chunks = chunkify(numbers, chunk_size)  # Split numbers into chunks
    with ProcessPoolExecutor(pool_size) as executor:
        results = list(executor.map(process_chunk, chunks))
    # Flatten the list of results
    return [item for sublist in results for item in sublist]

# Timing and testing different methods
def time_tests(numbers, pool_size=4, chunk_size=1000):
    """
    Time the execution of different methods for processing numbers.

    Args:
    numbers (list): The list of numbers to process.
    pool_size (int): The size of the pool for multiprocessing.
    chunk_size (int): The size of each chunk to process.

    Returns:
    dict: A dictionary containing the execution time for each method.
    """
    # Sequential method
    start_time = time.time()
    sequential(numbers)
    sequential_time = time.time() - start_time

    # Multiprocessing Pool with map() method (using chunking)
    start_time = time.time()
    multiprocessing_pool_map(numbers, pool_size, chunk_size)
    multiprocessing_pool_map_time = time.time() - start_time

    # Multiprocessing Pool with apply() method (using chunking)
    start_time = time.time()
    multiprocessing_pool_apply(numbers, pool_size, chunk_size)
    multiprocessing_pool_apply_time = time.time() - start_time

    # Asynchronous Multiprocessing Pool (apply_async) (using chunking)
    start_time = time.time()
    multiprocessing_pool_apply_async(numbers, pool_size, chunk_size)
    multiprocessing_pool_apply_async_time = time.time() - start_time

    # ProcessPoolExecutor (using chunking)
    start_time = time.time()
    process_pool_executor(numbers, pool_size, chunk_size)
    process_pool_executor_time = time.time() - start_time

    return {
        "sequential_time": sequential_time,
        "multiprocessing_pool_map_time": multiprocessing_pool_map_time,
        "multiprocessing_pool_apply_time": multiprocessing_pool_apply_time,
        "multiprocessing_pool_apply_async_time": multiprocessing_pool_apply_async_time,
        "process_pool_executor_time": process_pool_executor_time
    }

# Run with 10^6 numbers
times_10_6 = time_tests(numbers_10_6, pool_size=4)

# Run with 10^7 numbers
times_10_7 = time_tests(numbers_10_7, pool_size=4)

# Display results
print("Timing Results for 10^6 Numbers:")
print(times_10_6)

print("\nTiming Results for 10^7 Numbers:")
print(times_10_7)
