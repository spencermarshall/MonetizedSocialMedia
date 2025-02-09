import boto3  # this is pre-downloaded on aws
import random
import tweepy
import os

# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

s3_client = boto3.client('s3')
bucket_name = 'marvel.photos'


def Marvel_meme_post(event, context):
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter to include only .jpg files or .webp files or .png files
    files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.jpg') or file['Key'].endswith('.webp') or file['Key'].endswith('.png')]


    if not files:
        return {
            'statusCode': 404,
            'body': 'No JPG files found in the S3 bucket.'
        }

    random_file = random.choice(files)

    tweet_text = ""  # 20% of each possible: "", #LOTR, #LordOfTheRings, Lord of the Rings, LOTR
    ran = random.random()
    if ran < 0.02:
        tweet_text = "#Marvel"
    elif ran < 0.04:
        tweet_text = "#MarvelStudios"
    elif ran < 0.06:
        tweet_text = "#MCU"


    # Download the selected file to a temporary directory
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }
