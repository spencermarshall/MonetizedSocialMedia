import praw
import tweepy
import os
import random
import json
import boto3
import requests
from datetime import datetime, timedelta

client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key, consumer_secret=api_key_secret,
                       access_token=access_token, access_token_secret=access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)


def elon_musk_daily(event, context):
    text = ''
    ran = random.randint(1, 2)
    if ran == 1:
        text = 'No'
    elif ran == 2:
        negative_words = ['Nope', 'Not today', 'Negative', 'Not yet', 'Nah', 'Nay', 'Definitely not']
        text = random.choice(negative_words)

    if random.random() < 0.5:  # 50% add '!'
        text = text + '!'

    # next add images from s3 bucket 50% of time
    client.create_tweet(text=text)
    return text

    # else add image

    # tweet_text = 'In a tragic turn of events, Elon Musk has been found alive in his home in Austin, Texas. He was 54. \n\n(Via @NYPOST)'

    # client.create_tweet(text=tweet_text, media_ids=[media.media_id])
