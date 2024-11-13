import warnings
warnings.filterwarnings('ignore')
import tweepy

API_KEY = 'oBacdNpL8LB50kw8ZcPNIy5e7'
API_SECRET_KEY = 'rwjBwFW2v6FbNIOG1ua3U7NtJm1SZqSv93e1uE0ucDSggeAWF8'
access_token = '1798497258469564416-TgvOwczwFOyfwVVQitf0B7u0kXzEP7'
access_token_secret = 'kZ1WLWeJHKeV3EbnJptyeASuMa91H15U9jUMgRqAMEm7Y'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAADGfuAEAAAAAiKXhRiJILcmDv54r2LVG8PpizMU%3DOveJUzcf8xrH2G1uL32SFFG1WAj0s1He8Wf75y4lYUX0jcOj1K'
consumer_key = 'WU92SWwzN0xuemN0OTZvcFZOWHg6MTpjaQ'
consumer_secret = 'eNAjt3FkHSJOJHd6VzDetZrTIhuKP52d_yKtl3RRIFQBv0HInn'

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token = bearer_token,
    consumer_key = API_KEY,
    consumer_secret = API_SECRET_KEY,
    access_token = access_token,
    access_token_secret = access_token_secret
)
tweet_id = '1855336897721348479'
reply_text = 'test'

client.create_tweet(
    text=reply_text,  # The content of your reply tweet
    in_reply_to_tweet_id=tweet_id  # The ID of the tweet you're replying to
)