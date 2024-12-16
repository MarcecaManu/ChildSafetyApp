# ultrasonic_handler.py
from gpiozero import DistanceSensor
from threading import Thread
import time
import math

class UltrasonicSensorHandler:
    def __init__(self, pin1, pin2, pin3):



        self.door_lowersize = 0
        self.door_highersize = 0
        self.calibrated = False
        self.tolerance = 5   # Minimum difference beetween door size and registered value in cm

        self.lower_detected = False
        self.higher_detected = False
        self.actuator_detected = False


        # Initialize three ultrasonic sensors
        self.lower_sensor = DistanceSensor(echo=pin1[0], trigger=pin1[1])
        self.higher_sensor = DistanceSensor(echo=pin2[0], trigger=pin2[1])
        self.actuator_sensor = DistanceSensor(echo=pin3[0], trigger=pin3[1])

        # Store the latest distance readings
        self.distances = {"lower_sensor": None, "higher_sensor": None, "actuator_sensor": None}

        # Get stable door size
        print("Calibrating door sensors...")
        while(not self.calibrated):
            self.calibrate_sensors()
        print("Calibration complete. Door size is " + str(self.door_lowersize))

        self.lower_sensor.threshold_distance = self.door_lowersize - 0.05
        self.higher_sensor.threshold_distance = self.door_highersize - 0.05

        # Start the monitoring thread
        thread = Thread(target=self.monitor_sensor_low)
        thread.daemon = True  # The thread will exit when the main program exits
        thread.start()

        # Start the monitoring thread
        thread = Thread(target=self.monitor_sensor_high)
        thread.daemon = True  # The thread will exit when the main program exits
        thread.start()

        # Start the monitoring thread
        thread = Thread(target=self.monitor_sensor_actuator)
        thread.daemon = True  # The thread will exit when the main program exits
        thread.start()
        #self.monitor_sensors()


    # Measure the distance three times and check for a stable door size to set.
    def calibrate_sensors(self):
            
            measures_lower = []
            measures_higher = []

            for i in range(3):
                # Update the distance readings
                self.distances["lower_sensor"] = self.lower_sensor.distance   
                measures_lower.append(self.distances["lower_sensor"])

                self.distances["higher_sensor"] = self.higher_sensor.distance 
                measures_higher.append(self.distances["higher_sensor"])

                time.sleep(1)

            mean = sum(measures_lower) / len(measures_lower)   # mean
            var  = sum(pow(x-mean,2) for x in measures_lower) / len(measures_lower)  # variance
            std_lower  = math.sqrt(var)  # standard deviation

            mean = sum(measures_higher) / len(measures_higher)   # mean
            var  = sum(pow(x-mean,2) for x in measures_higher) / len(measures_higher)  # variance
            std_higher  = math.sqrt(var)  # standard deviation

            if std_lower > 2 or std_higher > 2:
                print("Unable to calibrate door sensors: keep the door area free. Retrying...")
            else:
                self.calibrated = True
                self.door_lowersize = measures_lower[2]
                self.door_highersize = measures_higher[2]
                


    def monitor_sensor_low(self):
        while True:
            self.lower_sensor.wait_for_in_range()
            self.lower_detected = True
            print("Lower sensor - Motion detected!")


            # # Update the distance readings
            # self.distances["lower_sensor"] = self.lower_sensor.distance * 100  # Convert to cm
            # self.distances["higher_sensor"] = self.higher_sensor.distance * 100

            # self.distances["actuator_sensor"] = self.actuator_sensor.distance * 100

            # self.lower_detected = self.distances["lower_sensor"] < self.door_lowersize - self.tolerance
            # self.higher_detected = self.distances["higher_sensor"] < self.door_highersize - self.tolerance
                

            # # Print the distances for debugging
            # print(f"Sensor 1: {self.distances['lower_sensor']:.2f} cm")
            # print(f"Sensor 2: {self.distances['higher_sensor']:.2f} cm")
            # print(f"Sensor 3: {self.distances['actuator_sensor']:.2f} cm")
            # print("-" * 20)
            time.sleep(1)
            self.lower_sensor.wait_for_out_of_range()
            # print("Lower sensor - No motion detected")
            self.lower_detected = False

    def monitor_sensor_high(self):
        while True:
            self.higher_sensor.wait_for_in_range()
            self.higher_detected = True
            print("Higher sensor - Motion detected!")


            # # Update the distance readings
            # self.distances["lower_sensor"] = self.lower_sensor.distance * 100  # Convert to cm
            # self.distances["higher_sensor"] = self.higher_sensor.distance * 100

            # self.distances["actuator_sensor"] = self.actuator_sensor.distance * 100

            # self.lower_detected = self.distances["lower_sensor"] < self.door_lowersize - self.tolerance
            # self.higher_detected = self.distances["higher_sensor"] < self.door_highersize - self.tolerance
                

            # # Print the distances for debugging
            # print(f"Sensor 1: {self.distances['lower_sensor']:.2f} cm")
            # print(f"Sensor 2: {self.distances['higher_sensor']:.2f} cm")
            # print(f"Sensor 3: {self.distances['actuator_sensor']:.2f} cm")
            # print("-" * 20)
            time.sleep(1)
            self.higher_sensor.wait_for_out_of_range()
            # print("Higher sensor - No motion detected")
            self.higher_detected = False

    def monitor_sensor_actuator(self):
        time.sleep(3)
        while True:
            self.actuator_sensor.wait_for_in_range()
            self.actuator_detected = True
            print("Actuator sensor - Motion detected!")


            # # Update the distance readings
            # self.distances["lower_sensor"] = self.lower_sensor.distance * 100  # Convert to cm
            # self.distances["higher_sensor"] = self.higher_sensor.distance * 100

            # self.distances["actuator_sensor"] = self.actuator_sensor.distance * 100

            # self.lower_detected = self.distances["lower_sensor"] < self.door_lowersize - self.tolerance
            # self.higher_detected = self.distances["higher_sensor"] < self.door_highersize - self.tolerance
                

            # # Print the distances for debugging
            # print(f"Sensor 1: {self.distances['lower_sensor']:.2f} cm")
            # print(f"Sensor 2: {self.distances['higher_sensor']:.2f} cm")
            # print(f"Sensor 3: {self.distances['actuator_sensor']:.2f} cm")
            # print("-" * 20)
            time.sleep(1)
            self.actuator_sensor.wait_for_out_of_range()
            # print("Higher sensor - No motion detected")
            self.actuators_detected = False



# Create an instance of the handler
ultrasonic_handler = UltrasonicSensorHandler(
    pin1=(27, 17),  # Echo and Trigger pins for sensor 1
    pin2=(23, 22),  # Echo and Trigger pins for sensor 2
    pin3=(25, 24)   # Echo and Trigger pins for sensor 3
)