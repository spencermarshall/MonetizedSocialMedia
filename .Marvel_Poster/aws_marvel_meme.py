import boto3  # AWS SDK for Python (pre-installed on Lambda)
import random
import tweepy
import os
import json  # <-- To handle the list of recent files

# Global variable to control the size of the history
MOST_RECENT = 100

# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

# Set up Tweepy v1.1 (for media uploads) and v2 (for tweeting)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# S3 client and bucket
s3_client = boto3.client('s3')
bucket_name = 'marvel.photos'


def Marvel_meme_post(event, context):
    # 1. List all objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # 2. If the bucket is empty, bail out
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # 3. Filter: only root-level keys (no slashes) AND image extensions
    files = [
        obj['Key']
        for obj in response['Contents']
        if '/' not in obj['Key']  # no folder prefix
           and obj['Key'].lower().endswith(('.jpg', '.webp', '.png', '.gif', '.jpeg'))
    ]

    if not files:
        return {
            'statusCode': 404,
            'body': 'No root-level image files found in the S3 bucket.'
        }

    # 4. Fetch the list of recently posted files from S3
    file_key = 'notes/MarvelMeme.txt'
    try:
        s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        content = s3_response['Body'].read().decode('utf-8')
        recent_files = json.loads(content)
    except s3_client.exceptions.NoSuchKey:
        # If the tracking file doesn't exist yet, start with an empty list
        recent_files = []
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error reading recent files list from S3: {str(e)}"
        }

    # 5. Pick a random file that has not been posted recently
    available_files = [f for f in files if f not in recent_files]

    # If all available files have been posted recently, reset the pool.
    # This allows the bot to start reusing old images once it has gone through all of them.
    if not available_files:
        available_files = files

    random_file = random.choice(available_files)

    # 6. Optionally add a hashtag
    tweet_text = ""
    ran = random.random()
    if ran < 0.1:
        tweet_text = "#Marvel"
    elif ran < 0.2:
        tweet_text = "#MarvelStudios"
    elif ran < 0.3:
        tweet_text = "#MCU"
    elif ran < 0.5:
        tweet_text = "Marvel"
    elif ran < 0.7:
        tweet_text = "MCU"


    # 7. Download into Lambda’s temp folder
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # 8. Upload to Twitter and post
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    # 9. Update the recent files list and save it back to S3
    # Add the new file to the beginning of the list
    recent_files.insert(0, random_file)

    # Trim the list to ensure it doesn't exceed the MOST_RECENT limit
    updated_recent_files = recent_files[:MOST_RECENT]

    # Upload the updated list back to the S3 file
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=json.dumps(updated_recent_files)
    )

    # 10. Return success
    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }