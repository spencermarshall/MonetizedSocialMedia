import tweepy
import os
import random
import requests
from datetime import date

#the real keys are on aws, these are placeholders for being on a public repo
API_KEY = 'placeholder'
API_SECRET_KEY = 'placeholder'
access_token = 'placeholder'
access_token_secret = 'placeholder'
bearer_token = 'placeholder'
consumer_key = 'placeholder'
consumer_secret = 'placeholder'

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token = bearer_token,
    consumer_key = API_KEY,
    consumer_secret = API_SECRET_KEY,
    access_token = access_token,
    access_token_secret = access_token_secret
)
def dailyHelloThere(event, context):
    start_date = date(2024, 7, 1)
    today_date = date.today()
    days_since_target = (today_date - start_date).days
    name = "Kenobi"
    probFirstName = random.random()
    if probFirstName > 0.5:
        name = "Obi-Wan Kenobi"
    tweet_text = f"Day {days_since_target} of posting {name}'s \"Hello there\" from Star Wars Episode 3: Revenge of the Sith "
    #hashtags
    percDict = {
        "#StarWars ": 0.25,
                }  # todo i can add more if i want to change probability of including a specific tag
    tagsString = f""
    tags = ["#StarWars ", "#Kenobi ", "#Obiwan ", "#hellothere ",
            "#swtwt "]  # todo i can add more possible tags if desired
    for tag in tags:
        randomProb = 0.10  # each tag has 10% chance of being included unless otherwise specified
        if tag in percDict:  # pulls pre-destined probability
            randomProb = percDict[tag]
        if random.random() < randomProb:
            tagsString += tag
    tweet_text += tagsString

    # Media URL
    media_url = 'https://raw.githubusercontent.com/spencermarshall/StarWarsTwitterPost/main/images/helloThere.gif'
    temp_filename = '/tmp/temp_media.gif'

    # Download the media
    response = requests.get(media_url)
    if response.status_code == 200:
        # Save the content to the temporary file
        with open(temp_filename, 'wb') as f:
            f.write(response.content)

        # Upload the media using Tweepy
        media = api.media_upload(temp_filename)

        # Post the tweet with the media
        client.create_tweet(text=tweet_text, media_ids=[media.media_id])

        # Remove the temporary file
        os.remove(temp_filename)
    else:
        print("Failed to download media")


