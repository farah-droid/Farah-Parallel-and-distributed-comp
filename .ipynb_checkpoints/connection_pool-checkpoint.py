import multiprocessing
import random
import time

class ConnectionPool:
    """
    A ConnectionPool class simulates a limited pool of database connections
    using a semaphore to control access to the pool.
    """

    def __init__(self, pool_size):
        """
        Initializes the connection pool with a specified number of connections.

        Args:
        pool_size (int): The number of available connections in the pool.
        """
        self.pool_size = pool_size
        self.manager = multiprocessing.Manager()  # Manager for shared state across processes
        self.connections = self.manager.list([f"Connection-{i+1}" for i in range(pool_size)])
        self.semaphore = multiprocessing.Semaphore(pool_size)  # Semaphore to limit access to the pool

    def get_connection(self):
        """
        Acquires a connection from the pool.

        Blocks if no connections are available, until a connection is released.

        Returns:
        str: A connection from the pool.
        """
        self.semaphore.acquire()  # Wait until a connection is available
        connection = self.connections.pop()  # Get a connection from the pool
        return connection

    def release_connection(self, connection):
        """
        Releases a connection back to the pool.

        Args:
        connection (str): The connection to return to the pool.
        """
        self.connections.append(connection)  # Return the connection to the pool
        self.semaphore.release()  # Allow another process to acquire a connection

def access_database(connection_pool):
    """
    Simulates a database operation by acquiring and releasing a connection.

    Args:
    connection_pool (ConnectionPool): The connection pool to access.
    """
    print(f"{multiprocessing.current_process().name} is waiting for a connection.")
    
    connection = connection_pool.get_connection()  # Get a connection from the pool
    print(f"{multiprocessing.current_process().name} acquired {connection}.")
    
    # Simulate a random amount of work
    time.sleep(random.randint(1, 3))  # Simulate work by sleeping for 1-3 seconds
    
    # Release the connection back to the pool
    connection_pool.release_connection(connection)
    print(f"{multiprocessing.current_process().name} released {connection}.")

def main():
    """
    Main function to simulate database operations using multiple processes
    with a limited connection pool.
    """
    # Create a pool with 3 database connections
    connection_pool = ConnectionPool(pool_size=3)
    
    # Create a list of processes
    processes = []
    for _ in range(6):  # Simulating 6 processes trying to access the pool
        process = multiprocessing.Process(target=access_database, args=(connection_pool,))
        processes.append(process)
        process.start()
    
    # Wait for all processes to finish
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()
