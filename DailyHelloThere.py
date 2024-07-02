import tweepy
import os

from dotenv import load_dotenv

# Your Twitter API credentials
load_dotenv()
bearer_token = os.getenv('bearer_token')
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('access_token')
ACCESS_TOKEN_SECRET = os.getenv('access_token_secret')

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Path to your GIF file
gif_path = '/images/helloThere.gif'

# Upload GIF
media = api.media_upload(gif_path)

# Post tweet with GIF
tweet_text = "Here is a fun GIF!"
api.update_status(status=tweet_text, media_ids=[media.media_id])

print("Tweet posted successfully!")
