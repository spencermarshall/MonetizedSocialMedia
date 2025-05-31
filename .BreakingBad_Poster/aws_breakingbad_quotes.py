import requests
import random
import tweepy

# These are placeholders so my keys won't be on a public github repo

api_key = 'm5GPo8zjDkAuWMuZhjTM2ksJu'
api_key_secret = 'iBt6OHUdCkq88fvwNVFsnuxL7CAU4avLzemUyU97aP18IWFZmS'
access_token = '1837346181229563904-49LOpBdittQOb1hHkrEMRk5mzhVXFU'
access_token_secret = 'HsPyF7XRBkfkhXI0sHUBZRKboPWTgtPRCy7fkHfy65bhU'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAANbewAEAAAAA2dsHWBhQRdWJwY6OhKfhja6fKOY%3DShBe6NotqhviLUXh3tjd2tZIa0rAkPvK654vNKcP93mV5OPIiq'

# Set up Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)


# here

def post_bb_quote(event, context):
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
        27: "This Whole Thing, All Of This... It's All About Me.",
        28: "I won.",
        29: "This is not Meth...",
        30: "If You Believe That There's A Hell, I Don't Know If You're Into That, We're Already Pretty Much Going There, Right? -Walter White",
        31: "If You Don’t Know Who I Am, Then Maybe Your Best Course Would Be To Tread Lightly.",
        32: "Say my name.",
        33: "TIGHT TIGHT TIGHT",
        34: "I am the one who knocks",
        35: "Let's cook.",
    }

    tweet_text = breaking_bad_quotes[random.randint(1, len(breaking_bad_quotes))]

    client.create_tweet(text=tweet_text)

