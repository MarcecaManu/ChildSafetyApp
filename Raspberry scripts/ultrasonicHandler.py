# ultrasonic_handler.py
from gpiozero import DistanceSensor
from threading import Thread
import time

class UltrasonicSensorHandler:
    def __init__(self, pin1, pin2, pin3):
        # Initialize three ultrasonic sensors
        self.sensor1 = DistanceSensor(echo=pin1[0], trigger=pin1[1], max_distance=2)
        self.sensor2 = DistanceSensor(echo=pin2[0], trigger=pin2[1], max_distance=2)
        self.sensor3 = DistanceSensor(echo=pin3[0], trigger=pin3[1], max_distance=2)

        # Store the latest distance readings
        self.distances = {"sensor1": None, "sensor2": None, "sensor3": None}

        # Start the monitoring thread
        thread = Thread(target=self.monitor_sensors)
        thread.daemon = True  # The thread will exit when the main program exits
        thread.start()

    def monitor_sensors(self):
        while True:
            # Update the distance readings
            self.distances["sensor1"] = self.sensor1.distance * 100  # Convert to cm
            self.distances["sensor2"] = self.sensor2.distance * 100
            self.distances["sensor3"] = self.sensor3.distance * 100

            # Print the distances for debugging
            print(f"Sensor 1: {self.distances['sensor1']:.2f} cm")
            print(f"Sensor 2: {self.distances['sensor2']:.2f} cm")
            print(f"Sensor 3: {self.distances['sensor3']:.2f} cm")
            print("-" * 20)

            # Update every second
            time.sleep(1)

# Create an instance of the handler
ultrasonic_handler = UltrasonicSensorHandler(
    pin1=(23, 24),  # Echo and Trigger pins for sensor 1
    pin2=(17, 18),  # Echo and Trigger pins for sensor 2
    pin3=(27, 22)   # Echo and Trigger pins for sensor 3
)
