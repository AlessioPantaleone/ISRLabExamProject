import logging
from CsimApi.pycsim import CSim, common
import time

import redis
from time import sleep

import Utilities.RedisHelper as RH
import Utilities.LoggerHelper as LH


MAX_SPEED = 1500


class PhysicalBody:
    def __init__(self, api: CSim):
        self._api = api
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")

        self._front_sensor = api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor4")

        self._left_sensor = api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor3")
        self._right_sensor = api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor6")

    def _set_two_motor(self, left: float, right: float):
        self._right_motor.set_target_velocity(right)
        self._left_motor.set_target_velocity(left)

    def go_forward(self, speed=0.5):
        self._set_two_motor(speed, speed)

    def go_backward(self, speed=0.5):
        self._set_two_motor(-speed, -speed)

    def stop(self):
        self._set_two_motor(0, 0)

    def get_front_distance(self):
        return self._front_sensor.read()[1].distance()

"""
    def rotate_right(self, speed=2.0):
        self._set_two_motor(speed, -speed)

    def rotate_left(self, speed=2.0):
        self._set_two_motor(-speed, speed)

    def right_length(self):
        return self._right_sensor.read()[1].distance()

    def left_length(self):
        return self._left_sensor.read()[1].distance()
"""

if __name__ == "__main__":
    Logger = LH.get_complete_logger("Pioneer.txt")
    Logger.info("This is the logging for the lego body")
    REDIS_HOST = "localhost"  # TODO
    REDIS_PORT = 6379

    with CSim.connect("127.0.0.1", 19997) as api:
        # api.simulation.start()
        try:
            B = PhysicalBody(api)
            B.stop()
            R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            Logger.info("connected to redis server")
            pubsub = R.pubsub(ignore_subscribe_messages=True)
            pubsub.subscribe("commands")
        except common.NotFoundComponentError as e:
            print(e)
            print("Have you opened the right scene inside Coppelia SIM?")
            exit(-1)
        try:
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

                Logger.info(f"Sending sensors data to Redis: {B.get_front_distance()}")
                RH.send_data(R, "sensors", "distance_sensor", B.get_front_distance())

                sleep(0.1)

        except Exception as e:
            Logger.critical("The REDIS server is not available, trying again soon")
            print(e)
            time.sleep(3)
