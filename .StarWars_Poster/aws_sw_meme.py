import boto3
import random
import tweepy
import os
import json
import botocore

MAX_RECENT = 30


def SW_meme_post(event, context):
    # Twitter credentials from environment variables
    API_KEY = os.environ["API_KEY"]
    API_SECRET_KEY = os.environ["API_SECRET_KEY"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]

    # Initialize Tweepy API and Client
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
    index_key = 'notes/SW_meme.txt'

    # Load the list of recent meme file names from S3
    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=index_key)
        content = obj['Body'].read().decode('utf-8')
        recent_memes = json.loads(content)  # Expecting a list like ["1.jpg", "2.jpg", ..., "n.jpg"]
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            recent_memes = []  # Start with an empty list if the file doesn't exist
        else:
            raise

    # List all .jpg files in the bucket, excluding specified prefixes
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' not in response:
        return {'statusCode': 404, 'body': 'No files found in the S3 bucket.'}
    jpg_files = [
        file['Key'] for file in response['Contents']
        if file['Key'].endswith('.jpg')
           and not file['Key'].startswith('questions/')
           and not file['Key'].startswith('notes/')
           and not file['Key'].startswith('art/')
    ]
    if not jpg_files:
        return {'statusCode': 404, 'body': 'No JPG files found in the S3 bucket.'}

    # Select a random meme that is not in the recent_memes list
    available_memes = [f for f in jpg_files if f not in recent_memes]
    if not available_memes:
        return {'statusCode': 404, 'body': 'No available memes to post.'}
    random_file = random.choice(available_memes)

    # Generate random tweet text based on probabilities
    tweet_text = ""
    rand_val = random.random()
    if rand_val < 0.01:
        tweet_text = "#StarWars"
    elif rand_val < 0.02:
        tweet_text = "#swtwt"
    elif rand_val < 0.03:
        tweet_text = "#StarWarsMemes"
    elif rand_val < 0.04:
        tweet_text = "Star Wars Meme"
    elif rand_val < 0.2:
        tweet_text = "lol"
    elif rand_val < 0.4:
        tweet_text = "😂"
    elif rand_val < 0.6:
        tweet_text = "🤣"
    elif rand_val < 0.8:
        tweet_text = "LOL"


    # Download the selected meme to a temporary location
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the meme to Twitter and post the tweet
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    # Update the recent_memes list: insert new file at the front
    recent_memes.insert(0, random_file)
    # Truncate the list to n items if it exceeds the limit
    while len(recent_memes) > MAX_RECENT:
        recent_memes.pop()

    # Save the updated list back to S3
    updated_content = json.dumps(recent_memes)
    s3_client.put_object(Bucket=bucket_name, Key=index_key, Body=updated_content)

    # Return success response
    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }