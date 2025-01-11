#I can easily add/remove quotes by adding/remove items to the dict. That's all that's needed, the rest will be taken care of automatically
import random
import tweepy
import os

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

client = tweepy.Client(bearer_token = BEARER_TOKEN,
                                consumer_key = API_KEY, consumer_secret = API_SECRET_KEY,
                                access_token = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRET)

def postQuote(event, context):
    dict = {
        1: "Hello There",
        2: "Another Happy Landing.",
        3: "May the force be with you.",
        4: "I have a bad feeling about this.",
        5: "It's over Anakin, I have the High Ground.",
        6: "Good soldiers follow orders.",
        7: "Execute Order 66",
        8: "No, I am your father.",
        9: "Do or do not, there is no try.",
        10: "Help me Obi-Wan Kenobi. You're my only hope.",
        11: "It's a Trap!",
        12: "I am one with the Force, and the Force is with me.",
        13: "This is the way",
        14: "Long live the Empire.",
        15: "I don't like sand. It's coarse, and rough, and irritating... and it gets everywhere.",
        16: "I'm just a simple man trying to make my way in the universe.",
        17: "These are not the droids you are looking for",
        18: "That's no moon. That's a space station.",
        19: "Strike me down, and I shall become more powerful than you can possibly imagine.",
        20: "This is where the fun begins.",
        21: "Rebellions are built on hope.",
        22: "I am no Jedi.",
        23: "I am the Senate.",
        24: "I have brought Peace, Freedom, Justice, and Security to my new Empire.",
        25: "A surprise, to be sure, but a welcome one.",
        26: "I'll try spinning, that's a good trick.",
        27: "Now this is podracing.",
        28: "In my experience, there's no such thing as luck"
        # 25: "Do it.",
        #I can add more quotes here as needed,
    }

    tweet_text = dict[random.randint(1,len(dict))]
    client.create_tweet(text=tweet_text)
