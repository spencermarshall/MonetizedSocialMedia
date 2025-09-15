import json
import random
import os
import boto3
import tweepy



# --- Tweepy client setup ---
API_KEY            = os.environ["API_KEY"]
API_SECRET_KEY     = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN       = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET= os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN       = os.environ["BEARER_TOKEN"]

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
)

quotes = {
    1: "Hello There",
    2: "If you strike me down, I will become more powerful than you could possibly imagine.",
    3: "May the force be with you.", #keep
    4: "I have a bad feeling about this.",
    5: "It's over Anakin, I have the High Ground.",
    6: "Good soldiers follow orders.",
    # 7: "Execute Order 66", #todo i moved this to main questions
    7: "",
    8: "No, I am your father.",
    9: "Do or do not, there is no try.",
    10: "Help me Obi-Wan Kenobi. You're my only hope.",
    11: "It's a Trap!", #keep
    12: "I am one with the Force, and the Force is with me.",
    13: "This is the way",
    14: "Long live the Empire.",
    15: "I don't like sand. It's coarse, and rough, and irritating... and it gets everywhere.", #keep
    16: "I'm just a simple man trying to make my way in the universe.", #keep
    17: "These are not the droids you are looking for",
    18: "That's no moon. That's a space station.", #keep
    19: "Strike me down, and I shall become more powerful than you can possibly imagine.",
    20: "This is where the fun begins.",
    21: "Gonk", #keep
    22: "I am no Jedi.",
    23: "I am the Senate.", #keep
    24: "I have brought Peace, Freedom, Justice, and Security to my new Empire.",
    25: "A surprise, to be sure, but a welcome one.",
    26: "I'll try spinning, that's a good trick.",
    27: "Now this is podracing.",
    28: "In my experience, there's no such thing as luck",
    29: "Aren't you a little short for a storm trooper?", #keep
    30: "Fear is the path to the dark side. Fear leads to anger, anger leads to hate, hate leads to suffering.",
    31: "These are not the droids you're looking for.",
    32: "I find your lack of faith disturbing.",
    33: "The ability to speak does not make you intelligent.",
    34: "So this is how liberty dies... with thunderous applause.",
    35: "Only a Sith deals in absolutes.", #keep
    36: "I sense a plot to destroy the Jedi.", #keep
    37: "",
    38: "",
    39: "I can bring you in warm, or I can bring you in cold.",
    40: "What about the droid attack on the wookies?", #keep
    41: "I'm a Mandalorian. Weapons are part of my religion.",
    42: "I have friends everywhere...",
    43: "The mission. The nightmares. They're... finally... over.",
    44: "I am a Jedi, like my father before me.",
    45: "We're just clones, sir. We're meant to be expendable.", #keep
    46: "Clones, bred for combat. All part of the plan... THE Plan. The only Plan that matters. Not even I was made aware of its grand design, but I played my part. And do you know what happened to me? I was cast aside. I was forgotten. But I survived, and I can thrive in the chaos that is to come.",
    47: "Do it.",
    48: "As a Jedi, we were trained to be keepers of the peace, not soldiers. But all I've been since I was a Padawan is a soldier.", #keep
    49: "You're a good soldier Rex. So is every one of those men down there. They may be willing to die, but I am not the one who is going to kill them.",
}


# --- S3 config ---
S3_BUCKET = "starwars.photos"
S3_KEY    = "notes/SW_quote.txt"
s3        = boto3.client("s3")

def load_history():
    """Fetch the 7 most‐recent quote IDs from S3, or default to zeros."""
    try:
        obj  = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        hist = json.loads(obj["Body"].read().decode("utf-8"))
        if isinstance(hist, list) and all(isinstance(i, int) for i in hist):
            return hist
    except Exception:
        pass
    # On any failure, start with a ‘blank’ history
    return [0] * 7

def save_history(hist):
    """Write the updated 7‐item list back to S3."""
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=json.dumps(hist),
        ContentType="application/json"
    )

def postQuote(event, context):
    # Added code for 50% chance to call SW_art
    if random.random() < 0.0:
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:975050204241:function:SW_art',
            InvocationType='Event'  # Asynchronous invocation to not wait for response
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Called SW_art and exiting"})
        }


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

    # 5️⃣ Return a proper JSON response (so Lambda doesn’t return null)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "quote_id": candidate,
            "text": text,
            "new_history": updated
        })
    }