import random

import self
import tweepy
from urllib3 import response
from subpackage.CloneWarsQuotes import getCloneWarsQuote


class TwitterPoster:
    def __init__(self):
        # My Credentials


        # Initialize the tweepy.Client with the necessary credentials


        self.client = tweepy.Client(bearer_token=self.bearer_token,
                                        consumer_key=self.API_KEY, consumer_secret=self.API_SECRET_KEY,
                                        access_token=self.access_token, access_token_secret=self.access_token_secret)

    def postCWQuote(self):
        tweet_text = "May the force be with you, always. #StarWars #StarWarsQuotes #StarWarsMemes"
        ans = getCloneWarsQuote(self)
        finalTweet = ans + " #StarWars #TheCloneWars #StarWarsQuotes"

        # Create a tweet
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