import time

import redis
import Utilities.RedisHelper as RH
import Utilities.LoggerHelper as LH


class Controller:
    my_state = None
    front_distance_detected = 0

    def __init__(self):
        self.my_state = "Stopped"
        self.distance_detected = 0

    def update_belief_state(self):
        Logger.info("Updating belief state")
        newdata = RH.read_data_from_topic(R, "sensors")
        if newdata[0] == "distance_sensor":
            Logger.info(f"Updating Distance Sensor, NewData = {newdata[1]}")
            self.distance_detected = newdata[1]
        if newdata[0] == 0:
            Logger.info("No new sensor data")

    def act(self):
        Logger.debug("Acting")
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

        Logger.debug("No Action Taken")
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
    except Exception as e:
        Logger.critical("The REDIS server is not available")
        time.sleep(3)

    while True:
        try:
            C.act()
            C.update_belief_state()
        except Exception as e:
            Logger.critical(f" {e} An error occurred")
            print(e.with_traceback())
            time.sleep(3)
