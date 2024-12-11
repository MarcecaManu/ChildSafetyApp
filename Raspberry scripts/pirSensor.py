# pir_sensor.py
from gpiozero import MotionSensor
from threading import Thread
import time

class PIRSensorHandler:
    def __init__(self, pin):
        self.pir = MotionSensor(pin)
        self.motion_detected = False

        # Start monitoring in a separate thread
        thread = Thread(target=self.monitor_motion)
        thread.daemon = True  # Ensures the thread exits when the main program does
        thread.start()

    def monitor_motion(self):
        while True:
            self.pir.wait_for_motion()
            self.motion_detected = True
            print("Motion detected!")

            self.pir.wait_for_no_motion()
            self.motion_detected = False
            print("No motion detected.")

# Create an instance of the handler
pir_handler = PIRSensorHandler(12)