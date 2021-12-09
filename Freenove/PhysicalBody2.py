import logging
import re
import time

import redis
from time import sleep

from MyRobot import MyRobot

MAX_SPEED = 1500


def send_data(R: redis.Redis, topic: str, my_key, value):
    logging.info(f"Sending data to redis Topic: {topic} , Key:{my_key}, Value:{value}")
    R.set(my_key, value)
    R.publish(topic, my_key)


class PhysicalBody:
    Robot = None

    def __init__(self):
        self.Robot = MyRobot()

    def get_distance(self):
        reader = self.Robot.stato_sensori()  # TODO Adapt Robot symbols
        data = []
        for row in reader:
            data.append(re.findall(r'\d+', str(row))[4])
        return data[0]

    def go_forward(self):
        self.Robot.avanti(MAX_SPEED)  # TODO Adapt Robot symbols

    def stop(self):
        self.Robot.stop_motori()  # TODO Adapt Robot symbols

    def go_backward(self):
        self.Robot.avanti(-MAX_SPEED)  # TODO Adapt Robot symbols


if __name__ == "__main__":
    REDIS_HOST = "127.0.0.1"  # TODO
    REDIS_PORT = 6379

    try:
        R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        B = PhysicalBody()
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
            if instruction == "Backward":
                B.go_backward()
                logging.info("Brick Going Back")

            send_data(R, "sensors", "distance_sensor", B.get_distance())

            sleep(1)

    except Exception as e:
        print(e)
        time.sleep(3)
