import praw
import tweepy
import os
import json
import requests
import random
from datetime import datetime, timedelta
import time

# Reddit API Credentials
# REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
# REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
# REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
REDDIT_CLIENT_ID = 'USAgnTeY8fqGUtRtJJjNeg'
REDDIT_CLIENT_SECRET = 'oViJMoCRQxcJo6go_QVYUU5jUuGkvA'
REDDIT_USER_AGENT = 'data_bot'


# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)





def fetch_top_post_with_media():
    """Fetch the top post from r/marvelmemes in the last 6 hours that has valid media."""
    subreddit = reddit.subreddit('marvelmemes')
    recent_posts = subreddit.new(limit=30)  # Fetch recent posts to cover at least 6 hours
    now = time.time()
    six_hours_ago = now - (24 * 3600)  # Calculate timestamp for 6 hours ago

    # Filter posts: within 6 hours, not NSFW, not stickied, and has valid media
    eligible_posts = [
        post for post in recent_posts
        if post.created_utc >= six_hours_ago
        and not post.over_18
        and not post.stickied
        and post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp'))
    ]

    if eligible_posts:
        # Select the post with the highest score
        top_post = max(eligible_posts, key=lambda p: p.score)
        print(f"Valid post found: {top_post.title}, URL: {top_post.url}")
        return top_post
    else:
        print("No suitable post with media found in the last 6 hours.")
        return None

def lambda_handler(event, context):
    def post_to_twitter(post):
        try:
            # Download media from the post URL
            filename = '/tmp/temp_media'
            response = requests.get(post.url, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)

            # Upload media to Twitter
            media = api.media_upload(filename)
            text = post.title

            # Clean the title by removing brackets if present
            if post.title[0] == '[':
                text = post.title[4:]
            if post.title[-1] == ']':
                text = post.title[:len(post.title)-4]

            tweet_text = f"{text}"
            print(f"Posting to Twitter: {tweet_text}")
            client.create_tweet(text=text, media_ids=[media.media_id])
            print(f"Successfully posted: {post.title}")
        except tweepy.errors.TweepyException as e:
            print("An error occurred while posting to Twitter.")
            if hasattr(e, 'response') and e.response is not None:
                print("HTTP Status Code:", e.response.status_code)
                print("Reason:", e.response.reason)
                try:
                    error_details = e.response.json()
                    print("Error Details:", json.dumps(error_details, indent=4))
                except Exception as json_error:
                    print("Error while parsing response JSON:", json_error)
            else:
                print("No response object available in the exception.")
            print("Error Message:", str(e))
        except requests.exceptions.RequestException as e:
            print("An error occurred while downloading media.")
            print("Error Type:", type(e).__name__)
            print("Error Message:", str(e))
        except Exception as e:
            print("An unexpected error occurred.")
            print("Error Type:", type(e).__name__)
            print("Error Message:", str(e))

    post = fetch_top_post_with_media()
    if post:
        post_to_twitter(post)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Posted: {post.title}")
        }
    else:
        print("No suitable post with media found.")
        return {
            'statusCode': 200,
            'body': json.dumps('No suitable post with media found.')
        }


















