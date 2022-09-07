#!/usr/bin/env python

import json
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable
import logging
import time
import os
import tweepy
from dotenv import load_dotenv
from tweepy import Client, StreamingClient

load_dotenv(".env")

logger = logging.getLogger(__name__)
# TO-DO: create a way to take in args during start of application

# kafka topic 
TOPIC_NAME = 'disasters'

# User level auth creds
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
# App level auth creds
BEARER_TOKEN = os.environ.get('API_BEARER_TOKEN')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')


class TweetStreamer(StreamingClient):
    """Streams data from twitter v2 api and sends tweet to kafka topic"""

    def __init__(self, kafka_producer, bearer_token, topic, **kwargs):

        super().__init__(bearer_token, **kwargs)
        self.producer = kafka_producer
        self.bearer_token = bearer_token
        self.topic = topic

    def on_tweet(self, tweet):
        print(f"Full tweet: {tweet}")
        print(f"Tweet ID: {tweet.id}, Tweet: {tweet.text}")

        logger.info("Incoming data: %s", tweet['data'])
        producer = self.producer.get_producer()
        try:
            producer.produce(bytes(json.dumps(tweet['data']), "ascii"))
            time.sleep(0.5)

        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            print(e)
            producer = self.producer.get_producer()
            producer.stop()
            producer.start()
            producer.produce(bytes(json.dumps(tweet['data']), "ascii"))

    def on_exception(self, exception):
        print(exception)
        return True


# Need to create utils module for these.
def generate_rules(screen_names, search_terms, english=True, no_rt=False):
    """Generate rules for input search terms with option to filter for english only and non-retweets."""
    if len(search_terms) == 1:
        rule = search_terms[0]
    else:
        rule = " ".join([str(item) for item in search_terms])
    if screen_names:
        if len(screen_names) == 1:
            rule += f"(from {screen_names[0]})"
        elif len(screen_names) > 1:
            rule += " (from "
            for name in screen_names:
                if screen_names.index(name) != len(screen_names) - 1:
                    rule += name + " OR "
                else:
                    rule += f"{name} )"
        else:
            pass
    if english:
        rule += " lang:en"
    if no_rt:
        rule += " -is:retweet"

    return rule


def start_twitter_stream(kafka_producer, bearer_token, rules):
    """Start streaming tweets from tweepy API and send messages to producer."""

    # initialize client
    streaming_client = TweetStreamer(bearerToken=bearer_token, kafka_producer=kafka_producer)
    # get all current rules
    rule_check_cb(streaming_client)
    streaming_client.add_rules(add=tweepy.StreamRule(value=rules))
    streaming_client.filter()


def rule_check_cb(client):
    """Removes old rules, and institutes current rule"""
    result = client.get_rules()
    rule_ids = []
    if result.data:
        for rule in result.data:
            print(f"rule marked for deletion: {rule.id} - {rule.value}")
            rule_ids.append(rule.id)
        if len(rule_ids) > 0:
            client.delete_rules(rule_ids)
        else:
            print("No rules to delete.")


if __name__ == '__main__':

    # Instantiate kafka client
    k_client = KafkaClient("127.0.0.1:9092")
    kafkaProducer = k_client.topics[bytes(TOPIC_NAME, "utf-8")]
    hashtags = ["#earthquake", "#storm", "#tsunami", "#flooding"]
    search_terms = ["wildfires", "flood"]
    # rules = search_terms[0] + " lang:en -is:retweet"
    new_rules = generate_rules(search_terms=search_terms, english=True, no_rt=True)
    start_twitter_stream(BEARER_TOKEN, kafkaProducer, rules=new_rules)
