from src.sequential import run_sequential
from src.threadingex import run_threading
from src.processes import run_processes

def main():
    print("Running sequential case:")
    run_sequential()

    print("\nRunning threading case:")
    run_threading()

    print("\nRunning processes case:")
    run_processes()

if __name__ == "__main__":
    main()