import json
import random
import os
import boto3
import tweepy

# --- Tweepy client setup ---
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
)

quotes = {
    1: "Hello There",

}

# --- S3 config ---
S3_BUCKET = "lotr.photos"
S3_KEY = "notes/lotr_quote.txt"
s3 = boto3.client("s3")


def load_history():
    """Fetch the 7 most‐recent quote IDs from S3, or default to zeros."""
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        hist = json.loads(obj["Body"].read().decode("utf-8"))
        if isinstance(hist, list) and all(isinstance(i, int) for i in hist):
            return hist
    except Exception:
        pass
    return [0] * 7


def save_history(hist):
    """Write the updated 7‐item list back to S3."""
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=json.dumps(hist),
        ContentType="application/json"
    )


def lotr_quote(event, context):
    # 1️⃣ Load last 7 IDs
    recent = load_history()

    # 2️⃣ Pick a new random ID not in the recent history
    max_id = len(quotes)
    while True:
        candidate = random.randint(1, max_id)
        if candidate not in recent:
            break

    # 3️⃣ Update history (prepend & trim) and save
    updated = [candidate] + recent[:-1]
    save_history(updated)

    # 4️⃣ Tweet the chosen quote
    text = quotes[candidate]
    client.create_tweet(text=text)

    # 5️⃣ Return a proper JSON response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "quote_id": candidate,
            "text": text,
            "new_history": updated
        })
    }
