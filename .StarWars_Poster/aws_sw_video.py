#this is an exact copy of what is in AWS Lambda "SW_video"
import boto3  # this is pre-downloaded on aws
import random
import tweepy
import os


def aws_sw_video(event, context):
    API_KEY = os.environ["API_KEY"]
    API_SECRET_KEY = os.environ["API_SECRET_KEY"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]

    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                           access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    s3_client = boto3.client('s3')

    # aws S3 bucket name
    bucket_name = 'starwars.videos'  # 's3://starwars.videos'

    # List all objects in the bucket - i only put .mp4 in this bucket but i verify files chosen end in .mp4
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .mp4 files - s3 bucket should only have .mp4 in the first place though
    mp4_files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.mp4')]

    if not mp4_files:
        return {
            'statusCode': 404,
            'body': 'No MP4 files found in the S3 bucket.'
        }

    random_file = random.choice(mp4_files) #this picks a random mp4 file from the s3 bucket

    titles = {
        "ep1": "The Phantom Menace",
        "ep2": "Attack of the Clones",
        "ep3": "Revenge of the Sith",
        "ep4": "A New Hope",
        "ep5": "The Empire Strikes Back",
        "ep6": "Return of the Jedi",
        "ep7": "The Force Awakens",
        "ep8": "The Last Jedi",
        "ep9": "The Rise of Skywalker",

        "rogueone": "Rogue One",
        "solo": "Solo: A Star Wars Story",

        "tcw": "The Clone Wars",
        "rebels": "Star Wars Rebels",
        "mando": "The Mandalorian",
        "bobf": "The Book of Boba Fett",
        "badbatch": "The Bad Batch",
        "kenobi": "Obi-Wan Kenobi",
        "andor": "Andor",
        "ahsoka": "Ahsoka",
        "visions": "Visions",
        "resist": "Resistance",
        "totj": "Tales of the Jedi",
        "acolyte": "The Acolyte"
    }
    tweet_text = "What are your opinions on "

    title = random_file[:random_file.find("/")]  # this gets file name until /
    tweet_text += titles[title]
    tweet_text += "?"

    if random.random() < 0.5:
        tweet_text = "Did you enjoy " + titles[title] + " as a movie?"

    ran = random.random()
    if ran < 0.01:
        tweet_text += " #StarWars"
    elif ran < 0.03:
        tweet_text += " #swtwt"

    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    media = api.media_upload(download_path)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id]) #this actually posts the tweet

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }
