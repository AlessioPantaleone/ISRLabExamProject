import time
from datetime import datetime
from random import randrange
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379

if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        while 1:
            data = datetime.now().__str__()
            R.lpush("ExerciseList1", data)
            time.sleep((randrange(5)))
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
