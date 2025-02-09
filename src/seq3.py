import time

# Sequential Summation
def sequential_sum(n):
    total = sum(range(1, n+1))
    return total

# Measure the execution time
n = 10**6  # Large number
start_time = time.time()

total_sum = sequential_sum(n)

end_time = time.time()

execution_time = end_time - start_time

print(f"Sum: {total_sum}")
print(f"Execution Time (Sequential): {execution_time:.6f} seconds")
