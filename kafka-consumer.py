#!/usr/bin/env python

from kafka3 import KafkaConsumer
import json
import logging

TOPIC = 'market_news'
logger = logging.getLogger(__name__)
BOOTSTRAP_SERVERS = ['localhost:9092']
if __name__ == '__main__':
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        max_poll_records=100,
        value_deserializer=(lambda v: json.loads(v.decode('ascii')))
    )
    # load messages from json
    consumer.subscribe([TOPIC])
    if consumer.bootstrap_connected():
        print(f"Connection with Producer Established on {BOOTSTRAP_SERVERS}")
        try:
            while True:
                msg = consumer.poll(1.0)
                if not msg:
                    print("No messages. Consumer waiting..")
                elif msg:
                    print("Incoming message: %s", msg)
        except Exception as e:
            print(f"An Error Occurred: {e}")

