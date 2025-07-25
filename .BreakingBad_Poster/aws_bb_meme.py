import boto3  # Pre-downloaded on AWS Lambda
import random
import tweepy
import os


def BB_meme_post(event, context):
    # Twitter API keys and tokens
    bb_client_id = 'cnFHZ0h6LURnVmxqbXVmZW9qWTY6MTpjaQ'
    bb_client_secret = 'gHpeCROnQ330bUhYj9Yry-dWQj01tlnogUUIHRTd8y6TM_rWVL'
    bb_api_key = 'm5GPo8zjDkAuWMuZhjTM2ksJu'
    bb_api_key_secret = 'iBt6OHUdCkq88fvwNVFsnuxL7CAU4avLzemUyU97aP18IWFZmS'
    bb_access_token = '1837346181229563904-49LOpBdittQOb1hHkrEMRk5mzhVXFU'
    bb_access_token_secret = 'HsPyF7XRBkfkhXI0sHUBZRKboPWTgtPRCy7fkHfy65bhU'
    bb_bearer_token = 'AAAAAAAAAAAAAAAAAAAAANbewAEAAAAA2dsHWBhQRdWJwY6OhKfhja6fKOY%3DShBe6NotqhviLUXh3tjd2tZIa0rAkPvK654vNKcP93mV5OPIiq'

    client = tweepy.Client(bearer_token=bb_bearer_token,
                           consumer_key=bb_api_key, consumer_secret=bb_api_key_secret,
                           access_token=bb_access_token, access_token_secret=bb_access_token_secret)

    auth = tweepy.OAuth1UserHandler(bb_api_key, bb_api_key_secret, bb_access_token, bb_access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'bb.photos'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if there are any objects in the bucket
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .jpg files
    jpg_files = [
        file['Key'] for file in response['Contents']
        if file['Key'].endswith('.jpg')
           and not file['Key'].startswith('questions/')
           and not file['Key'].startswith('notes/')
    ]
    # If there are no JPG files
    if not jpg_files:
        return {
            'statusCode': 404,
            'body': 'No JPG files found in the S3 bucket.'
        }

    # Select a random JPG file
    random_file = random.choice(jpg_files)

    tweet_text = ""
    ran = random.random()
    if ran < 0.03:
        tweet_text = "Breaking Bad"
    elif ran < 0.06:
        tweet_text = "#BreakingBad"

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