import praw
import tweepy
import os
import json
import random
import requests
from datetime import datetime, timedelta
import time


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
api_key = 'og4HjXRYmKAzHHTYP0xFJ6D3q'
api_key_secret = 'k3axIzwG18PAVUCmgg2Wwzatc29aiUdvrXy6UIlzMbcESucNj5'
client_id = 'ZlBDcWxWaUdWeE9RbjFWYTJDams6MTpjaQ'
client_secret = 'E0tGd957j87G_J42aAcazaZsZeoE0TkT0ad-U7FS4DVZ36lPw7'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHmDwgEAAAAAdta3NLjsPDs4piYh6cUKNw%2B1WU0%3D4jUmVHUEhaKI6RzDxhk26HNHINjq1YCk4zmavEPSpJMvTatlHx'
access_token = '1849619632052961280-xUY3pvEPa9v0ye2ZMxtoKavSj6j2oh'
access_token_secret = 'iaTq7GcUqkLU0aBJEX4N1Je59ppJ3xRydUlZCgRtsa87X'

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)
client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=api_key, consumer_secret=api_key_secret,
                           access_token=access_token, access_token_secret=access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)


def fetch_top_post_with_media():
    """Fetch the top post from r/HarryPotterMemes in the last 6 hours that has valid media."""
    subreddit = reddit.subreddit('HarryPotterMemes')
    posts = list(subreddit.new(limit=30))  # Fetch the 100 most recent posts
    now = time.time()
    six_hours_ago = now - 6 * 3600
    eligible_posts = [
        post for post in posts
        if post.created_utc > six_hours_ago
        and not post.over_18
        and not post.stickied
        and post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp'))
    ]
    if eligible_posts:
        top_post = max(eligible_posts, key=lambda p: p.score)
        print(f"Valid post found: {top_post.title}, URL: {top_post.url}")
        return top_post
    else:
        print("No suitable post with media found in the last 6 hours.")
        return None

def post_to_twitter(post):
    try:
        # Download media
        filename = '/tmp/temp_media'
        response = requests.get(post.url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)

        # Upload media to Twitter
        media = api.media_upload(filename)
        text = post.title
        # Clean title by removing square brackets if present
        if text.startswith('[') and ']' in text:
            text = text[text.index(']')+1:].strip()
        tweet_text = f"{text}"

        print(f"Posting to Twitter: {tweet_text}")
        client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        print(f"Successfully posted: {post.title}")
    except tweepy.errors.TweepyException as e:
        print(f"Twitter posting error: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Media download error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def lambda_handler(event, context):
    post = fetch_top_post_with_media()
    if post:
        post_to_twitter(post)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Posted: {post.title}")
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('No suitable post with media found in the last 6 hours.')
        }