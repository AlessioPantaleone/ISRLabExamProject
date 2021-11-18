"""
    Consumer of data coming from a redis message broker
"""

import redis
from typing import Dict
from time import sleep

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def read_data(R : redis.Redis, topic : str):
    pubsub = R.pubsub()
    pubsub.subscribe(topic)
    for msg in pubsub.listen():
        if msg["type"] == 'message':
            source_name = msg["data"]
            value = R.get(source_name)
            print(source_name, value)



if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        print("My REDIS server version is: ", R.info()['redis_version'])
        read_data(R, "data_ready")
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
