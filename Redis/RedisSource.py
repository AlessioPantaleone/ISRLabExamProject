"""
    Redis Explorer will
    Reads from a REDIS server the full set of keys, query for each key its type
    and makes a copy in the Python memory space
"""
import time

import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379

if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        i = 1
        while 1:
            data = R.lpush("TOPIC1", i)
            i = i + 1
            time.sleep(3)
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
