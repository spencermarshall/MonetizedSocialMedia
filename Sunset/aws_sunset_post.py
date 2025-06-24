import praw
import tweepy
import os
import json
import requests
import random
from datetime import datetime, timedelta
import boto3
from urllib.parse import urlparse

REDDIT_CLIENT_ID = 'USAgnTeY8fqGUtRtJJjNeg'
REDDIT_CLIENT_SECRET = 'oViJMoCRQxcJo6go_QVYUU5jUuGkvA'
REDDIT_USER_AGENT = 'data_bot'

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Set up Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def fetch_top_post_with_media():
    """Fetch the top post from r/cryptocurrencymemes in the last 8 hours that has valid media."""
    subreddit = reddit.subreddit('sunset')
    # Fetch top posts from the past 6 hours
    top_posts = subreddit.top(time_filter='day', limit=20)
    count = 0
    # Get current time and 6-hour threshold
    now = datetime.utcnow()
    eight_hours_ago = now - timedelta(hours=6)
    print(top_posts)

    # Loop through posts and return the first one with valid media posted within the last 8 hours
    for post in top_posts:
        count += 1
        print(f"Checked if post {count} has media")
        print(post.title)
        post_time = datetime.utcfromtimestamp(post.created_utc)
        if (not post.stickied and
                post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp')) and
                post_time >= eight_hours_ago):
            print(f"Valid post found: {post.title}, URL: {post.url}, Posted: {post_time}")
            return post

    # If no suitable post is found, return None
    print("No suitable post with media found within the last 6 hours.")
    return None


def SunsetPost(event, context):
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

            client.create_tweet(text="", media_ids=[media.media_id])
            print(f"Successfully posted: {post.title}")

            # Upload to S3 bucket "sunset.photos"
            try:
                s3 = boto3.client('s3')
                parsed_url = urlparse(post.url)
                path = parsed_url.path
                extension = os.path.splitext(path)[1]
                s3_key = f"{post.id}{extension}"
                s3.upload_file(filename, 'sunset.photos', s3_key)
                print(f"Successfully uploaded to S3: {s3_key}")
            except Exception as e:
                print(f"Error uploading to S3: {str(e)}")

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