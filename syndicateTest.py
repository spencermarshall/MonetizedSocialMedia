import requests
import json
from datetime import datetime

username = "starwars"
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

# Print the tweets with their timestamps
for tweet in sorted_tweets:
    created_at = tweet["content"]["tweet"]["created_at"]
    tweet_text = tweet["content"]["tweet"]["full_text"]
    created_at_parsed = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    print(f"{created_at_parsed.strftime('%b %d, %Y %H:%M:%S %z')}: {tweet_text}")
