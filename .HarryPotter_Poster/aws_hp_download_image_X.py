import tweepy
import time
import requests
import boto3
import os

# this lambda is identical to X_2 except X_TARGET_USERNAME is different, meaning it downloads from a different
# x account

X_TARGET_USERNAME = 'AllboutHogwarts'  # EDIT THIS AS NEEDED
BUCKET_NAME = 'harrypotter.photos'  # EDIT THIS AS NEEDED
# i need to make sure i have policy permissions for each s3 bucket


# Set up Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

s3 = boto3.client('s3')


# search recent tweets of specified user, from the last 7 days, that has media
def X_Download_Image_HP(event, context):
    tweets = None
    try:
        tweets = client.search_recent_tweets(
            query=f"from:{X_TARGET_USERNAME} has:media -is:retweet",
            max_results=31,
            tweet_fields=['created_at', 'public_metrics', 'lang', 'possibly_sensitive', 'text'],
            expansions='author_id,attachments.media_keys',
            media_fields=['url', 'type', 'preview_image_url'],
            user_fields=['username', 'public_metrics', 'verified']
        )
    except tweepy.TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", 0))
        current_time = int(time.time())
        wait_time = reset_time - current_time
        # X API can only request every 15 minutes, this shows cooldown if you've done more than 1
        if wait_time > 0:
            print(
                f"{X_TARGET_USERNAME} had a Rate limit exceeded. Waiting for {wait_time} seconds until rate limit resets.")
    print(tweets)
    media_dict = {media.media_key: media for media in tweets.includes.get('media', [])}
    print(media_dict)

    for tweet in tweets.data:
        author = next((user for user in tweets.includes['users'] if user.id == tweet.author_id), None)
        author_name = author.username if author else "Unknown"
        print(f"{tweet.text} by {author_name} at {tweet.created_at}")
        print(f"Tweet ID: {tweet.id}")

        if 'attachments' in tweet and 'media_keys' in tweet.attachments:
            num_media = len(tweet.attachments['media_keys'])
            print("#### HERE #####\n")
            print(f"Number of media attachments: {num_media}")
            if num_media > 1:
                print("SKIP b/c > 1 media")
                continue
            for media_key in tweet.attachments['media_keys']:
                media = media_dict.get(media_key)
                if media and media.url.endswith(
                        ('.jpg', '.png', 'webp', '.gif', '.jpeg')):  # this filters media to just get jpg or png
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
