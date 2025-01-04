import tweepy
import os
import random
import requests
from datetime import date

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)


def dailyHelloThere(event, context):
    start_date = date(2024, 7, 1)
    today_date = date.today()
    days_since_target = (today_date - start_date).days

    name = "Kenobi"
    ran = random.random()
    if ran > 0.5:
        name = "Obi-Wan Kenobi"

    title = " "
    ran = random.random()
    if ran > 0.2:
        title = " Star Wars "
    tweet_text = f"Day {days_since_target} of posting {name}'s \"Hello there\" from{title}Episode 3: Revenge of the Sith "

    ran = random.random()
    if ran < 0.04:
        tweet_text += "#swtwt"
    elif ran < 0.05:
        tweet_text += "#StarWars"
    elif ran < 0.055:
        tweet_text += "#Kenobi"
    elif ran < 0.06:
        tweet_text += "#Obiwan"
    elif ran < 0.065:
        tweet_text += "#hellothere"

    # temp github, todo: in future put the helloThere.gif in s3 bucket and pull from there, but this works for now
    media_url = 'https://raw.githubusercontent.com/spencermarshall/StarWarsTwitterPost/main/images/helloThere.gif'
    temp_filename = '/tmp/temp_media.gif'

    response = requests.get(media_url)
    if response.status_code == 200:
        with open(temp_filename, 'wb') as f:
            f.write(response.content)

        media = api.media_upload(temp_filename)

        client.create_tweet(text=tweet_text, media_ids=[media.media_id])

        os.remove(temp_filename)
    else:
        print("Failed to download media")
