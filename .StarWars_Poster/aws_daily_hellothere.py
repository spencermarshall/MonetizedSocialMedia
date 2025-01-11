import os
import random
import boto3
import tweepy
from datetime import date

# X credentials stored in env variables
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
    # 1) Calculate the day count since your start date
    start_date = date(2024, 7, 1)
    today_date = date.today()
    days_since_target = (today_date - start_date).days

    name = "Kenobi"
    if random.random() < 0.5:
        name = "Obi-Wan Kenobi"

    title = " "
    if random.random() < 0.8:
        title = " Star Wars "

    posting = "posting"
    if random.random() < 0.1:
        posting = "tweeting"

    tweet_text = (
        f"Day {days_since_target} of {posting} {name}'s \"Hello there\" from{title}Episode 3: Revenge of the Sith "
    )

    r = random.random()
    if r < 0.04:
        tweet_text += "#swtwt"
    elif r < 0.05:
        tweet_text += "#StarWars"
    elif r < 0.055:
        tweet_text += "#Kenobi"
    elif r < 0.06:
        tweet_text += "#Obiwan"
    elif r < 0.065:
        tweet_text += "#hellothere"

    s3 = boto3.client('s3')
    bucket_name = 'starwars.gifs'
    ep3_hellothere = 'hellothere/helloThere.gif'
    temp_filename = '/tmp/temp_media.gif'

    try:
        s3.download_file(bucket_name, ep3_hellothere, temp_filename)
    except Exception as e:
        print(f"Failed to download {ep3_hellothere} from S3: {e}")
        return  # Exit if we cannot get the file

    media = api.media_upload(temp_filename)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    os.remove(temp_filename)
