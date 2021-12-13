import logging
import re
import time

import redis
from time import sleep

import Utilities.RedisHelper as RH
import Utilities.LoggerHelper as LH

from MyRobot import MyRobot

MAX_SPEED = 1500


class PhysicalBody:
    Robot = None

    def __init__(self):
        self.Robot = MyRobot()

    def get_distance(self):
        reader = self.Robot.stato_sensori()
        data = []
        for row in reader:
            data.append(re.findall(r'\d+', str(row))[4])
        return data[0]

    def go_forward(self):
        self.Robot.avanti(MAX_SPEED)

    def stop(self):
        self.Robot.stop_motori()

    def go_backward(self):
        self.Robot.avanti(-MAX_SPEED)


if __name__ == "__main__":
    Logger = LH.get_complete_logger("Freenove.txt")
    Logger.info("This is the logging for the lego body")
    REDIS_HOST = "127.0.0.1"  # TODO
    REDIS_PORT = 6379

    try:
        R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        Logger.info("connected to redis server")
        B = PhysicalBody()
        pubsub = R.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe("commands")

        while True:
            msg = pubsub.get_message()
            if msg:
                instruction = R.get(msg["data"])
                Logger.info(f"Reading Data... Got {instruction}")
            else:
                instruction = None

            if instruction == "Ahead":
                B.go_forward()
                Logger.info("Brick Going Forward")
            if instruction == "Stop":
                B.stop()
                Logger.info("Brick Motors Stopping")
            if instruction == "Backward":
                B.go_backward()
                logging.info("Brick Going Back")

            Logger.info(f"Sending sensors data to Redis: {B.get_distance()}")
            RH.send_data(R, "sensors", "distance_sensor", B.get_distance())

            sleep(1)

    except Exception as e:
        Logger.critical("The REDIS server is not available, trying again soon")
        print(e)
        time.sleep(3)
