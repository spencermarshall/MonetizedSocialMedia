import tweepy
import os
import logging
import sys
from dotenv import load_dotenv


class DailyHelloTherePoster:
    def __init__(self):
        # Set up logging
        logging.basicConfig(filename='daily_hello_there.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')

        logging.debug(f"Running script with Python version: {sys.version}")

        # Load environment variables
        env_path = os.path.abspath('.env')
        logging.debug(f"Loading environment variables from: {env_path}")
        load_dotenv(env_path)

        # Your Twitter API credentials
        self.BEARER_TOKEN = os.getenv('BEARER_TOKEN')
        self.API_KEY = os.getenv('API_KEY')
        self.API_SECRET_KEY = os.getenv('API_SECRET_KEY')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

        # Check if environment variables are loaded correctly
        if not all([self.API_KEY, self.API_SECRET_KEY, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET, self.BEARER_TOKEN]):
            logging.error("Some environment variables are missing. Please check your .env file.")
            raise ValueError("Some environment variables are missing. Please check your .env file.")

        # Paths to your GIF file and count file
        self.gif_path = os.path.abspath('images/helloThere.gif')
        self.count_file = os.path.abspath('count/countDailyHelloThere.txt')

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
        try:
            if os.path.exists(self.count_file):
                with open(self.count_file, 'r') as file:
                    return int(file.read().strip())
            return 0
        except Exception as e:
            logging.error(f"Error reading count file: {e}")
            raise

    def write_count(self, count):
        try:
            with open(self.count_file, 'w') as file:
                file.write(str(count))
        except Exception as e:
            logging.error(f"Error writing count file: {e}")
            raise

    def post_tweet(self):
        try:
            # Debugging: Print the current working directory
            logging.debug(f"Current working directory: {os.getcwd()}")

            # Debugging: Print the absolute path to the GIF file
            logging.debug(f"Absolute path to GIF: {self.gif_path}")

            # Check if the GIF file exists
            if not os.path.isfile(self.gif_path):
                raise FileNotFoundError(f"The file at path {self.gif_path} was not found.")

            # Upload GIF using media_upload (v1.1)
            media = self.api.media_upload(self.gif_path)

            # Print the media ID and other information
            logging.debug(f"Media uploaded successfully! Media ID: {media.media_id}")
            logging.debug(f"Media details: {media}")

            # Read the current count from the file
            count = self.read_count()

            # Increment the count
            count += 1

            # Post tweet with the uploaded GIF using create_tweet (v2)
            tweet_text = f"Day {count} of me posting Obi-Wan Kenobi's \"Hello there\" from Star Wars Episode 3: Revenge of the Sith #StarWars #TheAcolyte #Kenobi #Obiwan #hellothere"
            response = self.client.create_tweet(text=tweet_text, media_ids=[media.media_id])
            logging.debug(f"Tweet posted successfully! Response: {response}")

            # Write the updated count back to the file
            self.write_count(count)

        except tweepy.TweepyException as e:
            logging.error(f"An error occurred with Tweepy: {e}")
            if hasattr(e, 'api_codes') and 453 in e.api_codes:
                logging.error(
                    "It seems your API credentials do not have the necessary permissions to upload media. Please check your access level on the Twitter Developer Portal.")
            raise

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise


def main():
    try:
        poster = DailyHelloTherePoster()
        poster.post_tweet()
    except Exception as e:
        logging.error(f"Failed to post tweet: {e}")


if __name__ == "__main__":
    main()
