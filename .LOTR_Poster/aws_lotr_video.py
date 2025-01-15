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


def aws_lotr_video(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'lotr.videos'  # s3 bucket

    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # only .mp4 files
    mp4_files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.mp4')]

    if not mp4_files:
        return {
            'statusCode': 404,
            'body': 'No MP4 files found in the S3 bucket.'
        }

    random_file = random.choice(mp4_files)

    titles = {
        "lotr1": "LOTR: The Fellowship of the Ring",
        "lotr2": "LOTR: The Two Towers",
        "lotr3": "LOTR: The Return of the King",
        "hobbit1": "The Hobbit: An Unexpected Journey",
        "hobbit2": "The Hobbit: The Desolation of Smaug",
        "hobbit3": "The Hobbit: The Battle of the Five Armies",
    }

    title = random_file[:random_file.find("/")]  # this gets str up until the first space
    tweet_text = titles[title]

    if random.random() < 0.5:
        if tweet_text[0] == "L":
            tweet_text = tweet_text[6:]
        elif tweet_text[0] == "T":
            tweet_text = tweet_text[12:]

    ran = random.random()
    if ran < 0.02:
        tweet_text += " #LOTR"
    elif ran < 0.04:
        tweet_text += " #LordOfTheRings"

    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }
