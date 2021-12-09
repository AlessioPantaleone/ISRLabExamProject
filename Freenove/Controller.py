import time

import redis
import Utilities.RedisHelper as RH
import Utilities.LoggerHelper as LH


class Controller:
    my_state = None
    front_distance_detected = 0

    def __init__(self):
        self.my_state = "Stopped"
        self.front_distance_detected = 0

    def update_belief_state(self, newdata):
        Logger.info("Updating belief state")
        if newdata[0] == "distance_sensor":
            Logger.critical(f"Updating Distance Sensor, NewData = {newdata[1]}")
            self.front_distance_detected = newdata[1]
        if newdata[0] == 0:
            Logger.info("No new sensor data")

    def act(self):
        if self.my_state == "Stopped" and int(self.front_distance_detected) > 100:
            Logger.info("Taking action to start motors")
            self.my_state = "Running"
            RH.send_data(R, "commands", "Motor_Status", "Ahead")
        if self.my_state == "Backing" and int(self.front_distance_detected) > 100:
            Logger.info("Taking action to go ahead again")
            self.my_state = "Running"
            RH.send_data(R, "commands", "Motor_Status", "Ahead")
        if self.my_state == "Running" and int(self.front_distance_detected) < 100:
            Logger.info("Taking action to go back")
            self.my_state = "Backing"
            RH.send_data(R, "commands", "Motor_Status", "Backward")
        time.sleep(1)


if __name__ == '__main__':

    Logger = LH.get_complete_logger("Freenove.txt")
    Logger.info("This is the logging for the Freenove controller")
    C = Controller()

    try:
        REDIS_HOST = "127.0.0.1"
        REDIS_PORT = 6379
        R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        Logger.info("connected to redis server")
        pubsub = R.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe("sensors")
        while True:
            try:
                C.act()
                newdata = RH.read_data_from_pubsub(R, pubsub)
                C.update_belief_state(newdata)
            except Exception as e:
                Logger.critical(f" {e} An error occurred")
                print(e.with_traceback())
                time.sleep(3)
    except Exception as e:
        Logger.critical("The REDIS server is not available")
        time.sleep(3)


