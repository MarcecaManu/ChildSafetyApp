import time
from motionHandler import pir_handler
from ultrasonicHandler import ultrasonic_handler
from actuatorHandler import actuator_handler
from mqttHandler import mqtt_handler

class Main:
    # Class-level attributes for better readability
    FREE = "FREE"                    # No one's at the door
    CHECK_LOW = "CHECK_LOW"          # Lower sensor has been triggered, waiting for the other sensor
    CHECK_HIGH = "CHECK_HIGH"        # Higher sensor has been triggered, waiting for the other sensor
    OCCUPIED_CHILD = "OCCUPIED_CHILD"  # Child detected passing through the door
    OCCUPIED_ADULT = "OCCUPIED_ADULT"  # Adult detected passing through the door

    # Threshold values (in seconds)
    timeslot_child_alone = 60       # Time after which a notification is sent if a child is alone
    timeslot_actuator_off = 10      # Time before re-enabling the actuator
    notification_sent = False       # Flag to indicate if a notification was already sent

    def __init__(self):
        # Initialize room occupancy flags
        self.child_in_room = False
        self.adult_in_room = False

        # Sensor and motion detection timeouts
        self.timeslot_both_sensors = 0.5  # Time to detect both sensors triggered
        self.timeslot_pir = 30           # Timeout for detecting motion in the room

        # Status variables
        self.previous_status = self.FREE
        self.door_status = self.FREE

        # Timestamps for tracking events
        self.timestamp_door = time.time()
        self.timestamp_child_alone = time.time()
        self.timestamp_pir = time.time()
        self.timestamp_actuator = time.time()

    # Helper functions to update timestamps
    def updateTimestampDoor(self):
        self.timestamp_door = time.time()

    def updateTimestampPir(self):
        self.timestamp_pir = time.time()

    def updateTimestampChild(self):
        self.timestamp_child_alone = time.time()

    def updateTimestampActuator(self):
        self.timestamp_actuator = time.time()

    # Determine the current door status based on sensor inputs
    def getCurrentStatusDoor(self):
        if self.door_status == self.FREE:
            # Check if either sensor is triggered
            if ultrasonic_handler.lower_detected:
                self.door_status = self.CHECK_LOW
                self.updateTimestampDoor()
            elif ultrasonic_handler.higher_detected:
                self.door_status = self.CHECK_HIGH
                self.updateTimestampDoor()

        if self.door_status in [self.CHECK_LOW, self.CHECK_HIGH]:
            # Check if both sensors are triggered within the threshold
            if time.time() - self.timestamp_door < self.timeslot_both_sensors:
                if self.door_status == self.CHECK_LOW and ultrasonic_handler.higher_detected:
                    self.door_status = self.OCCUPIED_ADULT
                elif self.door_status == self.CHECK_HIGH and ultrasonic_handler.lower_detected:
                    self.door_status = self.OCCUPIED_ADULT
            else:
                # If the higher sensor triggered first, assume no detection
                if self.door_status == self.CHECK_HIGH:
                    self.door_status = self.FREE
                else:
                    self.door_status = self.OCCUPIED_CHILD

        # Reset door status if neither sensor is active
        if self.door_status in [self.OCCUPIED_CHILD, self.OCCUPIED_ADULT]:
            if not ultrasonic_handler.lower_detected and not ultrasonic_handler.higher_detected:
                self.door_status = self.FREE

        # Log status change for debugging
        if self.previous_status != self.door_status:
            print(self.door_status)

    # Determine the current room occupancy status
    def getCurrentStatusRoom(self):
        current_status_child = self.child_in_room
        current_status_adult = self.adult_in_room

        # Update room occupancy based on the door status
        if self.door_status == self.FREE:
            if self.previous_status == self.OCCUPIED_CHILD:
                self.child_in_room = not self.child_in_room
                self.updateTimestampPir()
            elif self.previous_status == self.OCCUPIED_ADULT:
                self.adult_in_room = not self.adult_in_room
                self.updateTimestampPir()

        # Handle motion detection in the room
        if self.adult_in_room or self.child_in_room:
            if pir_handler.motion_detected:
                self.updateTimestampPir()
            elif time.time() - self.timestamp_pir > self.timeslot_pir:
                # No motion detected for the timeout duration
                print(f"No motion detected for {self.timeslot_pir}s. Assuming the room is empty.")
                self.adult_in_room = False
                self.child_in_room = False

        # Log changes in room occupancy
        if current_status_adult != self.adult_in_room:
            if self.adult_in_room:
                print("An adult is in the room")
            else:
                print("No adults in this room")

        if current_status_child != self.child_in_room:
            if self.child_in_room:
                print("A child is in the room")
                if not self.adult_in_room:
                    print("Child is alone!")
                    self.updateTimestampChild()
            else:
                print("No children in this room")

        # Update previous door status for tracking changes
        self.previous_status = self.door_status

    # Actuator control logic based on room occupancy
    def actuate(self):
        if self.child_in_room and not self.adult_in_room:
            # Send notification if the child is alone for too long
            if not self.notification_sent and time.time() - self.timestamp_child_alone > self.timeslot_child_alone:
                mqtt_handler.send_notification(f"A child has been alone in the room for over {self.timeslot_child_alone} seconds!")
                self.notification_sent = True
                print(f"A child has been alone for more than {self.timeslot_child_alone}s. Sending notification...")

            # Turn off actuator if the child is near it
            if actuator_handler.actuator_is_on and ultrasonic_handler.actuator_detected:
                actuator_handler.turnOffActuator()
                self.updateTimestampActuator()
                mqtt_handler.send_notification("An appliance has been disabled for safety.")
                print("A child alone in the room has got close to a plug. Turning it OFF...")
        elif not actuator_handler.actuator_is_on and not (not self.adult_in_room and self.child_in_room) and time.time() - self.timestamp_actuator > self.timeslot_actuator_off:
            # Re-enable the actuator if conditions are safe
            print(f"{self.timeslot_actuator_off}s have passed. Turning actuator back ON...")
            actuator_handler.turnOnActuator()
            print("Actuator re-enabled.")
        else:
            # Reset notification flag when conditions are met
            self.notification_sent = False
            self.updateTimestampChild()


# Create an instance of the Main class
main_instance = Main()

# Main loop to continuously monitor and handle room events
while True:
    main_instance.getCurrentStatusDoor()
    main_instance.getCurrentStatusRoom()
    main_instance.actuate()
    time.sleep(0.001)  # Reduce CPU usage while allowing data to be updated
