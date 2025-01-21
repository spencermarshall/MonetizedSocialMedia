import random
import boto3
import tweepy
import os

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


def SW_question(event, context):
    dict = {
        0: "What are your thoughts on Star Wars Rebels?",
        1: "What is your favorite Star Wars movie?",
        2: "Who is your favorite Star Wars character?",
        3: "What is your favorite Star Wars quote?",
        4: "What is your favorite Star Wars planet?",
        5: "What is your favorite Star Wars species?",
        6: "What is your favorite Star Wars ship?",
        7: "What is your favorite Star Wars game?",
        8: "Have you read any of the Star Wars books? Legends or Disney Canon?",
    }
    # dictionary, 1000 questions open ended to cause discussion, conversation, and engagement

    # pull question/id

    # while question is in 50 most recent, pick a new question

    # post tweet question
    client.create_tweet(text="hey")

    # update 50 most recent dynamo DB, FIFO so it keeps track of 50 most recent questions/id
