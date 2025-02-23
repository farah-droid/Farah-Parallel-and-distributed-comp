import time
from threading import Lock

# Global dictionary to store temperature averages
temperature_averages = {}
lock = Lock()

def process_temperatures(queue):
    """
    Processes temperature data from the queue and calculates averages.
    """
    sensor_data = {}  # Local

    while True:
        if not queue.empty():
            sensor_id, temperature = queue.get() 

            with lock:
                if sensor_id not in sensor_data:
                    sensor_data[sensor_id] = [] 

                sensor_data[sensor_id].append(temperature)  # new reading added
                if len(sensor_data[sensor_id]) > 5:  # Keep only the last 5
                    sensor_data[sensor_id].pop(0)

                # Calculate average temperature
                average = sum(sensor_data[sensor_id]) / len(sensor_data[sensor_id])
                temperature_averages[sensor_id] = average  # Update the global averages

        time.sleep(5)  # Update averages every 5 seconds shows on display