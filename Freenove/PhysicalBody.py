
import logging
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D,Motor
from ev3dev2.sensor import INPUT_1,INPUT_4
from ev3dev2.sensor.lego import ColorSensor,UltrasonicSensor

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
    #ev3 = EV3Brick()

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
    logging.basicConfig(filename='controller_logging.txt',
                        level=logging.DEBUG,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("This is the logging for the lego body")
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379

    try:
        R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        logging.info("connected to redis server")
        B = PhysicalBody(INPUT_1, INPUT_4, OUTPUT_A, OUTPUT_D)
        pubsub = R.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe("commands")

        while True:
            msg = pubsub.get_message()
            if msg:
                instruction = R.get(msg["data"])
                logging.info(f"Reading Data... Got {instruction}")
            else:
                instruction = None

            if instruction == "Ahead":
                B.go_forward()
                logging.info("Brick Going Forward")
            if instruction == "Stop":
                B.stop()
                logging.info("Brick Motors Stopping")
            if instruction == "Backward":
                B.go_backward()
                logging.info("Brick Going Back")

            logging.info(f"Sending sensors data to Redis: {B.get_color()},{B.get_distance()}")
            send_data(R, "sensors", "color_sensor", B.get_color())
            send_data(R, "sensors", "distance_sensor", B.get_distance())

            sleep(1)

    except Exception as e:
        logging.critical("The REDIS server is not available, trying again soon")
        print(e)
        time.sleep(3)
