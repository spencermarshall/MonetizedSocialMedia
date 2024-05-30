#twitter api
import tweepy


#My Credentials
API_KEY = 'FMYNXsMFBMu5SfgOEC0hA2lxF'
API_SECRET_KEY = 'RVNVnPALx141A5t5PuXkUX7K8tuD5pfO1PYSLoMuKucNH7q8rp'
access_token = '1773130626134048768-JYUK22qsQwr73cjUh8IILs0pMk8Lqc'
access_token_secret = 'zBvbWxTjjsoe1WNdwX9GSxD1qQSUDSR0cJi7M0bSg0mfA'

consumer_key = 'os9Yea8yX1HdH4DYcTHwwn4Oi'
consumer_secret = 'lNbRTOqF7emu1Ojt1zSbA3s2jd3tWvKnDZoQjIL8Bcp8aMXCwp'

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFQruAEAAAAAo7wS5V4JvD2z0mm8FQJkDiQa9XE%3DfXM6vBkQtGhRJJWUm02D8i1HcQcHX2lPngEy9FGIYSKjaspKbh'

# client = tweepy.Client(bearer_token=bearer_token,
#     consumer_key=consumer_key, consumer_secret=consumer_secret,
#     access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
#auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
#auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

# Define the tweet text
tweet_text = "May the force be with you, always."

# Create a tweet
try:
    tweet = api.update_status(status=tweet_text)



    print("Tweet posted successfully!")
    print("Tweet ID:", tweet.id)
    print("Tweet Text:", tweet.text)
except tweepy.TweepyException as e:
    print("Error:", e)