"""
    Redis Explorer will
    Reads from a REDIS server the full set of keys, query for each key its type
    and makes a copy in the Python memory space
"""

import redis
from typing import Dict

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def redis_explorer(R: redis.Redis) -> Dict:
    """
    :param R: redis server handler
    :return: dictionary of the discovered keys
    """
    out = {}
    keys = R.keys()
    out['number_of_keys'] = len(keys)
    out['keys'] = set()
    for k in keys:
        out['keys'].add(k)
        pk = f'k:{k}'
        out[pk] = {}
        out[pk]['type'] = R.type(k)
        match out[pk]['type']:
            case 'string':
                out[pk]['value'] = R.get(k)
            case 'set':
                out[pk]['value'] = R.smembers(k)
            case 'list':
                out[pk]['value'] = R.lrange(k, 0, -1)
            case 'hash':
                out[pk]['value'] = R.hgetall(k)
    return out


if __name__ == '__main__':
    R = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        print("My REDIS server version is: ", R.info()['redis_version'])
        database = redis_explorer(R)
        for key in database:
            print(key, type(key), database[key])
    except Exception as e:
        print("The REDIS server is not available")
        print(e)
