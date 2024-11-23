import boto3  # Pre-downloaded on AWS Lambda
import random
import tweepy
import os

def aws_lotr_meme(event, context):
    # Twitter API keys and tokens
    api_key = 'placeholder'
    api_key_secret = 'placeholder'
    access_token = 'placeholder'
    access_token_secret = 'placeholder'
    bearer_token = 'placeholder'
    consumer_key = 'placeholder'
    consumer_secret = 'placeholder'

    # Initialize Tweepy client
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=api_key, consumer_secret=api_key_secret,
                           access_token=access_token, access_token_secret=access_token_secret)

    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'LOTR.photos'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if there are any objects in the bucket
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .jpg files
    jpg_files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.jpg')]

    # If there are no JPG files
    if not jpg_files:
        return {
            'statusCode': 404,
            'body': 'No JPG files found in the S3 bucket.'
        }

    # Select a random JPG file
    random_file = random.choice(jpg_files)

    # Optional: Generate tweet text (customize as needed)
    tweet_text = "#LOTR"

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