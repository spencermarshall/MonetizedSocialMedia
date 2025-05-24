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

# Twitter API Credentials
# TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
# TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
# TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
# TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
# TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
api_key = 'F2qNzaY8nFfo2xL2jQovqPhFP'
api_key_secret = 'kDNIb2yTBUyu1vuw8lpodMwQYdSUetdT1H5J68dUsLlA8vHOfT'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOT6vwEAAAAAvWmz9YdCrQgdmBuwQQMLIxuLeXw%3DQH4mvTQ0GvnWWsDetTrR7BDnRxWc6OLfP2ThqBJlwoMAAmNbzt'
access_token = '1834727038022041601-wWnXmXkoJDQBrXBvrbXwNPZv9W2P87'
access_token_secret = 'w5x7yOkgbnQGE5s5oMkmoxVYCCXfVR13z6hjc9j3PJrm0'

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
    """Fetch the top post from r/dataisbeautiful in the last 1 hour that has valid media."""
    subreddit = reddit.subreddit('marvelmemes')
    top_posts = subreddit.top(time_filter='day', limit=10)  # Fetch top posts from the past hour
    count = 0

    now = time.time()  # Get current time in Unix timestamp
    twelve_hours_ago = now - (24 * 3600)  # Subtract 24 hours

    count = 0
    for post in top_posts:
        count += 1
        post_time = post.created_utc  # Get post's Unix timestamp
        print(f"Checked if post {count} has media. Posted at {datetime.utcfromtimestamp(post_time)} UTC")
        if post.over_18:
            print(f"Skipping post {idx} titled '{post.title}' because it is marked as NSFW.")
            continue

        # Ensure the post is within the last 12 hours and contains media
        if post_time >= twelve_hours_ago and not post.stickied and post.url.endswith(
                ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp')):
            print(f"Valid post found: {post.title}, URL: {post.url}")
            return post

    # If no suitable post is found, return None
    print("No suitable post with media found.")
    return None


def lambda_handler(event, context):
    def post_to_twitter(post):
        try:
            # Check if the post URL points to valid media
            filename = '/tmp/temp_media'
            # Download media
            response = requests.get(post.url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            with open(filename, 'wb') as file:
                file.write(response.content)

            # Post image or video to Twitter
            media = api.media_upload(filename)
            text = post.title
            if post.title[0] == '[':
                text = post.title[4:]
            if post.title[-1] == ']':
                text = post.title[:len(post.title) - 4]

            tweet_text = ""

            link = post.shortlink
            link = link.replace("i", "𝗂", 1)

            tweet_text = f"{text}"  # {link[8:]}"

            print(f"Posting to Twitter: {tweet_text}")
            client.create_tweet(text=tweet_text, media_ids=[media.media_id])
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




















