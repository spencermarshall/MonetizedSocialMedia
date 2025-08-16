import boto3  # this is pre-downloaded on aws
import random
import tweepy
import os
import json
import botocore.exceptions

MOST_RECENT = 200

# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

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
bucket_name = 'lotr.photos'


def MiddleEarthPost(event, context):
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
           and '/' not in obj['Key']  # exclude any “folders”
    ]

    if not image_keys:
        return {
            'statusCode': 404,
            'body': 'No matching image files found at the root of the bucket.'
        }

    # Fetch the recent memes list from S3
    file_key = 'notes/MiddleEarthMeme.txt'
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

    # 3. Pick one at random not in the recent list
    random_file = random.choice(image_keys)
    while random_file in recent_files:
        random_file = random.choice(image_keys)

    tweet_text = ""
    ran = random.random()
    if ran < 0.09:
        tweet_text = "Middle Earth"
    elif ran < 0.10:
        tweet_text = "#MiddleEarth"
    elif ran < 0.19:
        tweet_text = "Lord of the Rings"
    elif ran < 0.20:
        tweet_text = "#LordOfTheRings"
    elif ran < 0.29:
        tweet_text = "LOTR"
    elif ran < 0.30:
        tweet_text = "#LOTR"
    elif ran < 0.39:
        tweet_text = "Rings of Power"
    elif ran < 0.40:
        tweet_text = "#RingsOfPower"
    elif ran < 0.49:
        tweet_text = "The Hobbit"
    elif ran < 0.50:
        tweet_text = "#TheHobbit"

    # 5. Download from S3 into Lambda’s /tmp
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # 6. Upload media and post tweet
    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    # Update the recent files list
    recent_files.insert(0, random_file)
    if len(recent_files) > MOST_RECENT:
        recent_files.pop()
    updated_content = json.dumps(recent_files)
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)

    scheduler_client = boto3.client('scheduler')
    new_min = random.randint(0, 59)

    # this below should be identical to EventBridge Scheduler Cron Expression, hours are 9 and 17
    new_expr = f"cron({new_min} 9,17 * * ? *)"
    try:
        get_response = scheduler_client.get_schedule(GroupName='default', Name='MiddleEarthMeme')
        update_params = {
            'Name': 'MiddleEarthMeme',
            'GroupName': 'default',
            'ScheduleExpression': new_expr,
            'FlexibleTimeWindow': get_response['FlexibleTimeWindow'],
            'Target': get_response['Target'],
            'State': get_response['State']
        }
        timezone = get_response.get('ScheduleExpressionTimezone')
        if timezone is not None:
            update_params['ScheduleExpressionTimezone'] = timezone
        description = get_response.get('Description')
        if description is not None:
            update_params['Description'] = description
        kms_key_arn = get_response.get('KmsKeyArn')
        if kms_key_arn is not None:
            update_params['KmsKeyArn'] = kms_key_arn
        scheduler_client.update_schedule(**update_params)
    except Exception as e:
        print(f"Error updating schedule: {str(e)}")

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }