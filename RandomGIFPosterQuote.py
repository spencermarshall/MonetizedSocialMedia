import random
import tweepy
import os
from dotenv import load_dotenv
from pathlib import Path

class RandomGIFPoster:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.recent_files_file = Path('count/recentFilesGIFPosterQuote.txt').resolve()

        # Your Twitter API credentials
        self.BEARER_TOKEN = os.getenv('BEARER_TOKEN')
        self.API_KEY = os.getenv('API_KEY')
        self.API_SECRET_KEY = os.getenv('API_SECRET_KEY')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

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

        self.gif_folder_quote = Path('images/quote-or-meme').resolve()
        self.gif_folder_no_words = Path('images/no-words').resolve()

    def read_recent_paths(self) -> list:
        if self.recent_files_file.exists():
            with self.recent_files_file.open('r') as file:
                return file.read().strip().split('\n')
        return []

    def get_random_gif(self, quote: bool = True) -> Path:
        gifs = list(self.gif_folder_quote.glob('*.gif')) if quote else list(self.gif_folder_no_words.glob('*.gif'))
        recent_paths = self.read_recent_paths()

        # Ensure the randomly selected GIF is not in the recent paths
        available_gifs = [gif for gif in gifs if gif.name not in recent_paths]

        if available_gifs:
            return random.choice(available_gifs)
        return None

    def write_recent_paths(self, paths: list):
        with self.recent_files_file.open('w') as file:
            file.write('\n'.join(paths))

    def post_gif(self, random_gif: Path):
        recent_paths = self.read_recent_paths()

        while random_gif.name in recent_paths:
            random_gif = self.get_random_gif(quote=True)


        # Upload GIF using media_upload (v1.1)
        media = self.api.media_upload(str(random_gif))

        # Prepare tweet text
        additional_text = ""
        text_dict = {        # todo, i can edit this dictionary to add any caption i want for any specific gif
            "don't-like-sand.gif": "I don't like sand. It's coarse, and rough, and irritating. And it gets everywhere...",
            "execute-order-66.gif": "Execute Order 66"
        }
        if random_gif.name in text_dict:
            additional_text = text_dict[random_gif.name]

        tags = "#StarWars #TheAcolyte #swtwt"
        tweet_text = f"{additional_text} {tags}"
        self.client.create_tweet(text=tweet_text, media_ids=[media.media_id])

        # Update the recent paths with the new path
        recent_paths.append(random_gif.name)
        if len(recent_paths) > 3:
            recent_paths.pop(0)  # Keep only the last 3 paths

        # Write the updated recent paths back to the file
        self.write_recent_paths(recent_paths)

if __name__ == "__main__":
    poster = RandomGIFPoster()
    random_gif = poster.get_random_gif(quote=True)
    if random_gif:
        poster.post_gif(random_gif)
