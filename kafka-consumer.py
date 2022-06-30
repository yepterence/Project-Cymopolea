from kafka3 import KafkaConsumer
import json
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    consumer = KafkaConsumer(
        'market_news',
        bootstrap_servers = ['localhost:9092'],
        auto_offset_reset='earliest',
        max_poll_records = 100,
        value_deserializer=(lambda v: json.dumps(v).encode('utf-8'))
    )
    # load messages from json
    for message in consumer:
        tweets = json.loads(json.dumps(message.value))
