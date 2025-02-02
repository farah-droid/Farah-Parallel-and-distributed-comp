from multiprocessing import Process
import time
import random

def generate_chars():
    chars = [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(500)]  # Split work in half
    return ''.join(chars)

def generate_numbers():
    numbers = [random.randint(1, 100) for _ in range(500)]
    return sum(numbers)

def run_processes():
    start_time = time.time()

    process1 = Process(target=generate_chars)
    process2 = Process(target=generate_chars)

    process3 = Process(target=generate_numbers)
    process4 = Process(target=generate_numbers)

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    end_time = time.time()

    print(f"Process execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    run_processes()