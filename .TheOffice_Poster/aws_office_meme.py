import boto3  # Pre-downloaded on AWS Lambda
import random
import tweepy
import os
import json


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

    # Maximum number of recently posted items to keep track of
    RECENTLY_POSTED = 30

    # Initialize S3 and Twitter clients
    s3_client = boto3.client('s3')

    index_key = 'notes/office_meme.txt'
    bucket_name = "office.photoss"
    obj = s3_client.get_object(Bucket=bucket_name, Key=index_key)
    content = obj['Body'].read().decode('utf-8')
    recent_memes = json.loads(content)  # Expecting a list like ["1.jpg", "2.jpg", ..., "n.jpg"]

    # List objects directly in the bucket root
    response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')

    # Filter for image files with supported extensions
    image_files = [
        file['Key'] for file in response.get('Contents', [])
        if file['Key'].endswith(('.jpg', '.webp', '.png'))
    ]

    if not image_files:
        return "No image files found directly in the bucket."

    # Select a random file not recently posted
    available_files = [f for f in image_files if f not in recent_memes]
    if not available_files:
        return "All available images have been recently posted."

    random_file = random.choice(available_files)

    # Download the file to /tmp
    download_path = f"/tmp/{random_file}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload to Twitter with appropriate media category
    if random_file.endswith('.gif'):
        media = api.media_upload(download_path, media_category='tweet_gif')
    else:
        media = api.media_upload(download_path, media_category='tweet_image')

    # Post the tweet
    client.create_tweet(text="", media_ids=[media.media_id])

    recent_memes.insert(0, random_file)
    # Truncate the list to n items if it exceeds the limit
    while len(recent_memes) > RECENTLY_POSTED:
        recent_memes.pop()

    # Save the updated list back to S3
    updated_content = json.dumps(recent_memes)
    s3_client.put_object(Bucket=bucket_name, Key=index_key, Body=updated_content)

    # Clean up and update recent_posted list
    os.remove(download_path)

    return f"Tweet posted with media: {random_file}"
