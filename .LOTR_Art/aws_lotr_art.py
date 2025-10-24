import boto3      # AWS SDK for Python, to talk to S3
import random     # for picking a random file
import tweepy     # Twitter/X API client
import os         # to read environment variables
import json       # to parse and write JSON

CHECK_RECENT = 100  # Number of recent images to track

def LOTR_art(event, context):
    # 1️⃣ Load Twitter credentials
    API_KEY             = os.environ["API_KEY"]
    API_SECRET_KEY      = os.environ["API_SECRET_KEY"]
    ACCESS_TOKEN        = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    BEARER_TOKEN        = os.environ["BEARER_TOKEN"]

    # 2️⃣ Init Tweepy clients
    auth   = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY,
                                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
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
    bucket    = 'lotr.photos'
    index_key = 'notes/LOTR_art.txt'
    prefix    = 'art/'

    # 4️⃣ Load our recent list from S3
    obj            = s3.get_object(Bucket=bucket, Key=index_key)
    content        = obj['Body'].read().decode('utf-8')
    recent_files = json.loads(content)  # e.g. ["ar3987ghi.jpg", "sfeugi3.png", …]

    # 5️⃣ List all image keys under art/ with common extensions
    allowed_exts = ('.jpg', '.jpeg', '.png', '.webp')
    resp     = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    objects  = resp.get('Contents', [])
    images   = [o['Key'] for o in objects
                if o['Key'].lower().endswith(allowed_exts)]

    if not images:
        return {'statusCode': 404, 'body': 'No images found under art/'}

    # 6️⃣ Pick a random image whose filename isn’t in the recent list
    while True:
        chosen_key = random.choice(images)
        if os.path.basename(chosen_key) not in recent_files:
            break

    # 7️⃣ Update the recent list: prepend new, trim to CHECK_RECENT
    recent_files.insert(0, os.path.basename(chosen_key))
    recent_files = recent_files[:CHECK_RECENT]
    s3.put_object(
        Bucket=bucket,
        Key=index_key,
        Body=json.dumps(recent_files)
    )

    # 8️⃣ Download the chosen image locally
    local_path = f"/tmp/{os.path.basename(chosen_key)}"
    s3.download_file(bucket, chosen_key, local_path)

    # 9️⃣ Upload to Twitter and tweet it
    media = api.media_upload(local_path)
    client.create_tweet(text="", media_ids=[media.media_id])

    # 🔟 Return success
    return {
        'statusCode': 200,
        'body': (
            f"Tweeted fresh LOTR art {os.path.basename(chosen_key)!r}, "
            f"updated recent list to {CHECK_RECENT} items."
        )
    }