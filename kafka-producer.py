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

# authentication
# auth = tweepy.OAuth1UserHandler(consumer_key=CONSUMER_KEY,
#                                 consumer_secret=CONSUMER_SECRET,
#                                 access_token=ACCESS_TOKEN,
#                                 access_token_secret=ACCESS_SECRET
#                                 )
# api = tweepy.API(auth)

# Instantiate kafka client
kafka_client = KafkaClient(bootstrap_servers=["localhost:9092"])
producer = KafkaProducer(bootstrap_servers=["localhost:9092"])


def rule_generator(screen_names, search_terms, english=True, no_rt=False):
    """Generate rules for input search terms with option to filter for english only and non-retweets"""
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
                if screen_names.index(name) != len(screen_names)-1:
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


class TweetStreamer(StreamingClient):

    def on_tweet(self, tweet):
        print(f"Full tweet: {tweet}")
        print(f"Tweet ID: {tweet.id}, Tweet: {tweet.text}")

        logger.info("Incoming data: %s", tweet['data'])
        try:
            producer.send(TOPIC_NAME, json.dumps(tweet['data']))
            producer.flush()
            time.sleep(0.5)
        except Exception as e:
            print(e)

    # def on_errors(self, status_code):
    #     logger.error("Stream has been disconnected due to %s", status_code)
    #     if status_code == 420:
    #         return False
    #
    # def on_exception(self, exception):
    #     print("An error has occurred while trying retrieve tweets: {}".format(exception))


def main():
    # Search keywords
    screen_names = ["Benzinga", "CNBC Now", "Stocktwits", "WSJ Markets"]
    hashtags = ["#earthquake", "#storm", "#tsunami", "#flooding"]
    search_terms = ["market narrative"]
    # rules = rule_generator(screen_names=screen_names, search_terms=search_terms, english=True, no_rt=True)
    rules = "from (@stlouisfed OR @business OR @MarketWatch) lang:en -is:retweet"
    print(rules)
    rule_ids = []
    # existing_rules = TweetStreamer.get_rules()
    # logger.info("Existing rules: %s", existing_rules)
    # initialize client
    streaming_client = TweetStreamer(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
    result = streaming_client.get_rules()
    print(result)
    if result.data:
        for rule in result.data:
            print(f"rule marked for deletion: {rule.id} - {rule.value}")
            rule_ids.append(rule.id)
        if len(rule_ids) > 0:
            streaming_client.delete_rules(rule_ids)
        else:
            print("No rules to delete.")
    streaming_client = TweetStreamer(bearer_token=BEARER_TOKEN)
    streaming_client.add_rules(add=tweepy.StreamRule(value=rules))
    streaming_client.filter()


if __name__ == '__main__':
    # insert twitter stream code
    main()
