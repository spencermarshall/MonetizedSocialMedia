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
        2: "If you strike me down, and I will become more powerful than you could possibly imagine.",
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
        21: "Gonk",
        22: "I am no Jedi.",
        23: "I am the Senate.",
        24: "I have brought Peace, Freedom, Justice, and Security to my new Empire.",
        25: "A surprise, to be sure, but a welcome one.",
        26: "I'll try spinning, that's a good trick.",
        27: "Now this is podracing.",
        28: "In my experience, there's no such thing as luck",
        29: "Aren't you a little short for a storm trooper?",
        30: "Fear is the path to the dark side. Fear leads to anger, anger leads to hate, hate leads to suffering.",
        31: "These are not the droids you're looking for.",
        32: "I find your lack of faith disturbing.",
        33: "The ability to speak does not make you intelligent.",
        34: "So this is how liberty dies... with thunderous applause.",
        35: "Only a Sith deals in absolutes.",
        36: "I sense a plot to destroy the Jedi.",
        37: "Let the past die. Kill it, if you have to.",
        38: "Insolence!? We are pirates! We don’t even know what that means.",
        39: "I can bring you in warm, or I can bring you in cold.",
        40: "I have spoken.",
        41: "I'm a Mandalorian. Weapons are part of my religion.",
        42: "Jabba ruled with fear. I intend to rule with respect.",
        43: "The mission. The nightmares. They're... finally... over.",
        44: "In my book, experience outranks everything.",
        45: "We're just clones, sir. We're meant to be expendable.",
        46: "Clones, bred for combat. All part of the plan... THE Plan. The only Plan that matters. Not even I was made aware of its grand design, but I played my part. And do you know what happened to me? I was cast aside. I was forgotten. But I survived, and I can thrive in the chaos that is to come.",
        47: "There is no justice, now law, no order... except for the one that will replace it!",
        48: "As a Jedi, we were trained to be keepers of the peace, not soldiers. But all I've been since I was a Padawan is a soldier.",
        49: "You're a good soldier Rex. So is every one of those men down there. They may be willing to die, but I am not the one who is going to kill them.",
        50: "Do it.",

    }

    tweet_text = dict[random.randint(1,len(dict))]
    client.create_tweet(text=tweet_text)
