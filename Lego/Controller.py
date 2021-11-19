"""
Controller for the lego EV3 Brick
"""
import redis

"""
Function to send data to redis
@:param R The Redis instance
@:param topic The topic you want to publish to
@:param my_key Name of the key
@:param value Value of the key
"""


def send_data(R: redis.Redis, topic: str, my_key, value):
    R.set(my_key, value)
    R.publish(topic, my_key)


"""
Controller for the lego EV3 Brick
"""


class Controller:
    my_state = None
    color_detected = None
    distance_detected = None

    def __init__(self):
        self.my_state = "Stopped"
        self.color_detected = "NONE"
        self.distance_detected = 0

    """
    Function to constantly listen to a topic from redis
    @:param self the controller that is reading data
    @:param R the Redis instance
    @:param topic the topic you want to listen to
    """
    def read_data(self, R: redis.Redis, topic: str):
        pubsub = R.pubsub()
        pubsub.subscribe(topic)
        for msg in pubsub.listen():
            if msg["type"] == 'message':
                source_name = msg["data"]
                value = R.get(source_name)
                if source_name == "color_sensor":
                    self.color_detected = value
                if source_name == "distance_sensor":
                    self.distance_detected = value
                self.act()

    """
    Function to act based on the belief of the controller
    """
    def act(self):
        print('\nState pre  acting: {} with color = {} and distance = {}'.format(self.my_state,
                                                                              self.color_detected,
                                                                              self.distance_detected))
        if self.my_state == "Stopped":
            if self.color_detected == "GREEN" and int(self.distance_detected) > 100:
                self.my_state = "Running"
                send_data(R, "commands", "Motor_Status", "Ahead")
        if self.my_state == "Running":
            if self.color_detected == "RED" or int(self.distance_detected) < 100:
                self.my_state = "Stopped"
                send_data(R, "commands", "Motor_Status", "Stop")

        print('State post acting: {} with color = {} and distance = {}'.format(self.my_state,
                                                                               self.color_detected,
                                                                               self.distance_detected))


if __name__ == '__main__':
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    C = Controller()

    while True:
        try:
            print("My REDIS server version is: ", R.info()['redis_version'])
            C.read_data(R, "sensors")
        except Exception as e:
            print("The REDIS server is not available")
            print(e)
