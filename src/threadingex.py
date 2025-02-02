import threading
import time
import random

def generate_chars():
    chars = [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(500)]  # Split work in half
    return ''.join(chars)

def generate_numbers():
    numbers = [random.randint(1, 100) for _ in range(500)]
    return sum(numbers)

def run_threading():
    start_time = time.time()

    thread1 = threading.Thread(target=generate_chars)
    thread2 = threading.Thread(target=generate_chars)

    thread3 = threading.Thread(target=generate_numbers)
    thread4 = threading.Thread(target=generate_numbers)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    end_time = time.time()

    print(f"Threading execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    run_threading()