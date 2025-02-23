import time

def initialize_display():
    """
    Initializes the display layout.
    """
    print("Current temperatures:")
    print("Latest Temperatures: Sensor 0: --°C Sensor 1: --°C Sensor 2: --°C")
    print("Sensor 1 Average: --°C")
    print("Sensor 2 Average: --°C")
    print("Sensor 3 Average: --°C")

def update_display(latest_temperatures, temperature_averages):
    """
    Updates the display with the latest temperatures and averages.
    """
    print("\rLatest Temperatures: Sensor 0: {}°C Sensor 1: {}°C Sensor 2: {}°C".format(
        latest_temperatures.get(0, "--"),
        latest_temperatures.get(1, "--"),
        latest_temperatures.get(2, "--")), end="")
    print("\rSensor 1 Average: {}°C".format(temperature_averages.get(0, "--")), end="")
    print("\rSensor 2 Average: {}°C".format(temperature_averages.get(1, "--")), end="")
    print("\rSensor 3 Average: {}°C".format(temperature_averages.get(2, "--")), end="")