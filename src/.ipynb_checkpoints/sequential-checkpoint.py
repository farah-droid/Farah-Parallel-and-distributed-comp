import random
import time

def generate_chars():
    chars = [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(1000000)]
    return ''.join(chars)

def generate_numbers():
    numbers = [random.randint(1, 100) for _ in range(1000000)]
    return sum(numbers)

def run_sequential():
    start_time = time.time()
    generate_chars()
    generate_numbers()
    end_time = time.time()
    print(f"Sequential execution time: {end_time - start_time} seconds")