import praw
import tweepy
import os
import json
import requests
from datetime import datetime, timedelta

# Reddit API Credentials
# REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
# REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
# REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
REDDIT_CLIENT_ID = 'USAgnTeY8fqGUtRtJJjNeg'
REDDIT_CLIENT_SECRET = 'oViJMoCRQxcJo6go_QVYUU5jUuGkvA'
REDDIT_USER_AGENT = 'data_bot'

# Twitter API Credentials
# TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
# TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
# TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
# TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
# TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
api_key = '8DV6yFr7lt5ydelNdMeM9Aic4'
api_secret_key = '5j6fsAt5kqcLCUZNwzLqLBZptYIHMLKU6jxDYEDXfMg1j0NrfA'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAABn6xAEAAAAA8EZ2zBWtzcFYVz8mF%2B7w7nkH6xU%3DzXEIZcuGmrzr352DCgLUZ1mjFgDDKEPR2NcaLBu6KZOQWEVREp'
access_token = '1796617595522531329-OGwRWV450HKxsJD3sRUMVIYdhHasG8'
access_token_secret = 'IBSHdPrNHLZKLSBRwLlVZ49sa1ZVl6hNCZ8Hmz3aqPBKj'
client_id = 'WWV6ZXI1RVlrVGkwaTRxeXc4STE6MTpjaQ'
client_secret = 'pXQs8EoHDiMoa63J4JCK4x2qt-OV6YTJLYDVoFx65h4C2TbZoi'

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)
client = tweepy.Client(bearer_token=bearer_token,
    consumer_key=client_id, consumer_secret=client_secret, #client id and client_secret might be incorrect, im not sure it was labeled as something else, if it's not working look at how this compares to elias's code
    access_token=access_token, access_token_secret=access_token_secret
)

# Initialize Twitter API
auth = tweepy.OAuth1UserHandler(
    client_id,
    client_secret,
    access_token,
    access_token_secret
)
api = tweepy.API(auth)


def fetch_top_post():
    """Fetch the top post from r/funny in the last 2 hours."""
    subreddit = reddit.subreddit('dataisbeautiful')
    top_posts = subreddit.top(time_filter='hour', limit=50)  # Fetch top posts from the past hour
    best_post = None
    highest_score = -1
    for post in top_posts:
        if not post.stickied and (datetime.utcnow() - datetime.utcfromtimestamp(post.created_utc)) < timedelta(hours=2):
            print(f"Title: {post.title}, Score: {post.score}, Post Shortlink: {post.shortlink}")
            if post.score > highest_score:
                best_post = post
                highest_score = post.score
    return best_post

def post_to_twitter(post):
    """Post content to Twitter."""
    if post.url.endswith(('jpg', 'jpeg', 'png', 'gif', 'mp4')):
        media_file = post.url
        try:
            filename = '/tmp/temp_media'
            # Download media
            with open(filename, 'wb') as file:
                file.write(requests.get(media_file).content)

            # Post image or video to Twitter
            media = api.media_upload(filename)
            client.create_tweet(text=f"{post.title}\n{post.shortlink}", media_ids=[media.media_id])
            print(f"Posted to Twitter: {post.title}")
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
    else:
        # Post text if no suitable media is found
        client.create_tweet(text=f"{post.title}\n{post.shortlink}")
        print(f"Posted to Twitter (Text): {post.title}")

def lambda_handler(event, context):

    post = fetch_top_post()
    if post:
        post_to_twitter(post)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Posted: {post.title}")
        }
    else:
        print("No suitable post found.")
        return {
            'statusCode': 200,
            'body': json.dumps('No suitable post found.')
        }