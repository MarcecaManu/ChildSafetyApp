import time
from motionHandler import pir_handler
from ultrasonicHandler import ultrasonic_handler
from actuatorHandler import actuator_handler
from mqttHandler import mqtt_handler

class Main:
    # Class-level attributes for better readability
    FREE = "FREE"                       # No one's at the door
    CHECK_LOW = "CHECK_LOW"             # LOWER sensor has been triggered, waiting for the other sensor
    CHECK_HIGH = "CHECK_HIGH"           # HIGHER sensor has been triggered, waiting for the other sensor
    CHECK_DIRECTION = "CHECK_DIRECTION" # DIRECTION sensor has been triggered, waiting for the other sensor
    OCCUPIED_CHILD = "OCCUPIED_CHILD"   # Child detected passing through the door
    OCCUPIED_ADULT = "OCCUPIED_ADULT"   # Adult detected passing through the door

    timeslot_child_alone = 60    # Time in seconds for a child to be considered alone
    timeslot_actuator_off = 10   # Time in seconds before re-enabling the actuator
    notification_sent = False    # Tracks if a notification has already been sent

    def __init__(self):
        # Tracks the count of children and adults in the room
        self.children_in_room = 0
        self.adults_in_room = 0
        self.entering = None  # Tracks if someone is entering or exiting

        # Time intervals (in seconds) for various checks
        self.timeslot_door_sensors = 0.5
        self.timeslot_pir = 30

        # Statuses
        self.previous_status = self.FREE
        self.door_status = self.FREE

        # Timestamps to track the timing of events
        self.timestamp_door = time.time()
        self.timestamp_direction = time.time()
        self.timestamp_child_alone = time.time()
        self.timestamp_pir = time.time()
        self.timestamp_actuator = time.time()

    # Utility functions to update timestamps
    def updateTimestampDoor(self):
        self.timestamp_door = time.time()

    def updateTimestampDirection(self):
        self.timestamp_direction = time.time()

    def updateTimestampPir(self):
        self.timestamp_pir = time.time()

    def updateTimestampChild(self):
        self.timestamp_child_alone = time.time()

    def updateTimestampActuator(self):
        self.timestamp_actuator = time.time()

    # Returns True if there are children in the room without adults
    def childrenAlone(self):
        return self.children_in_room > 0 and self.adults_in_room == 0

    def getCurrentStatusDoor(self):
        # Check initial status of the door
        if self.door_status == self.FREE:
            if ultrasonic_handler.lower_detected:
                self.door_status = self.CHECK_LOW
                self.updateTimestampDoor()
            elif ultrasonic_handler.higher_detected:
                self.door_status = self.CHECK_HIGH
                self.updateTimestampDoor()
            elif ultrasonic_handler.direction_detected:
                self.entering = True  # Assume someone is entering
                self.updateTimestampDirection()

        # Check if both sensors are triggered within the allowed time
        if self.door_status in [self.CHECK_LOW, self.CHECK_HIGH]:
            self.checkDoor()
            if self.entering is None:
                self.entering = False  # Assume exit if direction isn't clear
            self.updateTimestampDirection()

        # Reset the door status if no sensors are triggered
        if self.door_status in [self.OCCUPIED_CHILD, self.OCCUPIED_ADULT]:
            if not ultrasonic_handler.lower_detected and not ultrasonic_handler.higher_detected:
                self.door_status = self.FREE

        # Debugging output to track status changes
        if self.previous_status != self.door_status:
            print(self.door_status)

    def checkDoor(self):
        # Handle transitions when both sensors are triggered
        if time.time() - self.timestamp_door < self.timeslot_door_sensors:
            if self.door_status == self.CHECK_LOW and ultrasonic_handler.higher_detected:
                self.door_status = self.OCCUPIED_ADULT
            elif self.door_status == self.CHECK_HIGH and ultrasonic_handler.lower_detected:
                self.door_status = self.OCCUPIED_ADULT
        else:
            if self.door_status == self.CHECK_HIGH:
                self.door_status = self.FREE
            else:
                self.door_status = self.OCCUPIED_CHILD

    def getCurrentStatusRoom(self):
        # Track previous room status
        current_status_child = self.children_in_room
        current_status_adult = self.adults_in_room

        # Adjust room count based on door status and direction
        if self.door_status == self.FREE:
            if self.previous_status == self.OCCUPIED_CHILD:
                self.adjustRoomCount("child")
            elif self.previous_status == self.OCCUPIED_ADULT:
                self.adjustRoomCount("adult")

            # Clear entering state if no action occurs within the allowed time
            elif self.previous_status == self.FREE:
                if self.entering is not None and time.time() - self.timestamp_direction > self.timeslot_door_sensors:
                    self.entering = None

        # Update PIR status to determine if the room is empty
        if self.adults_in_room > 0 or self.children_in_room > 0:
            if pir_handler.motion_detected:
                self.updateTimestampPir()
            elif time.time() - self.timestamp_pir > self.timeslot_pir:
                print(f"No motion detected for {self.timeslot_pir}s. Assuming the room is empty.")
                self.adults_in_room = 0
                self.children_in_room = 0

        # Log status changes
        self.logRoomChanges(current_status_child, current_status_adult)

        # Update previous status for comparison
        self.previous_status = self.door_status

    def adjustRoomCount(self, person_type):
        # Adjust room counts based on direction
        if self.entering:
            if person_type == "child":
                self.children_in_room += 1
            elif person_type == "adult":
                self.adults_in_room += 1
        else:
            if person_type == "child":
                self.children_in_room = max(0, self.children_in_room - 1)
            elif person_type == "adult":
                self.adults_in_room = max(0, self.adults_in_room - 1)
        self.entering = None
        self.updateTimestampPir()

    def logRoomChanges(self, prev_children, prev_adults):
        # Print changes in room occupancy
        if prev_adults > self.adults_in_room:
            print("An adult has left the room")
        elif prev_adults < self.adults_in_room:
            print("An adult has entered the room")

        if prev_children > self.children_in_room:
            print("A child has left the room")
        elif prev_children < self.children_in_room:
            print("A child has entered the room")

        # Display the updated status
        self.printStatus()

    def printStatus(self):
        print(f"Adults: {self.adults_in_room} | Children: {self.children_in_room}")

    def actuate(self):
        # Manage actuator behavior based on room occupancy
        if self.childrenAlone():
            self.handleChildAlone()
        elif not actuator_handler.actuator_is_on and not self.childrenAlone() and time.time() - self.timestamp_actuator > self.timeslot_actuator_off:
            actuator_handler.turnOnActuator()
            print("Actuator re-enabled.")

    def handleChildAlone(self):
        # Send a notification if a child has been alone for too long
        if not self.notification_sent and time.time() - self.timestamp_child_alone > self.timeslot_child_alone:
            mqtt_handler.send_notification(f"A child has been alone in the room for over {self.timeslot_child_alone} seconds!")
            self.notification_sent = True
            print(f"A child has been alone for over {self.timeslot_child_alone}s. Sending notification...")

        # Turn off the actuator if a child is near it
        if actuator_handler.actuator_is_on and ultrasonic_handler.actuator_detected:
            actuator_handler.turnOffActuator()
            self.updateTimestampActuator()
            mqtt_handler.send_notification("An appliance has been disabled for safety.")
            print("A child alone in the room has approached a plug. Turning it OFF...")

# Create an instance of the Main class and start monitoring
main_instance = Main()

while True:
    main_instance.getCurrentStatusDoor()
    main_instance.getCurrentStatusRoom()
    main_instance.actuate()
    time.sleep(0.001)  # Reduce CPU usage while allowing data to be updated
