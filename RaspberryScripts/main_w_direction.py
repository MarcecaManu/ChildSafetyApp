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

    timeslot_child_alone = 60    # 1 minute
    timeslot_actuator_off = 10
    notification_sent = False

    def __init__(self):
        self.children_in_room = 0
        self.adults_in_room = 0
        self.entering = None


        # Timeslot values (in seconds)
        self.timeslot_door_sensors = 0.5
        self.timeslot_pir = 30

        # Statuses
        self.previous_status = self.FREE
        self.door_status = self.FREE

        # Timestamps
        self.timestamp_door = time.time()
        self.timestamp_direction = time.time()
        self.timestamp_child_alone = time.time()
        self.timestamp_pir = time.time()
        self.timestamp_actuator = time.time()

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

    def childrenAlone(self):
        return self.children_in_room > 0 and self.adults_in_room == 0

    def getCurrentStatusDoor(self):
        if self.door_status == self.FREE:
            if ultrasonic_handler.lower_detected:
                self.door_status = self.CHECK_LOW
                self.updateTimestampDoor()
            elif ultrasonic_handler.higher_detected:
                self.door_status = self.CHECK_HIGH
                self.updateTimestampDoor()
            elif ultrasonic_handler.direction_detected:
                self.entering = True
                self.updateTimestampDirection()

        if self.door_status in [self.CHECK_LOW, self.CHECK_HIGH]:
            self.checkDoor()
            if self.entering == None:
                self.entering = False
            self.updateTimestampDirection()

        if self.door_status in [self.OCCUPIED_CHILD, self.OCCUPIED_ADULT]:
            if not ultrasonic_handler.lower_detected and not ultrasonic_handler.higher_detected:
                self.door_status = self.FREE
                


        # Debugging output
        if self.previous_status != self.door_status:
            print(self.door_status)

    def checkDoor(self):
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

        current_status_child = self.children_in_room
        current_status_adult = self.adults_in_room

        
        if self.door_status == self.FREE:
            if self.previous_status == self.OCCUPIED_CHILD:
                if self.entering == True:
                    self.children_in_room += 1
                else:
                    self.children_in_room -= 1
                    if self.children_in_room < 0:
                        self.children_in_room = 0
                self.entering = None
                self.updateTimestampPir()
                # if self.child_in_room:
                #     print("A child is in the room")
                # else:
                #     print("No children in this room")
            elif self.previous_status == self.OCCUPIED_ADULT:
                if self.entering == True:
                    self.adults_in_room += 1
                else:
                    self.adults_in_room -= 1
                    if self.adults_in_room < 0:
                        self.adults_in_room = 0
                self.entering = None
                self.updateTimestampPir()
                # if self.adult_in_room:
                #     print("An adult is in the room")
                # else:
                #     print("No adults in this room")
            elif self.previous_status == self.FREE:
                if self.entering != None and time.time() - self.timestamp_direction > self.timeslot_door_sensors:
                    self.entering = None



        if self.adults_in_room > 0 or self.children_in_room > 0:
            if pir_handler.motion_detected:
                self.updateTimestampPir()
            elif time.time() - self.timestamp_pir > self.timeslot_pir:
                # No motion detected for a bit. Assume the room is empty
                print("No motion detected for " + str(self.timeslot_pir) + "s. Assuming the room is empty.")
                self.adults_in_room = 0
                self.children_in_room = 0
                

        
        if current_status_adult > self.adults_in_room:
            print("An adult has left the room")
            self.printStatus()
        elif current_status_adult < self.adults_in_room:
            print("An adult has entered the room")
            self.printStatus()
        
        if current_status_child > self.children_in_room:
            print("A child has left the room")
            self.printStatus()

        elif current_status_child < self.children_in_room:
            print("A child has entered the room")
            self.printStatus()
        
        self.previous_status = self.door_status

    def printStatus(self):
        print("Adults: " + str(self.adults_in_room) + " | Children: " + str(self.children_in_room))


    def actuate(self):
        if self.childrenAlone():
            if not self.notification_sent and time.time() - self.timestamp_child_alone > self.timeslot_child_alone:
                # Send notification
                mqtt_handler.send_notification("A child has been alone in the room for over " + str(self.timeslot_child_alone) + " seconds!")

                self.notification_sent = True 
                print("A child has been alone for more than " + str(self.timeslot_child_alone) + "s. Sending notification...")
            
            # Check for anything close to the actuator sensor and disable it eventually
            if actuator_handler.actuator_is_on and ultrasonic_handler.actuator_detected:            #Implement PIRSensor as well
                actuator_handler.turnOffActuator()
                self.updateTimestampActuator()

               # Send notification
                mqtt_handler.send_notification("An appliance has been disabled for safety.")


                #debug 
                print("A child alone in the room has got close to a plug. Turning it OFF...")
                
        elif not actuator_handler.actuator_is_on and  not self.childrenAlone() and time.time() - self.timestamp_actuator > self.timeslot_actuator_off:

            #debug
            print(str(self.timeslot_actuator_off) + "s have passed. Turning actuator back ON...")

            # NOTE!! Reenable the plug when an adult comes in?
            actuator_handler.turnOnActuator()
            print("Actuator re-enabled.")

        else: 
            self.notification_sent = False
            self.updateTimestampChild()



# Create an instance of the Main class
main_instance = Main()

while True:
    main_instance.getCurrentStatusDoor()
    main_instance.getCurrentStatusRoom()
    main_instance.actuate()
    time.sleep(0.001)  # Reduce CPU usage while allowing data to be updated
