from gpiozero import MotionSensor, LED
from threading import Thread
import time

class MotionSensorHandler:
    def __init__(self, pir_pin, led_pin):
        self.pir = MotionSensor(pir_pin)
        self.led = LED(led_pin)
        self.motion_detected = False

        # Start monitoring in a separate thread
        thread = Thread(target=self.monitor_motion)
        thread.daemon = True  # Ensures the thread exits when the main program does
        thread.start()

    def monitor_motion(self):
        while True:
            self.pir.wait_for_motion()
            self.motion_detected = True
            self.led.on()
            print("PIR - Motion detected!")

            time.sleep(2)
            self.pir.wait_for_no_motion()
            self.motion_detected = False
            self.led.off()
            print("PIR - No motion detected.")
            time.sleep(2)

# Create an instance of the handler with PIR on GPIO 18 and LED on GPIO 12
pir_handler = MotionSensorHandler(pir_pin=18, led_pin=12)

# # Keep the script running to allow motion detection to work
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Program stopped.")
