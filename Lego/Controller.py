import redis


class Controller:
    my_state = None
    color_detected = None
    distance_detected = None

    def __init__(self):
        self.my_state = "Running"
        self.color_detected = "NONE"
        self.distance_detected = 0

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

    def send_data(self, R: redis.Redis, topic: str, my_key, value):
        R.set(my_key, value)
        R.publish(topic, my_key)

    def act(self):
        if self.my_state == "Stopped":
            if self.color_detected == "GREEN" and self.distance_detected > 100:
                self.my_state = "Running"
                self.send_data(R, "commands", "Motor_Status", "Ahead")
        if self.my_state == "Running":
            if self.color_detected == "RED" or self.distance_detected < 100:
                self.my_state = "Stopped"
                self.send_data(R, "commands", "Motor_Status", "Stop")
        print(self.color_detected)
        print(self.distance_detected)
        print(self.my_state)


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
