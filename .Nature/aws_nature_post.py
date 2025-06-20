import boto3
import random
import tweepy
import os
import json

# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

# Constant for number of recent files to track
RECENT_NUM = 30

# S3 bucket and recent files list path
BUCKET_NAME = 'nature.photos'
RECENT_FILES_KEY = 'notes/nature.txt'

# Initialize tweepy and boto3 clients
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
s3_client = boto3.client('s3')

def get_recent_files():
    """Retrieve the list of recent files from S3 or return empty list if not found."""
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=RECENT_FILES_KEY)
        recent_files = json.loads(response['Body'].read().decode('utf-8'))
        return recent_files
    except s3_client.exceptions.NoSuchKey:
        return []

def update_recent_files(new_file, recent_files):
    """Add new file to front of recent files list and truncate to RECENT_NUM."""
    recent_files.insert(0, new_file)
    if len(recent_files) > RECENT_NUM:
        recent_files = recent_files[:RECENT_NUM]
    # Save updated list to S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=RECENT_FILES_KEY,
        Body=json.dumps(recent_files)
    )
    return recent_files

def NaturePost(event, context):
    # 1. List up to 1,000 objects in the bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # 2. Filter for root-level image files with allowed extensions
    allowed_ext = ('.jpg', '.jpeg', '.png', '.webp')
    image_keys = [
        obj['Key']
        for obj in response['Contents']
        if obj['Key'].lower().endswith(allowed_ext)
           and '/' not in obj['Key']  # exclude any “folders”
    ]

    if not image_keys:
        return {
            'statusCode': 404,
            'body': 'No matching image files found at the root of the bucket.'
        }

    # 3. Get recent files list
    recent_files = get_recent_files()

    # 4. Pick a random file not in recent_files
    available_keys = [key for key in image_keys if key not in recent_files]
    if not available_keys:
        return {
            'statusCode': 404,
            'body': 'No available image files (all recent files used).'
        }

    random_file = random.choice(available_keys)

    # 5. Download from S3 into Lambda’s /tmp
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(BUCKET_NAME, random_file, download_path)

    # 6. Upload media and post tweet
    try:
        media = api.media_upload(download_path)
        client.create_tweet(text="", media_ids=[media.media_id])
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to post tweet: {str(e)}"
        }

    # 7. Update recent files list
    update_recent_files(random_file, recent_files)

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }