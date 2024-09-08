import requests

# API endpoint to get a random advice
url = "https://api.adviceslip.com/advice"

# Send a GET request to fetch the random advice
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Convert the response to JSON format
    advice = data['slip']['advice']  # Extract the advice text

    # Print the advice
    print(f"Advice: {advice}")
else:
    print(f"Failed to fetch advice. Status code: {response.status_code}")
