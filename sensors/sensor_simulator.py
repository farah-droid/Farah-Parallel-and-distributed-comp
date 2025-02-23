import random
import time
from threading import Lock

# Global dictionary to store latest temperatures
latest_temperatures = {}
lock = Lock()

def simulate_sensor(sensor_id, queue):
    """
    Simulates a sensor by generating random temperatures and updating the global dictionary.
    """
    while True:
        temperature = random.randint(15, 40)  # Generate random temp
        with lock:
            latest_temperatures[sensor_id] = temperature  # Update global 
            queue.put((sensor_id, temperature)) 
        time.sleep(1)  # Wait for 1 second before next reading