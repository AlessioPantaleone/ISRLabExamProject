import redis
from typing import Dict
from time import sleep

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def send_data(R: redis.Redis, topic: str, my_key, value):
    R.set(my_key, value)
    R.publish(topic, my_key)


def send_gimmik_data():
    send_data(R, "sensors", "distance_sensor", "150")
    send_data(R, "sensors", "color_sensor", "GREEN")
    sleep(3)
    send_data(R, "sensors", "distance_sensor", "150")
    send_data(R, "sensors", "color_sensor", "RED")
    sleep(3)
    send_data(R, "sensors", "distance_sensor", "150")
    send_data(R, "sensors", "color_sensor", "GREEN")
    sleep(3)
    send_data(R, "sensors", "distance_sensor", "50")
    send_data(R, "sensors", "color_sensor", "GREEN")
    sleep(3)
    send_data(R, "sensors", "distance_sensor", "50")
    send_data(R, "sensors", "color_sensor", "RED")
    sleep(3)
    send_data(R, "sensors", "distance_sensor", "150")
    send_data(R, "sensors", "color_sensor", "GREEN")


def send_gimmik_commands():
    send_data(R, "commands", "motor_status", "Ahead")
    send_data(R, "commands", "motor_status", "Stop")


if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print("My REDIS server version is: ", R.info()['redis_version'])
    try:
        send_gimmik_data()
        send_gimmik_commands()
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
