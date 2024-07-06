# import requests
# import json
# from datetime import datetime, timezone, timedelta
#
# def print_recent_tweets(username, num_tweets):
#     url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"
#
#     r = requests.get(url)
#     html = r.text
#
#     start_str = '<script id="__NEXT_DATA__" type="application/json">'
#     end_str = '</script>'
#
#     start_index = html.index(start_str) + len(start_str)
#     end_index = html.index(end_str, start_index)
#
#     json_str = html[start_index: end_index]
#     data = json.loads(json_str)
#
#     # Check if the data structure is correct
#     if "props" in data and "pageProps" in data["props"] and "timeline" in data["props"]["pageProps"]:
#         # Extract tweets
#         tweets = data["props"]["pageProps"]["timeline"]["entries"]
#
#         # Function to parse tweet creation date
#         def parse_tweet_date(tweet):
#             date_str = tweet["content"]["tweet"]["created_at"]
#             return datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')
#
#         # Sort tweets by creation date in descending order
#         sorted_tweets = sorted(tweets, key=parse_tweet_date, reverse=True)
#
#         # Get current time
#         now = datetime.now(timezone.utc)
#
#         # Print the specified number of most recent tweets with their timestamps and tweet IDs
#         for tweet in sorted_tweets[:num_tweets]:
#             tweet_id = tweet["content"]["tweet"]["id_str"]
#             created_at = tweet["content"]["tweet"]["created_at"]
#             tweet_text = tweet["content"]["tweet"]["full_text"]
#             created_at_parsed = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
#             formatted_date = created_at_parsed.strftime('%b %d, %Y %H:%M:%S %z')
#
#             # Check if the tweet was made within the last 24 hours
#             is_recent = (now - created_at_parsed) <= timedelta(days=1)
#             recent_status = "Recent: True" if is_recent else "Recent: False"
#
#             print(f"ID: {tweet_id}\n{formatted_date}:\n{tweet_text}\n{recent_status}\n")
#     else:
#         print("Unexpected data structure. Please check the endpoint and the JSON parsing.")
#
# # Example usage
# print_recent_tweets("swmemes", 10)

import tweepy
from datetime import datetime, timezone, timedelta
import os
import json

# Your Twitter API credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def get_recent_tweets(username, num_tweets):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the user's profile page
    url = f"https://twitter.com/{username}"
    driver.get(url)

    # Let the page load
    driver.implicitly_wait(10)

    # Get the page source and parse with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find tweets
    tweets = soup.find_all('div', {'data-testid': 'tweet'}, limit=num_tweets)

    for tweet in tweets:
        tweet_id = tweet['data-tweet-id']
        tweet_text = tweet.find('div', {'class': 'css-901oao'}).get_text()
        print(f"ID: {tweet_id}\nText: {tweet_text}\n")

    # Close the WebDriver
    driver.quit()


# Example usage
get_recent_tweets("starwars", 5)
