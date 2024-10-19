import boto3 #this is pre-downloaded on aws
import random
import tweepy
import os

def aws_marvel_video(event, context):
    api_key = 'placeholder'
    api_key_secret = 'placeholder'
    bearer_token = 'placeholder'
    access_token = 'placeholder'
    access_token_secret = 'placeholder'

    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=api_key, consumer_secret=api_key_secret,
                           access_token=access_token, access_token_secret=access_token_secret)

    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'marvel.videos'   #'s3://marvel.videos'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)


    # Check if there are any objects in the bucket
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .mp4 files
    mp4_files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.mp4')]

    # If there are no MP4 files
    if not mp4_files:
        return {
            'statusCode': 404,
            'body': 'No MP4 files found in the S3 bucket.'
        }

    # Select a random MP4 file
    random_file = random.choice(mp4_files)

    titles = {
        "infinitywar": "Avengers: Infinity War",
        "endgame": "Avengers: Endgame"
    }

    title = random_file[:random_file.find("/")] #this gets str up until the first space
    tweet_text = titles[title]
    tweet_text += " #MCU"
    if random.random() > 0.85:
        tweet_text += " #Marvel"


    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }





