import random
import tweepy
import os

lotr_api_key = 'placeholder'
lotr_api_key_secret = 'placeholder'
lotr_bearer_token = 'placeholder'
lotr_access_token = 'placeholder'
lotr_access_token_secret = 'placeholder'


client = tweepy.Client(bearer_token = lotr_bearer_token,
                                consumer_key = lotr_api_key, consumer_secret = lotr_api_key_secret,
                                access_token = lotr_access_token, access_token_secret = lotr_access_token_secret)

def post_lotr_quote(event, context):
    lotr_quotes = {
        0: "\"Text quote.\" -name",
    }

    tweet_text = lotr_quotes[random.randint(0,len(lotr_quotes)-1)]

    #identify if lotr or hobbit for hashtag, might be possible.
    tweet_text += " #LordOfTheRings" #verify this is best hashtag
    tweet_text += " #TheHobbit" #verify this is best hashtag
    client.create_tweet(text=tweet_text)
