import boto3  # this is pre-downloaded on aws
import random
import tweepy
import os

# X credentials stored in env variables
API_KEY            = os.environ["API_KEY"]
API_SECRET_KEY     = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN       = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET= os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN       = os.environ["BEARER_TOKEN"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api  = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

s3_client  = boto3.client('s3')
bucket_name = 'lotr.photos'

def LOTR_meme_post(event, context):
    # 1. List up to 1,000 objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # 2. Filter for root-level image files with our allowed extensions
    allowed_ext = ('.jpg', '.jpeg', '.png', '.webp')
    image_keys = [
        obj['Key']
        for obj in response['Contents']
        if obj['Key'].lower().endswith(allowed_ext)
           and '/' not in obj['Key']   # exclude any “folders”
    ]

    if not image_keys:
        return {
            'statusCode': 404,
            'body': 'No matching image files found at the root of the bucket.'
        }

    # 3. Pick one at random
    random_file = random.choice(image_keys)

    # 4. Choose your tweet text as before
    ran = random.random()
    if   ran < 0.025: tweet_text = "#LOTR"
    elif ran < 0.05:  tweet_text = "#LordOfTheRings"
    elif ran < 0.1:   tweet_text = "Lord of the Rings"
    elif ran < 0.15:  tweet_text = "LOTR"
    else:             tweet_text = ""

    # 5. Download from S3 into Lambda’s /tmp
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # 6. Upload media and post tweet
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }

