# main.py
import time
from src.threading_parallel import parallel_sum_threading
from src.multiprocessing_parallel import parallel_sum_multiprocessing
from src.seq3 import seq3  # Import the sequential function

def main():
    n = 10**6  # Large number
    
    # Run sequential
    start_time = time.time()
    total_sum_sequential = seq3(n)
    end_time = time.time()
    
    execution_time_sequential = end_time - start_time
    speedup_sequential = execution_time_sequential / execution_time_sequential  # Sequential time compared to itself
    efficiency_sequential = speedup_sequential / 1  # Efficiency for sequential (1 process)
    
    print("\nSequential (seq3) Results:")
    print(f"Sum: {total_sum_sequential}")
    print(f"Execution Time (Sequential): {execution_time_sequential:.6f} seconds")
    print(f"Speedup (Sequential): {speedup_sequential:.2f}")
    print(f"Efficiency (Sequential): {efficiency_sequential:.4f}")
    
    # Run multiprocessing
    start_time = time.time()
    total_sum_parallel_multiprocessing = parallel_sum_multiprocessing(n)
    end_time = time.time()
    
    execution_time_multiprocessing = end_time - start_time
    speedup_multiprocessing = execution_time_sequential / execution_time_multiprocessing  # Sequential time vs multiprocessing time
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
    speedup_threading = execution_time_sequential / execution_time_threading  # Sequential time vs threading time
    efficiency_threading = speedup_threading / 6  # 6 threads
    
    print("\nThreading Results:")
    print(f"Sum: {total_sum_parallel_threading}")
    print(f"Execution Time (Threading): {execution_time_threading:.6f} seconds")
    print(f"Speedup (Threading): {speedup_threading:.2f}")
    print(f"Efficiency (Threading): {efficiency_threading:.4f}")

if __name__ == "__main__":
    main()
