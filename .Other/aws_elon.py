import praw
import tweepy
import os
import random
import json
import boto3
import requests
from datetime import datetime, timedelta



client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

auth = tweepy.OAuth1UserHandler(
    api_key, api_key_secret,
    access_token, access_token_secret
)
api = tweepy.API(auth)

# --- Initialize S3 client ---
s3_client = boto3.client('s3')
BUCKET_NAME = 'elon.media'

def elon_musk_daily(event, context):
    # 1) Generate a “negative” text
    negative_base = ['No', 'Nope', 'Not today', 'Negative', 'Not yet', 'Nah', 'Nay', 'Definitely not']
    text = random.choice(negative_base)
    if random.random() < 0.5:
        text += '!'

    # 2) Decide branch: 50% text-only, 50% text+image
    if random.random() < 0.5:
        # Text-only tweet
        client.create_tweet(text=text)
    else:
        # Image branch
        # 2a) List and filter image files in S3
        resp = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        keys = [
            obj['Key'] for obj in resp.get('Contents', [])
            if obj['Key'].lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
        ]

        if not keys:
            # Fallback to text-only if no images found
            print("Couldn't find image")
            client.create_tweet(text=text)
        else:
            # 2b) Pick a random image
            key = random.choice(keys)
            local_path = os.path.join('/tmp', os.path.basename(key))

            # 2c) Download it
            s3_client.download_file(BUCKET_NAME, key, local_path)

            # 2d) Upload to Twitter and get media_id
            media = api.media_upload(local_path)
            media_id = media.media_id

            # 2e) Tweet with image
            client.create_tweet(text=text, media_ids=[media_id])

    return text
