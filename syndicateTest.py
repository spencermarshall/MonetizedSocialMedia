import requests
import json
from datetime import datetime

username = "elonmusk"
url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"

r = requests.get(url)
html = r.text

start_str = '<script id="__NEXT_DATA__" type="application/json">'
end_str = '</script></body></html>'

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

# Print the 3 most recent tweets
for tweet in sorted_tweets[:3]:
    print(tweet["content"]["tweet"]["full_text"])

