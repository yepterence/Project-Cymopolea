#!/usr/bin/env python3

import json
import logging
import datetime
import os
import tweepy
from tweepy import StreamingClient
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

logger = logging.getLogger(__name__)
# TO-DO: create a way to take in args during start of application

# kafka topic 
TOPIC_NAME = 'natural_disasters'

# User level auth creds
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
# App level auth creds
BEARER_TOKEN = os.environ.get('API_BEARER_TOKEN')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')


class TweetStreamer(StreamingClient):
    """Streams data from twitter v2 api and sends tweet to kafka topic"""
    def __init__(self, bearer_token, topic):
        super().__init__(bearer_token)
        client = KafkaClient('127.0.0.1:9092')
        self.topic = client.topics[topic]

    def on_tweet(self, tweet):
        payload = {'tweet_id': tweet.id,
                   'tweet_text': tweet.text,
                   'location': tweet.geo,
                   'author_id': tweet.author_id
                   }
        print(f"New tweet received: {payload}")
        bytes_payload = json.dumps(payload).encode('utf-8')
        with self.topic.get_producer() as producer:
            try:
                producer.produce(bytes_payload)
            except Exception as e:
                print("An Error Occurred: %s", e)
                self.topic.get_producer()
                producer.stop()
                producer.start()
                producer.produce(bytes_payload)

    def on_request_error(self, status_code):
        print(f"A request issue was encountered with code: {status_code}")
        self.disconnect()


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
                if screen_names.index(name) < len(screen_names):
                    rule += name + " OR "
                else:
                    rule += f"{name} )"
        else:
            pass
        rule += " lang:en" if english else ""
        rule += " -is:retweet" if no_rt else ""

    return rule


def start_twitter_stream(bearer_token, rules):
    """Start streaming tweets from tweepy API and send messages to producer."""

    # initialize client
    streaming_client = TweetStreamer(bearer_token=bearer_token, topic=TOPIC_NAME)
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
    hashtags = ["#earthquake", "#storm", "#tsunami", "#flooding"]
    search_terms = ["wildfires", "flood"]
    # rules = search_terms[0] + " lang:en -is:retweet"
    new_rules = generate_rules(screen_names=None, search_terms=search_terms, english=True, no_rt=True)
    start_twitter_stream(BEARER_TOKEN, rules=new_rules)
