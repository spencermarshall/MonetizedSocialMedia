import json
import random
import os
import boto3
import tweepy

# --- Config ---
HISTORY_LENGTH = 12  # 👈 change this number to 7, 15, 100 etc.

# --- Tweepy client setup ---
API_KEY             = os.environ["API_KEY"]
API_SECRET_KEY      = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN        = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN        = os.environ["BEARER_TOKEN"]

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
)

# --- Quote dictionary ---
quotes = {
    1: "A wizard is never late, nor is he early, he arrives precisely when he means to.",
    2: "YOU SHALL NOT PASS!",
    3: "When in doubt, follow your nose",
    4: "What about second breakfast?",
    5: "Fool of a took!",
    6: "For Frodo...",
    7: "I don't know half of you half as well as I should like...",
    8: "There's some good in this world, Mr. Frodo...",
    9: "In a hole in the ground there lived a hobbit...",
    10: "In a hole in the ground there lived a hobbit.",
    11: "So you have chosen...death",
    12: "I am no man",
    13: "I am not trying to rob you. I am trying to help you.",
    14: "I can't recall the taste of food...",
    15: "Po-ta-toes! Boil 'em, mash 'em...",
    16: "PO-TA-TOES",
    17: "Never thought I'd die fighting side by side with an elf",
}

# --- S3 config ---
S3_BUCKET = "lotr.photos"
S3_KEY    = "notes/lotr_quote.txt"
s3        = boto3.client("s3")

def load_history():
    """Fetch the most recent quote IDs from S3, or return a default list."""
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        hist = json.loads(obj["Body"].read().decode("utf-8"))
        if isinstance(hist, list) and all(isinstance(i, int) for i in hist):
            return hist[:HISTORY_LENGTH]
    except Exception:
        pass
    return [0] * HISTORY_LENGTH

def save_history(hist):
    """Write the updated history list to S3."""
    trimmed = hist[:HISTORY_LENGTH]
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=json.dumps(trimmed),
        ContentType="application/json"
    )

def lotr_quote(event, context):
    # 1️⃣ Load history
    recent = load_history()

    # 2️⃣ Pick a quote not in recent history
    max_id = len(quotes)
    while True:
        candidate = random.randint(1, max_id)
        if candidate not in recent:
            break

    # 3️⃣ Update and save history
    updated = [candidate] + recent
    save_history(updated)

    # 4️⃣ Tweet
    text = quotes[candidate]
    client.create_tweet(text=text)

    # 5️⃣ Return response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "quote_id": candidate,
            "text": text,
            "new_history": updated[:HISTORY_LENGTH]
        })
    }
