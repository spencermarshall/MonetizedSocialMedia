import os
import random
import time
import tweepy
from dotenv import load_dotenv

from subpackage.CloneWarsQuotes import getCloneWarsQuote


class TwitterPoster:
    def __init__(self):
        load_dotenv()
        bearer_token = os.getenv('bearer_token')
        API_KEY = os.getenv('API_KEY')
        API_SECRET_KEY = os.getenv('API_SECRET_KEY')
        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')

        self.client = tweepy.Client(bearer_token = bearer_token,
                                        consumer_key = API_KEY, consumer_secret = API_SECRET_KEY,
                                        access_token = access_token, access_token_secret = access_token_secret)
    def randomAddSpace(self, text):
        if random.random() < 0.5:
            return " " + text
        else:
            return text

    def postCWQuote(self):

        space = ""
        probRandomSpace = random.random()
        if probRandomSpace > 0.5:
            space = " "
        tweet_text = getCloneWarsQuote(self)

        percDict = {"#StarWars ": 0.7,
                    "#swtwt ": 0.5}  # todo i can add more if i want to change probability of including a specific tag
        tagsString = f""
        tags = ["#StarWars ", "#TheCloneWars ", "#TheAcolyte ", "#StarWarsQuotes ", "#swtwt "]  # todo i can add more possible tags if desired
        for tag in tags:
            randomProb = 0.3  # each tag has 30% chance of being included unless otherwise specified
            if tag in percDict:  # pulls pre-destined probability
                randomProb = percDict[tag]
            if random.random() < randomProb:
                tagsString += tag
        tweet_text += tagsString



        try:
            # Post the tweet usin g the Client
            response = self.client.create_tweet(text=tweet_text)
            ok = 3
        except Exception as e:
            print(f"An error occurred: {e}")



# Example usage
if __name__ == "__main__":
    # random wait time, 0-24 minutes
    time.sleep(random.randint(0, 60 * 24))
    poster = TwitterPoster()
    poster.postCWQuote()