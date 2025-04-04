import os
import random
import boto3
import tweepy
from datetime import date

# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)


def dailyHelloThere(event, context):
    # 1) Calculate the day count since your start date
    start_date = date(2024, 7, 1)
    today_date = date.today()
    days_since_target = (today_date - start_date).days

    s3 = boto3.client('s3')
    bucket_name = 'starwars.gifs'
    ep3_hellothere = 'hellothere/helloThere.gif'
    temp_filename = '/tmp/temp_media.gif'

    name = "Kenobi"
    if random.random() < 0.5:
        name = "Obi-Wan Kenobi"

    title = " Star Wars Episode 3: Revenge of the Sith "

    if random.random() < 0.2:
        title = " Star Wars Episode 3: ROTS"
    question_ran = random.randint(1,
                                  9)  # 9 because purposely leave some blank so i don't overwhelm by asking question every time
    if question_ran == 1:
        title += "\n\nDo you like how Kenobi saying \"Hello there\" has become a meme?"
    elif question_ran == 2:
        title += "\n\nDo you enjoy Ewan McGregor as Kenobi?"
    elif question_ran == 3:
        title += "\n\nDo you think it was smart he gave up the high ground just to say this?"
    elif question_ran == 4:
        title += "\n\nWhy did this become a meme? lol"
    elif question_ran == 5:
        title += "\n\nDo you always respond with \"General Kenobi\"?"
    elif question_ran == 6:
        title += "\n\nIs this the best part of Ep 3?"
    posting = "posting"
    if random.random() < 0.15:
        posting = "tweeting"

    letter = "D"
    if random.random() < 0.25:
        letter = "d"

    ran_clip = random.random()
    if ran_clip < 0.2:
        ep3_hellothere = 'hellothere/hellothere_1.gif'
        title = " Star Wars Episode 4: A New Hope.\n\n"
        question_ran = random.randint(1,
                                      8)  # 8 because purposely leave some blank so i don't overwhelm by asking question every time
        if question_ran == 1:
            title += "Did you enjoy Sir Alec Guinness as Ben Kenobi?"
        elif question_ran == 2:
            title += "Do you think Ben Kenobi aged too much since Episode 3 or Kenobi Series?"
        elif question_ran == 3:
            title += "Since Tatooine has 2 suns do people age twice as fast there?"
        elif question_ran == 4:
            title += "When did you learn this was the original \"Hello there\"?"
        elif question_ran == 5:
            title += "Do you think Obi-Wan will ever say this again in Canonical Star Wars?"

    elif ran_clip < 0.5:
        ep3_hellothere = 'hellothere/hellothere_2.gif'
        title = " the Kenobi Series.\n\n"
        question_ran = random.randint(1,
                                      9)  # 9 because purposely leave some blank so i don't overwhelm by asking question every time
        if question_ran == 1:
            title += "Did you enjoy the return of Ewan McGregor in the Kenobi Series?"
        elif question_ran == 2:
            title += "What did you like most about the Kenobi Series?"
        elif question_ran == 3:
            title += "What did you like least about the Kenobi Series?"
        elif question_ran == 4:
            title += "Did you think it was forced fan service for him to say this line at the end of the Kenobi Series?"
        elif question_ran == 5:
            title += "Do you think Obi-Wan will ever say this again in Canonical Star Wars?"
        elif question_ran == 6:
            title += "Do you think Ewan McGregor will return as Obi-Wan Kenobi again?"

    tweet_text = (
        f"{letter}ay {days_since_target} of {posting} {name} saying \"Hello there\" this time from{title} "
    )

    r = random.random()
    if r < 0.04:
        tweet_text += "#swtwt"
    elif r < 0.06:
        tweet_text += "#StarWars"
    elif r < 0.065:
        tweet_text += "#Kenobi"
    elif r < 0.07:
        tweet_text += "#Obiwan"
    elif r < 0.075:
        tweet_text += "#hellothere"

    try:
        s3.download_file(bucket_name, ep3_hellothere, temp_filename)
    except Exception as e:
        print(f"Failed to download {ep3_hellothere} from S3: {e}")
        return  # Exit if we cannot get the file

    media = api.media_upload(temp_filename)
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    os.remove(temp_filename)
