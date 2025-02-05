import boto3  # this is pre-downloaded on aws
import random
import tweepy
import os


def aws_bb_video(event, context):
    bb_client_id = 'placeholder'
    bb_client_secret = 'placeholder'
    bb_api_key = 'placeholder'
    bb_api_key_secret = 'placeholder'
    bb_access_token = 'placeholder'
    bb_access_token_secret = 'placeholder'
    bb_bearer_token = 'placeholder'

    client = tweepy.Client(bearer_token=bb_bearer_token,
                           consumer_key=bb_api_key, consumer_secret=bb_api_key_secret,
                           access_token=bb_access_token, access_token_secret=bb_access_token_secret)

    auth = tweepy.OAuth1UserHandler(bb_api_key, bb_api_key_secret, bb_access_token, bb_access_token_secret)
    api = tweepy.API(auth)

    # Initialize the S3 client
    s3_client = boto3.client('s3')


    # Define your S3 bucket name
    bucket_name = 'bb.videos'  # 's3://bb.videos'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if there are any objects in the bucket
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .mp4 files
    mp4_files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.mp4')]

    # If there are no MP4 files
    if not mp4_files:
        return {
            'statusCode': 404,
            'body': 'No MP4 files found in the S3 bucket.'
        }

    # Select a random MP4 file
    random_file = random.choice(mp4_files)

    # filter season and episode
    s_pos = random_file.find('s') + 1  # The season number starts after 's'
    e_pos = random_file.find('e') + 1  # The episode number starts after 'e'
    se = f"s{s_pos}e{e_pos}"

    breaking_bad_episodes = {
        "s1e1": "Pilot",
        "s1e2": "Cat's in the Bag...",
        "s1e3": "...And the Bag's in the River",
        "s1e4": "Cancer Man",
        "s1e5": "Gray Matter",
        "s1e6": "Crazy Handful of Nothin'",
        "s1e7": "A No-Rough-Stuff-Type Deal",

        "s2e1": "Seven Thirty-Seven",
        "s2e2": "Grilled",
        "s2e3": "Bit by a Dead Bee",
        "s2e4": "Down",
        "s2e5": "Breakage",
        "s2e6": "Peekaboo",
        "s2e7": "Negro y Azul",
        "s2e8": "Better Call Saul",
        "s2e9": "4 Days Out",
        "s2e10": "Over",
        "s2e11": "Mandala",
        "s2e12": "Phoenix",
        "s2e13": "ABQ",

        "s3e1": "No Más",
        "s3e2": "Caballo sin Nombre",
        "s3e3": "I.F.T.",
        "s3e4": "Green Light",
        "s3e5": "Más",
        "s3e6": "Sunset",
        "s3e7": "One Minute",
        "s3e8": "I See You",
        "s3e9": "Kafkaesque",
        "s3e10": "Fly",
        "s3e11": "Abiquiu",
        "s3e12": "Half Measures",
        "s3e13": "Full Measure",

        "s4e1": "Box Cutter",
        "s4e2": "Thirty-Eight Snub",
        "s4e3": "Open House",
        "s4e4": "Bullet Points",
        "s4e5": "Shotgun",
        "s4e6": "Cornered",
        "s4e7": "Problem Dog",
        "s4e8": "Hermanos",
        "s4e9": "Bug",
        "s4e10": "Salud",
        "s4e11": "Crawl Space",
        "s4e12": "End Times",
        "s4e13": "Face Off",

        "s5e1": "Live Free or Die",
        "s5e2": "Madrigal",
        "s5e3": "Hazard Pay",
        "s5e4": "Fifty-One",
        "s5e5": "Dead Freight",
        "s5e6": "Buyout",
        "s5e7": "Say My Name",
        "s5e8": "Gliding Over All",
        "s5e9": "Blood Money",
        "s5e10": "Buried",
        "s5e11": "Confessions",
        "s5e12": "Rabid Dog",
        "s5e13": "To'hajiilee",
        "s5e14": "Ozymandias",
        "s5e15": "Granite State",
        "s5e16": "Felina"
    }

    episode_title = breaking_bad_episodes[se]
    tweet_text = ''
    tweet_text += episode_title
    tweet_text += " #BreakingBad"

    # Download the random file to /tmp/ in Lambda
    download_path = f"/tmp/{os.path.basename(random_file)}"
    s3_client.download_file(bucket_name, random_file, download_path)

    # Upload the file to Twitter using Tweepy
    media = api.media_upload(download_path)

    # Create a tweet with the uploaded media
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return {
        'statusCode': 200,
        'body': f"Tweet posted with media: {random_file}"
    }
