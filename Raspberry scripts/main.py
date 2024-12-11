# main.py
from pirSensor import pir_handler
from ultrasonicHandler import ultrasonic_handler
import time


def getCurrentStatus():
    # Access the latest distance readings
    distances = ultrasonic_handler.distances

    # Check and print sensor data
    if distances["sensor1"] is not None:
        print(f"Sensor 1 Distance: {distances['sensor1']:.2f} cm")
    if distances["sensor2"] is not None:
        print(f"Sensor 2 Distance: {distances['sensor2']:.2f} cm")
    if distances["sensor3"] is not None:
        print(f"Sensor 3 Distance: {distances['sensor3']:.2f} cm")

    # Example condition: If any sensor detects an object within 50 cm
    if any(distance is not None and distance < 50 for distance in distances.values()):
        print("Warning: Object detected within 50 cm!")

    print("=" * 30)

    if pir_handler.motion_detected:
        print("Someone is in the room!")        # Room is NOT empty
    else:
        print("The room is empty.")             # Room is empty

while True:
    getCurrentStatus()
