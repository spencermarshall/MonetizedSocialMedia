import boto3      # AWS SDK for Python, to talk to S3
import random     # for picking a random file
import tweepy     # Twitter/X API client
import os         # to read environment variables
import json       # to parse and write JSON
import botocore.exceptions

# Number of recent images to avoid repeating
MAX_RECENT = 210

def SW_art(event, context):
    # 1️⃣ Load Twitter credentials
    API_KEY             = os.environ["API_KEY"]
    API_SECRET_KEY      = os.environ["API_SECRET_KEY"]
    ACCESS_TOKEN        = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    BEARER_TOKEN        = os.environ["BEARER_TOKEN"]

    # 2️⃣ Init Tweepy
    auth   = tweepy.OAuth1UserHandler(
                API_KEY, API_SECRET_KEY,
                ACCESS_TOKEN, ACCESS_TOKEN_SECRET
             )
    api    = tweepy.API(auth)
    client = tweepy.Client(
                bearer_token=BEARER_TOKEN,
                consumer_key=API_KEY,
                consumer_secret=API_SECRET_KEY,
                access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_TOKEN_SECRET
             )

    # 3️⃣ Init S3 info
    s3        = boto3.client('s3')
    bucket    = 'starwars.photos'
    index_key = 'notes/SW_art.txt'
    prefix    = 'art/'

    # 4️⃣ Load our “recent” list from S3
    try:
        obj              = s3.get_object(Bucket=bucket, Key=index_key)
        content          = obj['Body'].read().decode('utf-8')
        recent_keys = json.loads(content)  # e.g. ['art (12).jpg', 'art (5).jpg', …]
    except s3.exceptions.NoSuchKey:
        recent_keys = []
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error fetching recent files: {str(e)}'
        }

    # 5️⃣ List all JPG keys under art/
    listing = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    jpgs    = [
        o['Key'] for o in listing.get('Contents', [])
        if o['Key'].lower().endswith('.jpg')
    ]
    if not jpgs:
        return {'statusCode': 404, 'body': 'No JPGs found under art/'}

    # 6️⃣ Pick a random file—and ensure it isn’t in our recent list
    while True:
        chosen = random.choice(jpgs)
        chosen_basename = os.path.basename(chosen)
        if chosen_basename not in recent_keys:
            break
        # else: we loop and pick again

    # 7️⃣ Now that we have a fresh `chosen`, push it onto the front…
    recent_keys.insert(0, chosen_basename)
    #    …and trim to keep at most MAX_RECENT entries
    while len(recent_keys) > MAX_RECENT:
        recent_keys.pop()

    # 8️⃣ Write that updated list back to S3
    updated = json.dumps(recent_keys)
    s3.put_object(Bucket=bucket, Key=index_key, Body=updated)

    # 9️⃣ Download the chosen image locally
    local_path = f"/tmp/{os.path.basename(chosen)}"
    s3.download_file(bucket, chosen, local_path)

    # 🔟 Upload to Twitter and tweet it
    media = api.media_upload(local_path)
    client.create_tweet(text="", media_ids=[media.media_id])


    scheduler_client = boto3.client('scheduler')
    try:
        # Fetch current schedule to get the current minute
        get_response = scheduler_client.get_schedule(GroupName='default', Name='SW_art')
        current_schedule = get_response['ScheduleExpression']  # e.g., cron(20 4,8,13,18,23 * * ? *)
        current_min = int(current_schedule.split(' ')[0].split('(')[1])  # Extract minute from cron
    except Exception as e:
        print(f"Error fetching current schedule: {str(e)}")
        current_min = 20  # Default to 20 if schedule fetch fails

    # Increment minute by random amount (4-9), reset if > 40
    new_min = current_min + random.randint(4, 9)
    if new_min > 40:
        new_min -= 20

    new_expr = f"cron({new_min} 4,8,13,18,23 * * ? *)"
    try:
        update_params = {
            'Name': 'SW_art',
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

    # 1️⃣1️⃣ Return success
    return {
        'statusCode': 200,
        'body': (
            f"Picked fresh image {chosen}, kept recent list at {MAX_RECENT} items, "
            f"and tweeted: {chosen}"
        )
    }