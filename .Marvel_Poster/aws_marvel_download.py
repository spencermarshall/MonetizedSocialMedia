import praw
import tweepy
import os
import boto3
import json
import requests
import random
from datetime import datetime, timedelta
import time


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

# Initialize S3 client
s3 = boto3.client('s3')


def get_media_count(post):
    """
    Returns the number of media images attached to a post.
    For gallery posts, count the number of items.
    For non-gallery posts, count as 1 if the URL ends with a valid media extension.
    """
    if hasattr(post, "is_gallery") and post.is_gallery:
        try:
            # Count the items in the gallery
            return len(post.gallery_data['items'])
        except Exception as e:
            return 0
    else:
        # Check if the URL has a valid image/video extension
        if post.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp')):
            return 1
        else:
            return 0


def add_to_s3(post):
    """
    Downloads the media from the post URL and uploads it to the S3 bucket 'marvel.photos'.
    """
    try:
        response = requests.get(post.url, stream=True)
        if response.status_code == 200:
            content = response.content
            # Extract the file extension from the URL
            ext = post.url.split('.')[-1]
            # Create a filename using the post id and extension
            filename = f"{post.id}.{ext}"
            # Upload the content to the S3 bucket
            s3.put_object(Bucket="marvel.photos", Key=filename, Body=content)
        else:
            print(f"Failed to download media from {post.url} (status code: {response.status_code})")
    except Exception as e:
        print("Error in add_to_s3:", str(e))


def marvel_download(event, context):
    """
    Lambda function handler:
    - Reads top 10 posts from 'marvelmemes' subreddit for the past week.
    - Skips posts marked as NSFW.
    - Checks if the post URL ends with a valid image extension (.jpg, .jpeg, .png, .gif, .webp).
    - Uploads the image to the S3 bucket if it meets the criteria.
    """
    subreddit = reddit.subreddit('marvelmemes')
    top_posts = subreddit.top(time_filter='week', limit=3)

    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

    for idx, post in enumerate(top_posts, start=1):
        # Check if the post is marked as NSFW and skip if so
        if post.over_18:
            continue

        # Check if the URL ends with one of the allowed image extensions
        if post.url.lower().endswith(allowed_extensions):
            add_to_s3(post)
        else:
            print(
                f"Skipping post {idx} titled '{post.title}' because the URL does not end with a valid image extension.")

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete.')
    }