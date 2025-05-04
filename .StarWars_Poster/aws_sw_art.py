import boto3  # Pre-downloaded on AWS Lambda
import random
import tweepy
import os

def SW_art(event, context):
    # X credentials stored in env variables
    API_KEY = os.environ["API_KEY"]
    API_SECRET_KEY = os.environ["API_SECRET_KEY"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]

    # Initialize Tweepy
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    # Initialize S3 client
    s3_client = boto3.client('s3')
    bucket_name = 'starwars.photos'

    # List only objects under the "art/" prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='art/')

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the art/ folder of the S3 bucket.'
        }

    # Filter for .jpg files
    jpg_files = [
        obj['Key'] for obj in response['Contents']
        if obj['Key'].lower().endswith('.jpg')
    ]

    if not jpg_files:
        return {
            'statusCode': 404,
            'body': 'No JPG files found in art/.'
        }

    # Pick a random file and log its name
    random_file = random.choice(jpg_files)
    print(f"Selected file: {random_file}")

    # Download it locally
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload to X
    media = api.media_upload(download_path)

    # Use tweet_text from the event payload (or adjust as needed)
    client.create_tweet(text="", media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }
