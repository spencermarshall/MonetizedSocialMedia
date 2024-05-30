#twitter api
import tweepy


#My Credentials, these are fake variables, the real with real values are stored in github secret variables
API_KEYFake = None
API_SECRET_KEYFake = None
ACCESS_TOKENFake = None
ACCESS_TOKEN_SECRETFake = None


# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Create a tweet
tweet = "May the force be with you, always"

# Post the tweet
try:
    api.update_status(status=tweet)
    print("Tweet posted successfully!")
except tweepy.TweepError as e:
    print(f"Error: {e.reason}")
