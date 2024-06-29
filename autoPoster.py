import random

import self
import tweepy
from urllib3 import response
from subpackage.CloneWarsQuotes import getCloneWarsQuote
from dotenv import load_dotenv
import os


class TwitterPoster:
    def __init__(self):
        load_dotenv()
        bearer_token = os.getenv('bearer_token')
        API_KEY = os.getenv('API_KEY')
        API_SECRET_KEY = os.getenv('API_SECRET_KEY')
        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')

        self.client = tweepy.Client(bearer_token = bearer_token,
                                        consumer_key = API_KEY, consumer_secret = API_SECRET_KEY,
                                        access_token = access_token, access_token_secret = access_token_secret)

    def postCWQuote(self):
        finalTweet = getCloneWarsQuote(self) + " #StarWars #TheCloneWars #StarWarsQuotes"
        try:
            # Post the tweet using the Client
            response = self.client.create_tweet(text=finalTweet)

        except Exception as e:
            print(f"An error occurred: {e}")

    def getCloneWarsQuote(self):
        # Placeholder for your method that gets a Clone Wars quote
        return "The strongest defense is a swift and decisive offense."


# Example usage
if __name__ == "__main__":
    poster = TwitterPoster()
    poster.postCWQuote()