import requests


def get_motivational_quote():
    url = "https://zenquotes.io/api/random"

    # Send a GET request to the API
    response = requests.get(url)

    # Parse the response JSON
    if response.status_code != 200:
        return
    quote_data = response.json()
    print(f"'{quote_data[0]['q']}' -{quote_data[0]['a']}")



# Call the function to fetch and print a random motivational quote
get_motivational_quote()
