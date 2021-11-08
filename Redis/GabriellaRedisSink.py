""""
    Program 2 from exercise_redis.md
    SINK
"""
import random
import redis
import time

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def sink(R: redis.Redis):
    values = "VALUES"
    while True:
        value = R.rpop(values)
        print(value)
        time.sleep(5)


if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        # print("My REDIS server version is: ", R.info()['redis_version'])
        sink(R)
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
