import praw
import tweepy
import os
import json
import random
import requests
from datetime import datetime, timedelta

# Reddit API Credentials

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
    subreddit = reddit.subreddit('HarryPotterMemes')
    top_posts = subreddit.top(time_filter='day', limit=20)  # Fetch top posts from the past hour
    count = 0
    # Loop through posts and return the first one with valid media
    for post in top_posts:
        count += 1
        print(f"Checked if post {count} has media")

        if post.over_18:
            print(f"Skipping NSFW post: {post.title}")
            continue

        if not post.stickied and post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp')):
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

            link = post.shortlink
            link = link.replace("i", "𝗂", 1)
            link = link[8:]

            tweet_text = f"{text}"  # {link}"

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

