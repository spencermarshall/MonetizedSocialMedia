import requests
import random

# URL of the JSON file containing quotes
url = "https://raw.githubusercontent.com/chuckmeyer/us-president-quotes/main/us_president_quotes.json"

# Fetching the JSON data from the GitHub URL
response = requests.get(url)

# If the request was successful, process the JSON data
if response.status_code == 200:
    quotes = response.json()  # Parsing the JSON content
    # Pick a random quote from the list
    random_quote = random.choice(quotes)
    # Print the random quote and the author (president)
    print(f'"{random_quote["quote"]}" -{random_quote["president"]}')
else:
    print("Failed to retrieve the quotes. Please check the URL.")

