"""
    Produces data and signal to a shared topic channel through redis
"""

import redis
from typing import Dict
from time import sleep

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def send_data(R: redis.Redis, topic : str):
    mykey = "SENSKEY"
    while True:
        R.set(mykey, 1.0)
        R.publish(topic, mykey)
        sleep(1.0)


if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        print("My REDIS server version is: ", R.info()['redis_version'])
        send_data(R, "data_ready")
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
