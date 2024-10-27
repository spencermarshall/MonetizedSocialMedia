import boto3 #this is pre-downloaded on aws
import random
import tweepy
import os

def aws_hp_video(event, context):
    # harry potter
    hp_api_key = 'placeholder'
    hp_api_key_secret = 'placeholder'
    hp_client_id = 'placeholder'
    hp_client_secret = 'placeholder'
    hp_bearer_token = 'placeholder'
    hp_access_token = 'placeholder'
    hp_access_token_secret = 'placeholder'

    client = tweepy.Client(bearer_token=hp_bearer_token,
                           consumer_key=hp_api_key, consumer_secret=hp_api_key_secret,
                           access_token=hp_access_token, access_token_secret=hp_access_token_secret)

    auth = tweepy.OAuth1UserHandler(hp_api_key, hp_api_key_secret, hp_access_token, hp_access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'harrypotter.videos'   #'s3://starwars.videos'

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
        "hp1": "Harry Potter and the Sorcerer's Stone",
        "hp2": "Harry Potter and the Chamber of Secrets",
        "hp3": "Harry Potter and the Prisoner of Azkaban",
        "hp4": "Harry Potter and the Goblet of Fire",
        "hp5": "Harry Potter and the Order of the Phoenix",
        "hp6": "Harry Potter and the Half-Blood Prince",
        "hp7": "Harry Potter and the Deathly Hallows"
    }


    tweet_text = random_file#titles[titles] #temporarily hard coding

    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }





