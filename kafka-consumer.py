#!/usr/bin/env python

# from kafka3 import KafkaConsumer
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json
import logging

from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

TOPIC = 'natural_disasters'
logger = logging.getLogger(__name__)
BOOTSTRAP_SERVERS = ['localhost:9092']


if __name__ == '__main__':
    client = KafkaClient(hosts=BOOTSTRAP_SERVERS[0])
    topic = client.topics[TOPIC]
    consumer = topic.get_simple_consumer(
        consumer_group="nat_disaster",
        auto_offset_reset=OffsetType.EARLIEST,
        reset_offset_on_start=False,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    try:
        consumer.consume()
    except (SocketDisconnectedError, LeaderNotAvailable) as e:
        print(e)
        consumer.stop()
        consumer.start()
