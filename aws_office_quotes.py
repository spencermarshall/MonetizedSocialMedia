import random
import tweepy

API_KEY = ''
API_SECRET_KEY = ''
access_token = ''
access_token_secret = ''
bearer_token = ''

client = tweepy.Client(bearer_token = bearer_token,
                                consumer_key = API_KEY, consumer_secret = API_SECRET_KEY,
                                access_token = access_token, access_token_secret = access_token_secret)


def PostQuote(event, context):


    tweet_text = dict[random.randint(1,len(dict))]

    percDict = {"#StarWars ": 0.4,
                "#swtwt ": 0.25,
                "#StarWarsQuotes ": 0.05}  # todo i can add more if i want to change probability of including a specific tag
    tagsString = f""
    tags = ["#StarWars ", "#StarWarsQuotes ",
            "#swtwt "]  # todo i can add more possible tags if desired
    for tag in tags:
        randomProb = 0.3  #each tag has 30% chance of being included unless otherwise specified
        if tag in percDict:  # pulls pre-destined probability
            randomProb = percDict[tag]
        if random.random() < randomProb:
            tagsString += tag
    tweet_text += tagsString
    client.create_tweet(text=tweet_text)

