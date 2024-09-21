import requests
import random
import tweepy
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

# URL for the random quote endpoint
url = "https://api.breakingbadquotes.xyz/v1/quotes"

# List of words to replace and their replacements
words_to_replace = {
    'ass': 'a*s',
    'hell': 'h*ll',
    'damn': 'd*mn',
    'shit': 'sh*t',
    'fuck': 'f*ck',
    'bitch': 'b*tch',
    'masturbating': 'm******g',
}


def post_quote(event, context):
    response = requests.get(url)

    if response.status_code != 200:
        return
    data = response.json()[0]  # The API returns a list with one quote
    quote = data['quote']

    # Loop through the list of words and replace them
    for word, replacement in words_to_replace.items():
        if word in quote.lower():
            quote = quote.replace(word, replacement)

    tweet_text = f"\"{quote}\" -{data['author']} "
    tagsString = f""
    tags = ["#BreakingBad "]  #i can add more possible tags if desired
    for tag in tags:
        randomProb = 0.20  # each tag has 20% chance of being included unless otherwise specified
        if random.random() < randomProb:
            tagsString += tag
    tweet_text += tagsString
    client.create_tweet(text=tweet_text)

# Call the function to get and print a random quote
post_quote(1,2)
