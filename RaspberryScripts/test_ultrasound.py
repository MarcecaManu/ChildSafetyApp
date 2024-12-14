from gpiozero import DistanceSensor
ultrasonic = DistanceSensor(echo=23, trigger=22)
while True:
    print(ultrasonic.distance)