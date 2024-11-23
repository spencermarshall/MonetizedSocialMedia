import tweepy
import time
import requests
import boto3
import os

X_TARGET_USERNAME = 'rPrequelMemes' # EDIT THIS AS NEEDED
BUCKET_NAME = 'starwars.photos' # EDIT THIS AS NEEDED
# i need to make sure i have policy permissions for each s3 bucket


# X api keys
API_KEY = 'placeholder'
API_SECRET_KEY = 'placeholder'
bearer_token = 'placeholder'
access_token = 'placeholder'
access_token_secret = 'placeholder'


auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token = bearer_token,
    consumer_key = API_KEY,
    consumer_secret = API_SECRET_KEY,
    access_token = access_token,
    access_token_secret = access_token_secret
)
s3 = boto3.client('s3')

#search recent tweets of specified user, from the last 7 days, that has media
def X_Download_Image_LOTR(event, context):
    tweets=None
    try:
        tweets = client.search_recent_tweets(
            query=f"from:{X_TARGET_USERNAME} has:media -is:retweet",
            max_results=100,
            tweet_fields=['created_at', 'public_metrics', 'lang', 'possibly_sensitive', 'text'],
            expansions='author_id,attachments.media_keys',
            media_fields=['url', 'type', 'preview_image_url'],
            user_fields=['username', 'public_metrics', 'verified']
        )
    except tweepy.TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", 0))
        current_time = int(time.time())
        wait_time = reset_time - current_time
        #X API can only request every 15 minutes, this shows cooldown if you've done more than 1
        if wait_time > 0:
            print(f"{X_TARGET_USERNAME} had a Rate limit exceeded. Waiting for {wait_time} seconds until rate limit resets.")
    print(tweets)
    media_dict = {media.media_key: media for media in tweets.includes.get('media', [])}
    print(media_dict)

    for tweet in tweets.data:
        author = next((user for user in tweets.includes['users'] if user.id == tweet.author_id), None)
        author_name = author.username if author else "Unknown"
        print(f"{tweet.text} by {author_name} at {tweet.created_at}")
        print(f"Tweet ID: {tweet.id}")

        if 'attachments' in tweet and 'media_keys' in tweet.attachments:
            for media_key in tweet.attachments['media_keys']:
                media = media_dict.get(media_key)
                if media and media.url.endswith(('.jpg', '.png')): #this filters media to just get jpg or png
                    image_url = media.url
                    print(f"Downloading {image_url}")

                    response = requests.get(image_url)
                    if response.status_code == 200:
                        file_name = os.path.basename(image_url)

                        # Save the file to /tmp (AWS Lambda's writable directory)
                        file_path = f"/tmp/{file_name}"
                        with open(file_path, 'wb') as file:
                            file.write(response.content)

                        # Upload to S3
                        s3.upload_file(file_path, BUCKET_NAME, file_name)
                        print(f"Uploaded {file_name} to S3 bucket {BUCKET_NAME}")

                    else:
                        print(f"Failed to download {image_url}")
