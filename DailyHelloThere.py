import tweepy
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


# it reads the file, increments by 1, makes tweet (With new number), then puts new number into file
class DailyHelloTherePoster:
    def __init__(self):

        # Load environment variables
        load_dotenv()

        # Your Twitter API credentials
        self.BEARER_TOKEN = os.getenv('BEARER_TOKEN')
        self.API_KEY = os.getenv('API_KEY')
        self.API_SECRET_KEY = os.getenv('API_SECRET_KEY')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

        # Paths to your GIF file and count file
        self.gif_path = Path('images/helloThere.gif').resolve()
        self.count_file = Path('count/countDailyHelloThere.txt').resolve()

        # Authenticate to Twitter using Client for v2 API
        self.client = tweepy.Client(
            bearer_token=self.BEARER_TOKEN,
            consumer_key=self.API_KEY,
            consumer_secret=self.API_SECRET_KEY,
            access_token=self.ACCESS_TOKEN,
            access_token_secret=self.ACCESS_TOKEN_SECRET
        )

        # Authenticate to Twitter using OAuth1UserHandler for media upload (v1.1)
        self.auth = tweepy.OAuth1UserHandler(self.API_KEY, self.API_SECRET_KEY, self.ACCESS_TOKEN,
                                             self.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def read_count(self):
        if self.count_file.exists():
            with self.count_file.open('r') as file:
                return int(file.read().strip())
        return 0

    def write_count(self, count):
        with self.count_file.open('w') as file:
            file.write(str(count))

    def post_tweet(self):
        if not self.gif_path.is_file():
            raise FileNotFoundError(f"The file at path {self.gif_path} was not found.")

        # Upload GIF using media_upload (v1.1)
        media = self.api.media_upload(self.gif_path)

        # Read the current count from the file
        count = self.read_count()

        # Increment the count
        count += 1

        # Post tweet with the uploaded GIF using create_tweet (v2)
        tweet_text = f"Day {count} of me posting Obi-Wan Kenobi's \"Hello there\" from Star Wars Episode 3: Revenge of the Sith #StarWars #TheAcolyte #Kenobi #Obiwan #hellothere"
        self.client.create_tweet(text=tweet_text, media_ids=[media.media_id])

        # Write the updated count back to the file
        self.write_count(count)

if __name__ == "__main__":
    poster = DailyHelloTherePoster()
    poster.post_tweet()
