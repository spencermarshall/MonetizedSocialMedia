import tweepy
import time
import requests
import boto3
import os


X_TARGET_USERNAME = 'aestheticspost_'

BUCKET_NAME = 'nature.photos' # EDIT THIS AS NEEDED
# i need to make sure i have policy permissions for each s3 bucket




API_KEY             = os.environ["API_KEY"]
API_SECRET_KEY      = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN        = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN        = os.environ["BEARER_TOKEN"]

# Set up Tweepy v1.1 (for media uploads) and v2 (for tweeting)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api  = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
s3 = boto3.client('s3')


# Search recent tweets of specified user, from the last 7 days, that has media
def X_Download_Image_Nature(event, context):
    tweets = None
    try:
        tweets = client.search_recent_tweets(
            query=f"from:{X_TARGET_USERNAME} has:media -is:retweet",
            max_results=30,
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
            print(f"Rate limit exceeded for {X_TARGET_USERNAME}. Waiting for {wait_time} seconds.")
        return {"status": "error", "message": f"Rate limit exceeded. Wait {wait_time} seconds."}
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {str(e)}")
        return {"status": "error", "message": f"Failed to fetch tweets: {str(e)}"}

    # Check if tweets is None or has no data
    if tweets is None or tweets.data is None or not tweets.data:
        print(f"No tweets found for {X_TARGET_USERNAME} or API returned no data.")
        return {"status": "error", "message": "No tweets found or API returned no data."}

    media_dict = {media.media_key: media for media in tweets.includes.get('media', [])}
    print(f"Media found: {media_dict}")

    for tweet in tweets.data:
        author = next((user for user in tweets.includes['users'] if user.id == tweet.author_id), None)
        author_name = author.username if author else "Unknown"
        print(f"{tweet.text} by {author_name} at {tweet.created_at}")
        print(f"Tweet ID: {tweet.id}")

        if 'attachments' in tweet and 'media_keys' in tweet.attachments:
            for media_key in tweet.attachments['media_keys']:
                media = media_dict.get(media_key)
                if media:
                    if media.type in ['video', 'animated_gif']:
                        print(f"Skipping {media.type} media.")
                        continue
                    if media.type == 'photo' and hasattr(media, 'url') and media.url.endswith(('.jpg', '.png', '.webp', '.jpeg')):
                        image_url = media.url
                        print(f"Downloading {image_url}")
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            file_name = os.path.basename(image_url)
                            file_path = f"/tmp/{file_name}"
                            with open(file_path, 'wb') as file:
                                file.write(response.content)
                            # Upload to S3
                            try:
                                s3.upload_file(file_path, BUCKET_NAME, file_name)
                                print(f"Uploaded {file_name} to S3 bucket {BUCKET_NAME}")
                            except boto3.exceptions.S3UploadFailedError as e:
                                print(f"Failed to upload {file_name} to S3: {str(e)}")
                        else:
                            print(f"Failed to download {image_url}: Status code {response.status_code}")
                    else:
                        print(f"Skipping media with type {media.type} or invalid URL.")
    print("Finished processing tweets.")