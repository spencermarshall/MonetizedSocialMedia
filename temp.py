import requests

# Base URL for the API
BASE_URL = "https://officeapi.akashrajpurohit.com/quote"

# Set to store unique quotes
unique_quotes = set()

# Loop through pages 1 to 298 (inclusive)
for page in range(1, 298):
    response = requests.get(f"{BASE_URL}/{page}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract and format the quote and character
        quote = data.get("quote")
        character = data.get("character")
        if quote and character:
            text = f"\"{quote}\" -{character}"
            unique_quotes.add(text)
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")

# Print all unique quotes
print(f"Total unique quotes retrieved: {len(unique_quotes)}")
for quote in unique_quotes:
    print(quote)
