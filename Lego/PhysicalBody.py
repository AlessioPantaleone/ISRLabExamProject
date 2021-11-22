from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
import redis
from time import sleep


def send_data(R: redis.Redis, topic: str, my_key, value):
    R.set(my_key, value)
    R.publish(topic, my_key)


def read_data(R: redis.Redis, topic: str):
    pubsub = R.pubsub()
    pubsub.subscribe(topic)
    for msg in pubsub.get_message():
        if msg["type"] == 'message':
            source_name = msg["data"]
            return R.get(source_name)


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
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print("My REDIS server version is: ", R.info()['redis_version'])
    B = PhysicalBody(Port.S1, Port.S2, Port.A, Port.B)
    pubsub = R.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("commands")

    while True:
        msg = pubsub.get_message()
        if msg:
            instruction = R.get(msg["data"])
        else:
            instruction = None

        if instruction == "Ahead":
            B.go_forward()
        if instruction == "Stop":
            B.stop()

        send_data(R, "sensors", "color_sensor", B.get_color())
        send_data(R, "sensors", "distance_sensor", B.get_distance())

        sleep(1)
