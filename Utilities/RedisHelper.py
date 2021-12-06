import re

import redis
import logging


def send_data(R: redis.Redis, topic: str, my_key, value):
    logging.info(f"Sending data to redis Topic: {topic} , Key:{my_key}, Value:{value}")
    R.set(my_key, value)
    R.publish(topic, my_key)


def read_data_from_topic(R: redis.Redis, topic: str):
    pubsub = R.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(topic)

    msg = pubsub.get_message()
    if msg:
        source_name = msg["data"]
        value = R.get(source_name)
        return [R.get(source_name), value]
    else:
        return [0, 0]
