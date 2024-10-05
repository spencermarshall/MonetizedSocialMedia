#this code is working on AWS lambda and schedule for 8am, 2pm, 8pm everyday
# posts to the account at https://x.com/_TheOfficeDaily
import requests
import tweepy

# URL for the random quote endpoint
url = "https://officeapi.akashrajpurohit.com/quote/random"

# These are placeholders so my keys won't be on a public github repo
bearer_token = 'placeholder'
api_key = 'placeholder'
api_key_secret = 'placeholder'
access_token = 'placeholder'
access_token_secret = 'placeholder'

# Set up Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)


def get_random_quote(event, context):
    response = requests.get(url)
    data = response.json()
    #can pass id if i want to skip, idk how to easily find the id if i want to not post a quote, if needed probably just search for quote text exact
    # while (data['id'] == -1 or data['id'] == -1):
    #     response = requests.get(url)
    #     data = response.json()
    tweet_text = f"\"{data['quote']}\" -{data['character']}\n#TheOffice"
    # Tweet the quote
    client.create_tweet(text=tweet_text)


