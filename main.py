import threading
import queue
import time
from sensors.sensor_simulator import simulate_sensor, latest_temperatures
from sensors.data_processor import process_temperatures, temperature_averages
from display.display_logic import initialize_display, update_display

# Create a queue
data_queue = queue.Queue()

initialize_display()

sensor_threads = []
for i in range(3):  # Assuming 3 sensors
    thread = threading.Thread(target=simulate_sensor, args=(i, data_queue), daemon=True)
    sensor_threads.append(thread)
    thread.start()

processor_thread = threading.Thread(target=process_temperatures, args=(data_queue,), daemon=True)
processor_thread.start()

while True:
    update_display(latest_temperatures, temperature_averages)
    time.sleep(5)  # Update display every 5 seconds