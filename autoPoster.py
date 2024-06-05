import tweepy

# My Credentials
API_KEY = '4DvyV5GHRJpd35XZ9dfCXIPPH'
API_SECRET_KEY = 'SNCCqXHUREJwuYSO6svmlVvbzUYZGyV5yQphuePkhr9N5f8u0c'
access_token = '1773130626134048768-cYkdSf64H0ketKDLH8E8qwtIcPrtgs'
access_token_secret = 'paLRa3fJNJRIishcVBCVhohKavqbceylkBRk7YLMv8pQ2'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFQruAEAAAAAkzMGtgA%2BgDcNhES0wLvhp5whth4%3Dq5pBHJwn7Y91cAIdmPIQAVYLWgnyFDerbrYHS2HafXVLg6N7AB'

# Initialize the tweepy.Client with the necessary credentials
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                       access_token=access_token, access_token_secret=access_token_secret)

# Define the tweet text
tweet_text = "May the force be with you, always."

# Create a tweet
try:
    # Post the tweet using the Client
    response = client.create_tweet(text=tweet_text)

    # If successful, print out the tweet details
    print("Tweet posted successfully!")
    print("Tweet ID:", response.data['id'])
    print("Tweet Text:", response.data['text'])
except tweepy.TweepyException as e:
    print("Error:", e)
