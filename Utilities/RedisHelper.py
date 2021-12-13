import re

import redis
import logging


def send_data(R: redis.Redis, topic: str, my_key, value):
    logging.info(f"Sending data to redis Topic: {topic} , Key:{my_key}, Value:{value}")
    R.set(my_key, value)
    R.publish(topic, my_key)


def read_data_from_pubsub(R: redis.Redis, pubsub):
    msg = pubsub.get_message()
    if msg:
        source_name = msg["data"]
        value = R.get(source_name)
        return [source_name, value]
    else:
        return [0, 0]


def listen_for_data(R: redis.Redis, topic):
    pubsub = R.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(topic)
    for msg in pubsub.listen():
        if msg["type"] == 'message':
            source_name = msg["data"]
            value = R.get(source_name)
            return [source_name, value]

