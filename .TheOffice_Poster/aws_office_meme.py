import boto3  # Pre-downloaded on AWS Lambda
import random
import tweepy
import os


def office_meme_post(event, context):
    # Twitter API keys and tokens
    # Twitter API authentication setup
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAGscvwEAAAAAD%2BE%2FA1HFvb4hGDFzbZeMyA1hLuc%3D3yngqIcsmqDYyawEm2x3TVYfPEZaKYbnDRtEfFKEc9tPLmV8gk"
    api_key = "4ORKKv2122tpa1CKy6yGHZInO"
    api_key_secret = "35fQjzS0sxk5AverD0ur1YP9fZN8FdkJoS6xUW71Pc4zDGltDv"
    access_token = "1832642294165487616-Ro503mjfYALzFDKhSYqyRThUAiC2R9"
    access_token_secret = "2NsamH45xFXmM5BPUtb8K9pAIdI3hu3lvJqm561YMKSEz"
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=api_key, consumer_secret=api_key_secret,
                           access_token=access_token, access_token_secret=access_token_secret)

    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'office.photoss'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if there are any objects in the bucket
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .jpg files
    jpg_files = [file['Key'] for file in response['Contents'] if
                 file['Key'].endswith('.jpg') or file['Key'].endswith('.webp') or file['Key'].endswith('.png') or file[
                     'Key'].endswith('.gif')]

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
    if ran < 0.7:
        tweet_text = "The Office"
    elif ran < 0.8:
        tweet_text = "#TheOffice"

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