
def DailyHelloThere():
    import json
    import tweepy
    import os
    import random
    import requests  # Import requests for downloading the file

    from dotenv import load_dotenv
    from pathlib import Path
    from datetime import date
    # Initialize an empty log string
    log = ""

    # Load environment variables
    load_dotenv()

    # Your Twitter API credentials
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    API_KEY = os.getenv('API_KEY')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    # Paths to your GIF file and count file
    local_gif_path = '/tmp/helloThere.gif'
    count_file = '/tmp/countDailyHelloThere.txt'

    # Authenticate to Twitter using Client for v2 API
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    # Authenticate to Twitter using OAuth1UserHandler for media upload (v1.1)
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    def download_file(url, local_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as file:
                file.write(response.content)
            return True
        else:
            return False

    try:

        gif_url = "https://github.com/spencermarshall/StarWarsTwitterPost/raw/main/images/helloThere.gif"
        success = download_file(gif_url, local_gif_path)
        if success:
            log += "Successfully downloaded GIF.\n"
        else:
            log += "Failed to download GIF.\n"
            raise Exception("Failed to download GIF")

        # Upload the media to Twitter
        media = api.media_upload(local_gif_path)
        log += f"Media uploaded successfully! Media ID: {media.media_id}\n"

        # Calculate the number of days since 2024-07-01
        count = (date.today() - date(2024, 7, 1)).days
        log += f"Count of days since 2024-07-01: {count}\n"

        # Generate the tweet text
        name = "Kenobi"
        space = ""
        probFirstName = random.random()
        probRandomSpace = random.random()
        if probFirstName > 0.5:
            name = "Obi-Wan Kenobi"
        if probRandomSpace > 0.5:
            space = " "
        tweet_text = f"Day {count} of posting {name}'s \"Hello there\" from Star Wars{space} Episode 3: Revenge of the Sith "

        percDict = {"#StarWars ": 0.8, "#swtwt ": 0.6}
        tagsString = ""
        tags = ["#StarWars ", "#Kenobi ", "#Obiwan ", "#hellothere ", "#swtwt "]
        for tag in tags:
            randomProb = 0.15
            if tag in percDict:
                randomProb = percDict[tag]
            if random.random() < randomProb:
                tagsString += tag
        tweet_text += tagsString
        log += f"Generated tweet text: {tweet_text}\n"

        # Execute tweet
        client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        log += "Tweet posted successfully!\n"
        print(log)

    except Exception as e:
        log += f"An error occurred: {e}\n"

    return {
        'statusCode': 200,
        'body': json.dumps(log)
    }

if __name__ == "__main__":
    poster = DailyHelloThere()
    # start_date = date(2024, 7, 1)
    # today_date = date.today()
    # days_since_target = (today_date - start_date).days
