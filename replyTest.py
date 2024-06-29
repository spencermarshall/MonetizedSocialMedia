import random
import tweepy
from subpackage.CloneWarsQuotes import getCloneWarsQuote
from dotenv import load_dotenv
import os

class Reply:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        api_secret_key = os.getenv('API_SECRET_KEY')
        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')

        auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
        self.client = tweepy.Client(bearer_token=bearer_token)

        self.api = tweepy.API(auth)
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except Exception as e:
            print(f"Error during authentication: {e}")

    def keyWord(self, query, max_results=10):
        try:
            tweets = self.client.search_recent_tweets(query=query, max_results=max_results)
            for tweet in tweets.data:
                print(f"Tweet ID: {tweet.id} - Tweet Text: {tweet.text}")
        except Exception as e:
            print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    poster = Reply()
    poster.keyWord("test")
