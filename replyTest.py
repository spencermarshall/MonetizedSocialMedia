import tweepy
from dotenv import load_dotenv
import os

class TwitterClient:
    def __init__(self):
        load_dotenv()
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.api_key = os.getenv('API_KEY')
        self.api_secret_key = os.getenv('API_SECRET_KEY')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        print(f"Bearer Token: {self.bearer_token[:5]}... Loaded")
        print(f"API Key: {self.api_key[:5]}... Loaded")
        print(f"API Secret Key: {self.api_secret_key[:5]}... Loaded")
        print(f"Access Token: {self.access_token[:5]}... Loaded")
        print(f"Access Token Secret: {self.access_token_secret[:5]}... Loaded")

        try:
            self.client_v2 = tweepy.Client(bearer_token=self.bearer_token,
                                           consumer_key=self.api_key,
                                           consumer_secret=self.api_secret_key,
                                           access_token=self.access_token,
                                           access_token_secret=self.access_token_secret)
            print("Tweepy Client v2 initialized successfully.")
        except Exception as e:
            print(f"Error initializing Tweepy Client v2: {e}")

    def create_tweet(self, text):
        print(f"Attempting to create tweet with text: {text}")
        try:
            response = self.client_v2.create_tweet(text=text)
            print(f"Created Tweet: {response.data['id']}")
        except tweepy.TweepyException as e:
            print(f"Error creating tweet: {e}")

    def search_tweets_by_keyword(self, query, max_results=10):
        print(f"Attempting to search tweets with query: {query}")
        try:
            tweets = self.client_v2.search_recent_tweets(query=query, max_results=max_results)
            if tweets.data:
                for tweet in tweets.data:
                    print(f"Tweet ID: {tweet.id} - Tweet Text: {tweet.text}")
            else:
                print("No tweets found")
        except tweepy.TweepyException as e:
            print(f"Error searching tweets by keyword: {e}")

    def search_tweets_by_username(self, username, max_results=10):
        query = f"from:{username}"
        print(f"Attempting to search tweets from user: {username}")
        try:
            tweets = self.client_v2.search_recent_tweets(query=query, max_results=max_results)
            if tweets.data:
                for tweet in tweets.data:
                    print(f"Tweet ID: {tweet.id} - Tweet Text: {tweet.text}")
            else:
                print("No tweets found")
        except tweepy.TweepyException as e:
            print(f"Error searching tweets by username: {e}")

    def lookup_tweets(self, tweet_ids):
        print(f"Attempting to lookup tweets with IDs: {tweet_ids}")
        try:
            tweets = self.client_v2.get_tweets(ids=tweet_ids)
            for tweet in tweets.data:
                print(f"Tweet ID: {tweet.id} - Tweet Text: {tweet.text}")
        except tweepy.TweepyException as e:
            print(f"Error looking up tweets: {e}")

    def get_user_info(self, username):
        print(f"Attempting to get user info for username: {username}")
        try:
            user = self.client_v2.get_user(username=username)
            print(f"User ID: {user.data.id} - User Name: {user.data.name}")
        except tweepy.TweepyException as e:
            print(f"Error getting user info: {e}")

if __name__ == "__main__":
    client = TwitterClient()

    # Test creating a tweet
    client.create_tweet("Hello Twitter!")

    # Test searching tweets by keyword
    client.search_tweets_by_keyword("Python", 10)

    # Test searching tweets by username
    client.search_tweets_by_username("TwitterUsername", 10)

    # Test looking up specific tweets
    client.lookup_tweets(["tweet_id_1", "tweet_id_2"])

    # Test getting user information
    client.get_user_info("TwitterUsername")
