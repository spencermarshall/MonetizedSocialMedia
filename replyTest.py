import tweepy
from dotenv import load_dotenv
import random
import os
import time

class TwitterClient:
    def __init__(self):
        load_dotenv()

        # Load and print environment variables to verify the y  are loaded correctly
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.api_key = os.getenv('API_KEY')
        self.api_secret_key = os.getenv('API_SECRET_KEY')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        print(f"BEARER_TOKEN: {self.bearer_token}")
        print(f"API_KEY: {self.api_key}")
        print(f"API_SECRET_KEY: {self.api_secret_key}")
        print(f"ACCESS_TOKEN: {self.access_token}")
        print(f"ACCESS_TOKEN_SECRET: {self.access_token_secret}")

        # Check if any of the keys are None
        if not all([self.bearer_token, self.api_key, self.api_secret_key, self.access_token, self.access_token_secret]):
            print("One or more environment variables are missing.")
            return

        # Initialize the Tweepy client
        try:
            self.client_v2 = tweepy.Client(bearer_token=self.bearer_token,
                                           consumer_key=self.api_key,
                                           consumer_secret=self.api_secret_key,
                                           access_token=self.access_token,
                                           access_token_secret=self.access_token_secret)
            print("Tweepy Client v2 initialized successfully.")
        except Exception as e:
            print(f"Error initializing Tweepy Client v2: {e}")

    def check_access_level(self):
        # Attempt to make a simple API call to check access
        try:
            response = self.client_v2.get_me()
            print(f"Access Level Verified: {response.data}")
        except tweepy.TweepyException as e:
            print(f"Error checking access level: {e}")

    def reply_to_tweet(self, text, tweet_id):
        print(f"Attempting to reply to tweet ID {tweet_id} with text: {text}")
        try:
            response = self.client_v2.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
            print(f"Replied to Tweet: {response.data['id']}")
        except tweepy.TweepyException as e:
            print(f"Error replying to tweet: {e}")

    #this returns a string that would be a good generic response to (hopefully) any post regardless of context. So hopefully it'll be good.
    def get_generic_response(self):
        #todo, at any time edit this dictionary below this line,
        phrases = {"hello there": 0.2, " hello there": 0.2, "...": 0.3, ":|": 0.2} #key-value pairs, "comment":weight. doesn't have to sum to 1, but it auto-converts to scale of 1
        return random.choices(list(phrases.keys()), weights=list(phrases.values()), k=1)[0] #this line came from chat gpt, it uses values as weights to output a key

    def getTweetIDs(self):
        output = ["1809379239575081221"]

        return output

if __name__ == "__main__":
    client = TwitterClient()
    client.check_access_level()
    numStop = random.randint(1,3) #only reply to 1-3 tweets (assuming we even have that many)
    listOfID = client.getTweetIDs() #call function to pull recent tweet ID from key user's
    for i in range(len(listOfID)):
        client.reply_to_tweet("hello there", listOfID[i]) #this will actualyl reply to it, full functional
        time.sleep(random.randint(60,120)) #random wait time between 60 and 120 seconds between replies
        if i + 1 >= numStop: #reply to num of tweets then stop
            exit() #stops execution


