import random
from  random import randint

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
import redis
from time import sleep

def send_data(R: redis.Redis, topic: str, my_key, value):
    R.set(my_key, value)
    R.publish(topic, my_key)


def read_data_from_pubsub( pubsub , topic: str):
    msg = pubsub.get_message()
    if msg:
        return msg["data"]


class PhysicalBody:
    color_sensor = None
    distance_sensor = None
    motorL = None
    motorR = None
    ev3 = EV3Brick()

    def __init__(self, Color_Port, Distance_Port, MotorL_Port, MotorR_Port):
        color_sensor = 1

    def get_distance(self):
        return 50

    def get_color(self):
        return "RED"

    def go_forward(self):
        print("Vai Avanti")

    def stop(self):
        print("Stoppati")


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

        random = randint(1, 4)
        if random == 1:
            send_data(R, "sensors", "color_sensor", "GREEN")
            send_data(R, "sensors", "distance_sensor", "150")
        if random == 2:
            send_data(R, "sensors", "color_sensor", "GREEN")
            send_data(R, "sensors", "distance_sensor", "50")
        if random == 3:
            send_data(R, "sensors", "color_sensor", "RED")
            send_data(R, "sensors", "distance_sensor", "150")
        if random == 4:
            send_data(R, "sensors", "color_sensor", "RED")
            send_data(R, "sensors", "distance_sensor", "50")
        sleep(1)

