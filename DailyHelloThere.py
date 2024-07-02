#Note, this file should be fully functional including updaing the count/countDailyHelloThere.txt and reading from that file
#incrementing, and then reading out to that file, i just need to make sure to run this .py code once a day (automate on computer)

import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your Twitter API credentials
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Check if environment variables are loaded correctly
if not all([API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
    raise ValueError("Some environment variables are missing. Please check your .env file.")

# Function to read the count from a file
def read_count(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    return 0

# Function to write the count to a file
def write_count(file_path, count):
    with open(file_path, 'w') as file:
        file.write(str(count))

try:
    # Authenticate to Twitter using Client for v2 API
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=API_KEY,
                           consumer_secret=API_SECRET_KEY,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET)

    # Path to your GIF file
    gif_path = 'images/helloThere.gif'
    count_file = 'count/countDailyHelloThere.txt'  # File to store the count

    # Debugging: Print the current working directory
    print("Current working directory:", os.getcwd())

    # Debugging: Print the absolute path to the GIF file
    absolute_gif_path = os.path.abspath(gif_path)
    print("Absolute path to GIF:", absolute_gif_path)

    # Check if the GIF file exists
    if not os.path.isfile(absolute_gif_path):
        raise FileNotFoundError(f"The file at path {absolute_gif_path} was not found.")

    # Authenticate to Twitter using OAuth1UserHandler for media upload (v1.1)
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Upload GIF using media_upload (v1.1)
    media = api.media_upload(absolute_gif_path)

    # Print the media ID and other information
    print(f"Media uploaded successfully! Media ID: {media.media_id}")
    print(f"Media details: {media}")

    # Read the current count from the file
    count = read_count(count_file)

    # Increment the count
    count += 1

    # Post tweet with the uploaded GIF using create_tweet (v2)
    tweet_text = f"Day {count} of me posting Obi-Wan Kenobi's \"Hello there\" from Star Wars Episode 3: Revenge of the Sith #StarWars #TheAcolyte #Kenobi #Obiwan #hellothere"
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
    print("Tweet posted successfully! Response:", response)

    # Write the updated count back to the file
    write_count(count_file, count)

except tweepy.TweepyException as e:
    print(f"An error occurred with Tweepy: {e}")
    if hasattr(e, 'api_codes') and 453 in e.api_codes:
        print("It seems your API credentials do not have the necessary permissions to upload media. Please check your access level on the Twitter Developer Portal.")

except Exception as e:
    print(f"An error occurred: {e}")
