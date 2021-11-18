from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
class PhysicalBody:
    color_sensor= None
    distance_sensor= None
    motor= None
    ev3 = EV3Brick()
    def __init__(self, Color_Port, Distance_Port, Motor_Port):
        self.color_sensor = ColorSensor(Color_Port)
        self.distance_sensor = UltrasonicSensor(Distance_Port)
        self.motor= Motor(Motor_Port)
    def getDistance(self):
        return self.distance_sensor.distance()
    def getColor(self):
        return self.color_sensor.Color()
    def goForward(self):
        self.motor.dc(15)
    def stop(self):
        self.motor.dc(10)
    def goBackward(self):
        self.motor.dc(-15)
