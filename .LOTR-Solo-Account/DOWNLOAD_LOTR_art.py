import tweepy
import time
import requests
import boto3
import os

X_TARGET_USERNAME = 'nimgaladh'
BUCKET_NAME = 'lotr.photos'
FOLDER_NAME = 'art'

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

s3 = boto3.client('s3')


def LOTR_ArtDownload(event, context):
    tweets = None
    try:
        tweets = client.search_recent_tweets(
            query=f"from:{X_TARGET_USERNAME} has:media -is:retweet",
            max_results=25,
            tweet_fields=['created_at', 'public_metrics', 'lang', 'possibly_sensitive', 'text'],
            expansions='author_id,attachments.media_keys',
            media_fields=['url', 'type', 'preview_image_url'],
            user_fields=['username', 'public_metrics', 'verified']
        )
    except tweepy.TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", 0))
        current_time = int(time.time())
        wait_time = reset_time - current_time
        if wait_time > 0:
            print(
                f"{X_TARGET_USERNAME} had a Rate limit exceeded. Waiting for {wait_time} seconds until rate limit resets.")
        return

    if not tweets.data:
        print("No tweets found.")
        return

    media_dict = {media.media_key: media for media in tweets.includes.get('media', [])}

    for tweet in tweets.data:
        if tweet.possibly_sensitive:
            print(f"Skipping tweet {tweet.id} due to possibly sensitive content.")
            continue

        author = next((user for user in tweets.includes['users'] if user.id == tweet.author_id), None)
        author_name = author.username if author else "Unknown"
        print(f"{tweet.text} by {author_name} at {tweet.created_at}")
        print(f"Tweet ID: {tweet.id}")

        if 'attachments' in tweet and 'media_keys' in tweet.attachments:
            if len(tweet.attachments['media_keys']) != 1:
                print(f"Skipping tweet {tweet.id} due to multiple media items.")
                continue

            media_key = tweet.attachments['media_keys'][0]
            media = media_dict.get(media_key)
            if media and media.type == 'photo' and media.url and media.url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_url = media.url
                print(f"Downloading {image_url}")

                response = requests.get(image_url)
                if response.status_code == 200:
                    file_name = os.path.basename(image_url)
                    s3_key = f"{FOLDER_NAME}/{file_name}"

                    file_path = f"/tmp/{file_name}"
                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                    s3.upload_file(file_path, BUCKET_NAME, s3_key)
                    print(f"Uploaded {file_name} to S3 bucket {BUCKET_NAME}/{s3_key}")
                else:
                    print(f"Failed to download {image_url}")
            else:
                print(f"Skipping tweet {tweet.id} due to unsupported media type or format.")
