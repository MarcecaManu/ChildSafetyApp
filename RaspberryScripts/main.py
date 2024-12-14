import time
from pirSensor import pir_handler
from ultrasonicHandler import ultrasonic_handler

def getCurrentStatus():
    if ultrasonic_handler.lower_detected:
        print("lower sensor detected something!")
    else:
        print("lower sensor - nothing")

    if ultrasonic_handler.higher_detected:
        print("higher sensor detected something!")
    else:
        print("higher sensor - nothing")


    if pir_handler.motion_detected:
        print("Motion detected!")
    else:
        print("No motion detected.")

while True:
    getCurrentStatus()
    time.sleep(0.001)  # Reduce CPU usage, but still allow data to be updated
