import time
from pirSensor import pir_handler
from ultrasonicHandler import ultrasonic_handler
from actuatorHandler import actuator_handler

class Main:
    # Class-level attributes for better readability
    FREE = "FREE"                    # No one's at the door
    CHECK_LOW = "CHECK_LOW"          # LOWER sensor has been triggered, waiting for the other sensor
    CHECK_HIGH = "CHECK_HIGH"        # HIGHER sensor has been triggered, waiting for the other sensor
    OCCUPIED_CHILD = "OCCUPIED_CHILD"  # Child detected passing through the door
    OCCUPIED_ADULT = "OCCUPIED_ADULT"  # Adult detected passing through the door

    timeslot_child_alone = 60     # 1 minute
    timeslot_actuator_off = 10
    notification_sent = False

    def __init__(self):
        self.child_in_room = False
        self.adult_in_room = False

        # Timeslot values (in seconds)
        self.timeslot_both_sensors = 0.5

        self.previous_status = self.FREE
        self.status = self.FREE

        self.timestamp = time.time()
        self.timestamp_child_alone = time.time()
        self.timestamp_actuator = time.time()

    def updateTimestampDoor(self):
        self.timestamp = time.time()

    def updateTimestampChild(self):
        self.timestamp_child_alone = time.time()

    def updateTimestampActuator(self):
        self.timestamp_actuator = time.time()

    def getCurrentStatusDoor(self):
        if self.status == self.FREE:
            if ultrasonic_handler.lower_detected:
                self.status = self.CHECK_LOW
                self.updateTimestampDoor()
            elif ultrasonic_handler.higher_detected:
                self.status = self.CHECK_HIGH
                self.updateTimestampDoor()

        if self.status in [self.CHECK_LOW, self.CHECK_HIGH]:
            if time.time() - self.timestamp < self.timeslot_both_sensors:
                if self.status == self.CHECK_LOW and ultrasonic_handler.higher_detected:
                    self.status = self.OCCUPIED_ADULT
                elif self.status == self.CHECK_HIGH and ultrasonic_handler.lower_detected:
                    self.status = self.OCCUPIED_ADULT
            else:
                if self.status == self.CHECK_HIGH:
                    self.status = self.FREE
                else:
                    self.status = self.OCCUPIED_CHILD

        if self.status in [self.OCCUPIED_CHILD, self.OCCUPIED_ADULT]:
            if not ultrasonic_handler.lower_detected and not ultrasonic_handler.higher_detected:
                self.status = self.FREE

        # Debugging output
        if self.previous_status != self.status:
            print(self.status)
            


    def getCurrentStatusRoom(self):

        current_status_child = self.child_in_room
        current_status_adult = self.adult_in_room

        
        if self.status == self.FREE:
            if self.previous_status == self.OCCUPIED_CHILD:
                self.child_in_room = not self.child_in_room
                # if self.child_in_room:
                #     print("A child is in the room")
                # else:
                #     print("No children in this room")
            elif self.previous_status == self.OCCUPIED_ADULT:
                self.adult_in_room = not self.adult_in_room
                # if self.adult_in_room:
                #     print("An adult is in the room")
                # else:
                #     print("No adults in this room")


            

        
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

        self.previous_status = self.status

    def actuate(self):
        if self.child_in_room and not self.adult_in_room:
            if not self.notification_sent and time.time() - self.timestamp_child_alone > self.timeslot_child_alone:
                # Send notification
                # [............]

                self.notification_sent = True 
                print("A child has been alone for more than one minute. Sending notification...")
            
            # Check for anything close to the actuator sensor and disable it eventually
            if ultrasonic_handler.actuator_detected:            #Implement PIRSensor as well
                actuator_handler.turnOffActuator()
                self.updateTimestampActuator()

                #debug 
                print("A child alone in the room has got close to a plug. Turning it OFF...")
            elif time.time() - self.timestamp_actuator > self.timeslot_actuator_off:

                # NOTE!! Reenable the plug when an adult comes in?
                actuator_handler.turnOnActuator()
                
                #debug
                print("Turning actuator back ON...")
        else: 
            self.notification_sent = False
            self.updateTimestampChild()



# Create an instance of the Main class
main_instance = Main()

while True:
    main_instance.getCurrentStatusDoor()
    main_instance.getCurrentStatusRoom()
    
    time.sleep(0.001)  # Reduce CPU usage while allowing data to be updated
