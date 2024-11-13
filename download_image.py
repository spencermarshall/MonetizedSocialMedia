import tweepy
import time
import requests
import boto3



API_KEY =%3DShBe6NotqhviLUXh3tjd2tZIa0rAkPvK654vNKcP93mV5OPIiq'

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
BUCKET_NAME = 'lotr.photos'
#search recent tweets of user @elonmusk
tweets=None
try:
    tweets = client.search_recent_tweets(
        query="from:TheLOTRMemes has:media lang:en -is:retweet",
        max_results=3,
        tweet_fields=['created_at', 'public_metrics', 'lang', 'possibly_sensitive', 'text'],
        expansions='author_id,attachments.media_keys',  # Include media keys
        media_fields=['url', 'type', 'preview_image_url'],  # Request media fields
        user_fields=['username', 'public_metrics', 'verified']
    )
except tweepy.TooManyRequests as e:
    reset_time = int(e.response.headers.get("x-rate-limit-reset", 0))
    current_time = int(time.time())
    wait_time = reset_time - current_time

    if wait_time > 0:
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds until rate limit resets.")

print(tweets)
# Dictionary to map media keys to media objects
media_dict = {media.media_key: media for media in tweets.includes.get('media', [])}

for tweet in tweets.data:
    # Print tweet details
    author = next((user for user in tweets.includes['users'] if user.id == tweet.author_id), None)
    author_name = author.username if author else "Unknown"
    print(f"{tweet.text} by {author_name} at {tweet.created_at}")
    print(f"Tweet ID: {tweet.id}")

    # Print media details
    if 'attachments' in tweet and 'media_keys' in tweet.attachments:
        for media_key in tweet.attachments['media_keys']:
            media = media_dict.get(media_key)
            if media and media.url.endswith(('.jpg', '.png')):
                image_url = media.url
                print(f"Downloading {image_url}")

                # Download the image
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
