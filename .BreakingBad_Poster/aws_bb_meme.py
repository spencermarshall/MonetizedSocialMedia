import boto3  # Pre-downloaded on AWS Lambda
import random
import tweepy
import os
import json
import botocore.exceptions

MOST_RECENT = 200


def BB_meme_post(event, context):
    # Twitter API keys and tokens

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

    # Fetch the recent memes list from S3
    file_key = 'notes/BB_meme.txt'
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        recent_files = json.loads(file_content)
    except s3_client.exceptions.NoSuchKey:
        recent_files = []
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error fetching recent files: {str(e)}'
        }

    # Select a random JPG file not in the recent list
    random_file = random.choice(jpg_files)
    while random_file in recent_files:
        random_file = random.choice(jpg_files)

    tweet_text = ""
    ran = random.random()
    if ran < 0.03:
        tweet_text = "Breaking Bad"
    elif ran < 0.05:
        tweet_text = "#BreakingBad"

    # Download the selected file to a temporary directory
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    # Update the recent files list
    recent_files.insert(0, random_file)

    if len(recent_files) > MOST_RECENT:
        recent_files.pop()

    updated_content = json.dumps(recent_files)
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }