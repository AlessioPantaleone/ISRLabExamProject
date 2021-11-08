"""
    Program 1 from exercise_redis.md
    SOURCE
"""
import random
import redis
import time

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def source(R: redis.Redis):
    values = "VALUES"
    while True:
        rand = random.uniform(1.0, 100.0) # random float between 1.0 and 100.0
        R.rpush(values, rand)
        time.sleep(1)


if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        print("My REDIS server version is: ", R.info()['redis_version'])
        source(R)
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
