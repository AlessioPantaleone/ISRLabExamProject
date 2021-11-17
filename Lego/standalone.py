import time
import pybricks
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

def color_parser():
    ...
def distance_parser():
    ...


if __name__ == "__main__":

    #Import the lego robot

    while 1:
        #read sensors
        sensed_color = color_parser()
        sensed_distance = distance_parser()

        if (sensed_color == "green" and sensed_distance == "near"):
            ...
            # little horn noise
        if (sensed_color == "red" and sensed_distance == "far"):
            ...
            # big horn noise