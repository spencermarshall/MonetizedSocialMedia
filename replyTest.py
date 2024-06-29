import tweepy
from dotenv import load_dotenv
import os

class TwitterClient:
    def __init__(self):
        load_dotenv()
        bearer_token = os.getenv('BEARER_TOKEN')
        self.client = tweepy.Client(bearer_token=bearer_token)

    def search_tweets_by_keyword(self, query, max_results=10):
        try:
            tweets = self.client.search_recent_tweets(query=query, max_results=max_results)
            if tweets.data:
                for tweet in tweets.data:
                    print(f"Tweet ID: {tweet.id} - Tweet Text: {tweet.text}")
            else:
                print("No tweets found")
        except tweepy.TweepyException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    client = TwitterClient()
    client.search_tweets_by_keyword("Python", 10)
