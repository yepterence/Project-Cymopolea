import json 
from kafka3 import KafkaClient, KafkaProducer
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
TOPIC_NAME = 'market_news'

# User level auth creds
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
# App level auth creds
BEARER_TOKEN = os.environ.get('API_BEARER_TOKEN')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

# TO-DO: Calculate no of tweets and the %age change in price 
# Scrape and dump data to S3

client = Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
auth = tweepy.OAuth1UserHandler(ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

# Instantiate kafka client
kafka_client = KafkaClient(bootstrap_servers=["localhost:9092"])
producer = KafkaProducer(bootstrap_servers=["localhost:9092"], max_poll_records=1500)


class TweetStreamer(StreamingClient):

    def on_connect(self):
        logger.info("Connection established")
        return True

    def on_tweet(self, tweet):
        if tweet.referenced_tweets == None:
            print(tweet.text)
            time.sleep(2)
         
    def on_status(self, data):
        logger.info(data)
        producer.send(TOPIC_NAME, json.dumps())
        return True
    
    def on_limit(self,status_code):
        logger.warn("Twitter API Rate limit reached, pausing stream for 15 minutes. %s", status_code)
        time.sleep(15 * 60) # 15 minute cooloff 
        logger.info("Resuming stream..")
        return True

    def on_connection_error(self, status_code):
        logger.error("Stream has been disconnected due to %s", status_code)
        if status_code == 420:
            
            return False


def main():
    # Search keywords 
    search_terms = ["market", "market_news"]
    stream = TweetStreamer(bearer_token=BEARER_TOKEN)
    for term in search_terms:
        stream.add_rules(tweepy.StreamRule(term))
    stream.filter(tweet_fields = ["referenced_tweets"])

if __name__ == '__main__':
    # insert twitter stream code
    main()
    
    # Get producer performance metrics
    producer_metrics = producer.metrics()


