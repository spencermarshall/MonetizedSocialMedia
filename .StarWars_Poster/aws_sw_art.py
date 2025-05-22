import boto3      # AWS SDK for Python, to talk to S3
import random     # for picking a random file
import tweepy     # Twitter/X API client
import os         # to read environment variables
import json       # to parse and write JSON

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
    obj              = s3.get_object(Bucket=bucket, Key=index_key)
    content          = obj['Body'].read().decode('utf-8')
    question_indices = json.loads(content)  # e.g. [12, 5, 79, …]

    # 5️⃣ List all JPG keys under art/
    listing = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    jpgs    = [
        o['Key'] for o in listing.get('Contents', [])
        if o['Key'].lower().endswith('.jpg')
    ]
    if not jpgs:
        return {'statusCode': 404, 'body': 'No JPGs found under art/'}

    # 6️⃣ Pick a random file—and ensure its number isn’t in our 14
    def extract_num(key):
        start = key.find('(')
        end   = key.find(')', start + 1)
        return int(key[start+1:end])

    while True:
        chosen = random.choice(jpgs)
        num = extract_num(chosen)
        if num not in question_indices:
            break
        # else: we loop and pick again

    # 7️⃣ Now that we have a fresh `num`, push it onto the front…
    question_indices.insert(0, num)
    #    …and trim to keep exactly 30 entries
    while len(question_indices) > 30:
        question_indices.pop()

    # 8️⃣ Write that updated list back to S3
    updated = json.dumps(question_indices)
    s3.put_object(Bucket=bucket, Key=index_key, Body=updated)

    # 9️⃣ Download the chosen image locally
    local_path = f"/tmp/{os.path.basename(chosen)}"
    s3.download_file(bucket, chosen, local_path)

    # 🔟 Upload to Twitter and tweet it
    media = api.media_upload(local_path)
    client.create_tweet(text="", media_ids=[media.media_id])

    # 1️⃣1️⃣ Return success
    return {
        'statusCode': 200,
        'body': (
            f"Picked fresh image #{num}, kept recent list at 14 items, "
            f"and tweeted: {chosen}"
        )
    }
