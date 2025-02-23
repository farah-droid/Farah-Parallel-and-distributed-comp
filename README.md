# Lab 4: Real-Time Temperature Monitoring System

## Overview
This project simulates a real-time temperature monitoring system using multiple sensors. It demonstrates the use of **threading**, **queues**, and **synchronization mechanisms** in Python to handle concurrent tasks and shared resources.

The system:
1. Simulates temperature readings from multiple sensors.
2. Calculates the average temperature for each sensor.
3. Displays the latest temperatures and averages in real-time on the console.

---

## Features
- **Sensor Simulation:** Each sensor generates random temperatures between 15°C and 40°C every 1 second.
- **Data Processing:** The system calculates the average temperature for each sensor every 5 seconds.
- **Real-Time Display:** The console displays the latest temperatures and averages, updating in place without erasing the screen.
- **Thread Synchronization:** Uses `threading.Lock` and `queue.Queue` to safely share data between threads.

---

## File Structure
project/ <br>
├── sensors/ │ <br>
├── init.py │<br>
├── sensor_simulator.py # Simulates sensor readings<br>
│ └── data_processor.py # Processes temperature data<br>
├── display/ │ <br>
├── init.py │<br>
└── display_logic.py # Handles console display<br>
└── main.py # Main program to start the system<br>

---

## How to Run the Program
1. Clone or download the project files.
2. Ensure you have Python installed (Python 3.6 or higher recommended).
3. Navigate to the project directory:
   ```bash
   cd path/to/project
   ```
Run the main program:
```bash
python main.py
```
Observe the real-time temperature updates in the console.

## Synchronization Mechanisms
### For Sensor Simulation (simulate_sensor):
**Mechanism:** ```threading.Lock```
**Purpose:** Ensures that only one thread can update the latest_temperatures dictionary at a time, preventing race conditions.
### For Data Processing (process_temperatures):
**Mechanism:** ```threading.Lock```
**Purpose:** Ensures that only one thread can update the temperature_averages dictionary at a time, preventing race conditions.
### For Thread Communication:
**Mechanism:** ```queue.Queue```
**Purpose:** Safely passes data between the sensor threads and the data processor thread.
### For Display Updates (update_display):
**Mechanism:** No explicit synchronization is needed because the display thread only reads from the shared dictionaries, which are already protected by locks.
## Why No Metrics?
Because the goals are:
**To understand how to use threading to perform multiple tasks concurrently.**
**To learn how to use synchronization mechanisms like locks and queues to safely share data between threads.**
**To implement a real-time system that updates and displays data dynamically.**
Adding complex metrics (e.g., standard deviation, variance, etc.) would distract from these primary learning objectives.

## Bonus Implementation
**Latest Temperatures:** Updated every 1 second.
**Average Temperatures:** Updated every 5 seconds.
**Display Updates:** Refreshes in place without erasing the console.
