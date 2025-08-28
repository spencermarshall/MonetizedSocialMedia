import requests
import random
import tweepy
import os
import json
import boto3


client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

RECENT_LIST_MAX = 20

# S3 location of the JSON file that stores the “recent indices”
S3_BUCKET = 'bb.photos'
S3_KEY    = 'notes/BB_quote.txt'
s3_client = boto3.client('s3')
# here

def post_bb_quote(event, context):
    #half the time post a meme instead
    if random.random() < 0.5:
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:975050204241:function:BB_meme_post',
            InvocationType='Event',  # Asynchronous invocation
            Payload=json.dumps({})  # Empty payload; modify if needed
        )
        return "called meme"
    breaking_bad_quotes = {
        1: "A guy opens his door and gets shot, and you think that of me? No. I am the one who knocks.",
        2: "I am not in danger, Skyler. I am the danger.",
        3: "I am not in danger, Skyler. I am the danger. A guy opens his door and gets shot, and you think that of me? No. I am the one who knocks.",
        4: "Do you know what would happen if I suddenly decided to stop going into work? A business big enough that it could be listed on the NASDAQ goes belly up. Disappears! It ceases to exist without me. No, you clearly don't know who you're talking to, so let me clue you in. I am not in danger, Skyler. I am the danger.",
        5: "Mr White, he's the devil. You know, he is... he is smarter than you, he is luckier than you. Whatever... whatever you think is supposed to happen... I'm telling you the exact reverse opposite of that is gonna happen, okay?\" -Jesse Pinkman",
        6: "Jesse, we need to cook!",
        7: "Let's just say, I know a guy who knows a guy, who knows another guy.",
        8: "You don’t want a criminal lawyer. You want a criminal lawyer",
        9: "Jesse, you asked me if I was in the meth business or the money business.. Neither. I'm in the empire business.",
        10: "This is my own private domicile and I will not be harassed... b****",
        11: "You're the smartest guy I ever met, and you're too stupid to see he made up his mind 10 minutes ago.",
        12: "They're minerals!",
        13: "My name is ASAC Schrader, and you can go f*** yourself.",
        14: "Shut the f*** up and let me die in peace.",
        15: "It's all good man",
        16: "I did it for me. I liked it. I was good at it. I was alive.",
        17: "F*** you! And your eyebrows",
        18: "Do you know how much I make a year? I mean, even if I told you, you wouldn't believe it.",
        19: "I watched Jane die. I was there. And I watched her die. I could have saved her, but I didn't. -Walter White",
        20: "I'm not in the meth business. I'm in the empire business.",
        21: "Don't drink and drive but if you do, call me. -Saul Goodman",
        22: "I do not believe fear to be an effective motivator.",
        23: "We tried to poison you. We tried to poison you because you are an insane, degenerate piece of filth and you deserve to die. -Walter White",
        24: "I'm sorry, what were you asking me? Oh, yes, that stupid plastic container I asked you to buy. You see, hydrofluoric acid won't eat through plastic; it will however dissolve metal, rock, glass, ceramic. So there's that. -Walter White",
        25: "I investigate everyone with whom I do business. What careful man wouldn't?",
        26: "Yeah b****, Magents!!",
        27: "This whole thing, all of this... It's all about me.",
        28: "I won.",
        29: "This is not Meth...",
        30: "Let's cook.",
        31: "If you don’t know who i am, then maybe your best course would be to tread lightly.",
        32: "Say my name.",
        33: "TIGHT TIGHT TIGHT",
        34: "I am the one who knocks",

    }

    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        raw_bytes = obj["Body"].read()
        text      = raw_bytes.decode("utf-8")
        recent_indices = json.loads(text)
        # If for some reason it isn’t a Python list, reset
        if not isinstance(recent_indices, list):
            recent_indices = []
    except Exception as e:
        # If the file doesn’t exist or JSON is invalid, start fresh
        recent_indices = []

    # ──── 5.2. STEP 2: CHOOSE A RANDOM INDEX NOT IN RECENT_INDICES ─────────────────
    max_index = len(breaking_bad_quotes)  # here, 35
    if max_index == 0:
        # If somehow your dictionary is empty, bail out
        return {
            "statusCode": 500,
            "body": "No breaking_bad_quotes defined."
        }

    # Pick an integer between 1 and max_index, reroll if it’s “recent”
    num = random.randint(1, max_index)
    while num in recent_indices:
        num = random.randint(1, max_index)

    # ──── 5.3. STEP 3: RETRIEVE THE QUOTE & COMPOSE TWEET TEXT ───────────────────
    quote = breaking_bad_quotes.get(num, "")
    tweet_text = quote

    # ──── 5.4. STEP 4: ATTEMPT TO POST THE TWEET ───────────────────────────────────
    try:
        client.create_tweet(text=tweet_text)
        print(f"✅ Successfully tweeted quote #{num}")
    except Exception as tweet_err:
        # Log the error; proceed to update the “recent” list anyway
        print(f"❌ Failed to tweet quote #{num}: {tweet_err}")

    # ──── 5.5. STEP 5: UPDATE THE “RECENT INDICES” LIST ───────────────────────────
    recent_indices.insert(0, num)  # put this index at the front
    if len(recent_indices) > RECENT_LIST_MAX:
        # Trim anything beyond the first RECENT_LIST_MAX
        recent_indices = recent_indices[:RECENT_LIST_MAX]

    # ──── 5.6. STEP 6: WRITE THE UPDATED LIST BACK TO S3 ───────────────────────────
    try:
        serialized = json.dumps(recent_indices)
        s3_client.put_object(Bucket=S3_BUCKET, Key=S3_KEY, Body=serialized)
        print(f"💾 Updated S3 with recent indices: {recent_indices}")
    except Exception as write_err:
        print(f"❌ Failed to write recent indices to S3: {write_err}")

    # ──── 5.7. RETURN A SIMPLE RESPONSE ─────────────────────────────────────────────
    return {
        "statusCode": 200,
        "body": f"Tried to tweet quote #{num}."
    }

