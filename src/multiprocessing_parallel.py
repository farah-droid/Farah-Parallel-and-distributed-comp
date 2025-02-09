import multiprocessing

# Function to calculate the sum of a range of numbers
def process_sum(start, end, result, index):
    partial_sum = sum(range(start, end))
    print(f"Process {index} sum: {partial_sum}")  # Debugging output
    result[index] = partial_sum

def parallel_sum_multiprocessing(n, num_processes=6):  # Set to 6 processes
    step = n // num_processes
    processes = []
    result = multiprocessing.Array('l', num_processes)  # Use 'l' for long instead of 'i' to avoid overflow
    
    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step if i < num_processes - 1 else n + 1  # Ensure no overlap and include all numbers
        process = multiprocessing.Process(target=process_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  # Ensure all processes complete

    return sum(result)
