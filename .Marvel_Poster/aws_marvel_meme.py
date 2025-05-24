import boto3  # AWS SDK for Python (pre-installed on Lambda)
import random
import tweepy
import os

# X credentials stored in env variables
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

# S3 client and bucket
s3_client   = boto3.client('s3')
bucket_name = 'marvel.photos'


def Marvel_meme_post(event, context):
    # 1. List all objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # 2. If the bucket is empty, bail out
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # 3. Filter: only root-level keys (no slashes) AND image extensions
    files = [
        obj['Key']
        for obj in response['Contents']
        if '/' not in obj['Key']                             # no folder prefix
        and obj['Key'].lower().endswith(('.jpg', '.webp', '.png', '.gif', '.jpeg'))
    ]

    if not files:
        return {
            'statusCode': 404,
            'body': 'No root-level image files found in the S3 bucket.'
        }

    # 4. Pick one at random
    random_file = random.choice(files)

    # 5. Optionally add a hashtag 2% of the time each
    tweet_text = ""
    ran = random.random()
    if ran < 0.02:
        tweet_text = "#Marvel"
    elif ran < 0.04:
        tweet_text = "#MarvelStudios"
    elif ran < 0.06:
        tweet_text = "#MCU"

    # 6. Download into Lambda’s temp folder
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # 7. Upload to Twitter and post
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    # 8. Return success
    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }
