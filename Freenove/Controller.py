import time

import redis
import logging


def send_data(R: redis.Redis, topic: str, my_key, value):
    logging.info(f"Sending data to redis Topic: {topic} , Key:{my_key}, Value:{value}")
    R.set(my_key, value)
    R.publish(topic, my_key)


class Controller:
    my_state = None
    color_detected = None
    distance_detected = None

    def __init__(self):
        self.my_state = "Stopped"
        self.color_detected = "NONE"
        self.distance_detected = 0

    def read_data(self, R: redis.Redis, topic: str):
        pubsub = R.pubsub()
        pubsub.subscribe(topic)
        for msg in pubsub.listen():
            if msg["type"] == 'message':
                source_name = msg["data"]
                value = R.get(source_name)
                logging.info(f"New message received: key:{source_name} value:{value}")
                if source_name == "color_sensor":
                    self.color_detected = value
                    if value != self.color_detected:
                        logging.info("Belief state updated with new color")
                        self.color_detected = value
                        self.act()
                if source_name == "distance_sensor":
                    if value != self.distance_detected:
                        logging.info("Belief state updated with new distance")
                        self.distance_detected = value
                        self.act()

    def act(self):
        if self.my_state == "Stopped":
            if self.color_detected == "Green" and int(self.distance_detected) > 100:
                logging.info("Taking action to start motors")
                self.my_state = "Running"
                send_data(R, "commands", "Motor_Status", "Ahead")
            if self.color_detected == "Green" and int(self.distance_detected) < 100:
                logging.info("Taking action to start backward motors")
                self.my_state = "Backing"
                send_data(R, "commands", "Motor_Status", "Backward")
        if self.my_state == "Running" or self.my_state == "Backing":
            if self.color_detected == "Red" or int(self.distance_detected) < 100:
                logging.info("Taking actions to stop motors")
                self.my_state = "Stopped"
                send_data(R, "commands", "Motor_Status", "Stop")


if __name__ == '__main__':
    logging.basicConfig(filename='controller_logging.txt',
                        level=logging.DEBUG,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("This is the logging for the lego controller")
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    C = Controller()

    while True:
        try:
            logging.info("connected to redis server")
            C.read_data(R, "sensors")
        except Exception as e:
            logging.critical("The REDIS server is not available, trying again soon")
            print(e)
            time.sleep(3)
