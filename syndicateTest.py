import requests
import json
from datetime import datetime, timezone, timedelta

def print_recent_tweets(username, num_tweets):
    url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"

    r = requests.get(url)
    html = r.text

    start_str = '<script id="__NEXT_DATA__" type="application/json">'
    end_str = '</script>'

    start_index = html.index(start_str) + len(start_str)
    end_index = html.index(end_str, start_index)

    json_str = html[start_index: end_index]
    data = json.loads(json_str)

    # Extract tweets
    tweets = data["props"]["pageProps"]["timeline"]["entries"]

    # Function to parse tweet creation date
    def parse_tweet_date(tweet):
        date_str = tweet["content"]["tweet"]["created_at"]
        return datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')

    # Sort tweets by creation date in descending order
    sorted_tweets = sorted(tweets, key=parse_tweet_date, reverse=True)

    # Get current time
    now = datetime.now(timezone.utc)

    # Print the specified number of most recent tweets with their timestamps and tweet IDs
    for tweet in sorted_tweets[:num_tweets]:
        tweet_id = tweet["content"]["tweet"]["id_str"]
        created_at = tweet["content"]["tweet"]["created_at"]
        tweet_text = tweet["content"]["tweet"]["full_text"]
        created_at_parsed = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
        formatted_date = created_at_parsed.strftime('%b %d, %Y %H:%M:%S %z')

        # Check if the tweet was made within the last 24 hours
        is_recent = (now - created_at_parsed) <= timedelta(days=1)
        recent_status = "Recent: True" if is_recent else "Recent: False"

        print(f"ID: {tweet_id}\n{formatted_date}:\n{tweet_text}\n{recent_status}\n")

# Example usage
print_recent_tweets("youtube", 5)
