#I can easily add/remove quotes by adding/remove items to the dict. That's all that's needed, the rest will be taken care of automatically
#Right now this is scheduled with working api keys on aws Lambda and is scheduled to post once a day at 6pm MDT, and will be offset by 1 hour when we are not on Daylight time
import random
import tweepy

#the real api keys are working in the AWS lambda function, i just don't want them on a github repo
API_KEY = 'placeholder'
API_SECRET_KEY = 'placeholder'
access_token = 'placeholder'
access_token_secret = 'placeholder'
bearer_token = 'placeholder'
consumer_key = 'placeholder'
consumer_secret = 'placeholder'
client = tweepy.Client(bearer_token = bearer_token,
                                consumer_key = API_KEY, consumer_secret = API_SECRET_KEY,
                                access_token = access_token, access_token_secret = access_token_secret)

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
        19: "Strike me dow, and I shall become more powerful than you can possibly imagine.",
        20: "This is where the fun begins.",
        21: "Rebellions are built on hope.",
        22: "I am no Jedi.",
        23: "I am the Senate.",
        24: "I have brought Peace, Freedom, Justice, and Security to my new Empire.",
        25: "Do it.",
        26: "A surprise, to be sure, but a welcome one.",
        27: "I'll try spinning, that's a good trick.",
        28: "Now this is podracing.",
        29: "In my experience, there's no such thing as luck"
        #I can add more quotes here as needed,
    }
    tweet_text = dict[random.randint(1,len(dict))]
    client.create_tweet(text=tweet_text)


