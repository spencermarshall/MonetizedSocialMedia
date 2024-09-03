# from datetime import datetime
# import pytz
#
# class FinalPost:
#
#     def __init__(self):
#         # Utah time zone, MST or MDT
#         self.timezone = pytz.timezone('America/Denver')
#
#     def post(self):
#         time = datetime.now(self.timezone)
#         minutes_since_midnight = time.hour * 60 + time.minute
#         if (minutes_since_midnight < 360):
#             break # between 12am - 6am, do not post

import requests


def get_gif_links(api_url):
    # Send a GET request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        files = response.json()
        # Extract and return the download URLs of GIF files
        return [file['download_url'] for file in files if file['name'].endswith('.gif')]
    else:
        print(f"Failed to fetch directory contents: {response.status_code}")
        return []


# GitHub API URLs for the directories
nowords_gif_url = 'https://api.github.com/repos/spencermarshall/StarWarsTwitterPost/contents/images/no-words'
quote_gif_url = 'https://api.github.com/repos/spencermarshall/StarWarsTwitterPost/contents/images/quote-or-meme'

# list of GIF links
nowords_gif_links = get_gif_links(nowords_gif_url)
quote_gif_links = get_gif_links(quote_gif_url)

# Print out the GIF links
print("No-Words GIF Links:")
for link in nowords_gif_links:
    print(link)

print("\nQuote GIF Links:")
for link in quote_gif_links:
    print(link)
