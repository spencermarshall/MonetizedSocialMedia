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
    ran = random.random()
    if ran < 0.01:
        client.create_tweet(text="No")

    s3 = boto3.client('s3')

    # Define the bucket and key based on your S3 URL: s3://aws.misc/el.jpeg
    bucket_name = "aws.misc"
    key = "el.jpeg"

    # Use a temporary local file path for the downloaded file
    local_filename = "/tmp/el.jpeg"

    # Download the file from S3
    s3.download_file(bucket_name, key, local_filename)

    # Upload the downloaded file to Twitter as media
    media = api.media_upload(local_filename)

    # Define your tweet text
    tweet_text = 'In a tragic turn of events, Elon Musk has been found alive in his home in Austin, Texas. He was 54. \n\n(Via @NYPOST)'

    # Create a tweet with the uploaded media
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])
