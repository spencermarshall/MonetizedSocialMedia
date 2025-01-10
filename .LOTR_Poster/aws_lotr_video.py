import boto3 #this is pre-downloaded on aws
import random
import tweepy
import os

lotr_api_key = 'placeholder'
lotr_api_key_secret = 'placeholder'
lotr_client_id = 'placeholder'
lotr_client_secret = 'placeholder'
lotr_bearer_token = 'placeholder'
lotr_access_token = 'placeholder'
lotr_access_token_secret = 'placeholder'

def aws_lotr_video(event, context):
    

    client = tweepy.Client(bearer_token=lotr_bearer_token,
                           consumer_key=lotr_api_key, consumer_secret=lotr_api_key_secret,
                           access_token=lotr_access_token, access_token_secret=lotr_access_token_secret)

    auth = tweepy.OAuth1UserHandler(lotr_api_key, lotr_api_key_secret, lotr_access_token, lotr_access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'lotr.videos'   # s3 bucket

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

    random_file = random.choice(mp4_files)

    titles = {
        "lotr1": "Lord of the Rings",  #i should change this to be title of 1st movie, but for now all videos are here so i just want text to be LOTR
        "lotr2": "title2",
        "lotr3": "title3",
        "hobbit1": "title4",
        "hobbit2": "title5",
        "hobbit3": "title6",
    }

    title = random_file[:random_file.find("/")]  # this gets str up until the first space
    tweet_text = titles[title]
    tweet_text += " #LordOfTheRings"
    # tweet_text += " #TheHobbit"

    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }





