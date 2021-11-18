import time
import pybricks
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# def color_parser():
# def distance_parser():


if __name__ == "__main__":

    # Import the lego robot
    # Set up the Color Sensor.  It is used to detect the red beam when the
    # neck has moved to its maximum position.
    # Create your objects here.
    ev3 = EV3Brick()
    color_sensor = ColorSensor(Port.S1)
    distance_sensor = UltrasonicSensor(Port.S2)
    while True:
        time.sleep(5)
        print(time.time())
        print("Sensed Color: ")
        print(color_sensor.color())
        print("Sensed Distance: ")
        print(distance_sensor.distance())
        print("////////////////////")

        if color_sensor.color() == Color.RED and distance_sensor.distance() < 100:
            ev3.speaker.say("Rosso vicino")
            # little horn noise
        if color_sensor.color() == Color.GREEN and distance_sensor.distance() >= 100:
            ev3.speaker.say("Verde Lontano")
            # big horn noise
