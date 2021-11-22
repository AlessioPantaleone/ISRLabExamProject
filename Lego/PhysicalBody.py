from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog


class PhysicalBody:
    color_sensor = None
    distance_sensor = None
    motorL = None
    motorR = None
    ev3 = EV3Brick()

    def __init__(self, Color_Port, Distance_Port, MotorL_Port, MotorR_Port):
        self.color_sensor = ColorSensor(Color_Port)
        self.distance_sensor = UltrasonicSensor(Distance_Port)
        self.motorL = Motor(MotorL_Port)
        self.motorR = Motor(MotorR_Port)

    def get_distance(self):
        return self.distance_sensor.distance()

    def get_color(self):
        return self.color_sensor.color()

    def go_forward(self):
        self.motor.dc(15)

    def stop(self):
        self.motor.dc(0)

    def go_backward(self):
        self.motor.dc(-15)


if __name__ == "__main__":
    print("Misura, invia qualcosa al controller e ricevi qualcosa dal controllerr")
