import requests


def get_random_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}

    # Send a GET request to the API
    response = requests.get(url, headers=headers)

    # Parse the response JSON
    if response.status_code == 200:
        joke_data = response.json()
        print("Here's a dad joke for you:")
        print(joke_data['joke'])
    else:
        print("Couldn't fetch a joke. Status code:", response.status_code)


# Call the function to fetch and print a random joke
get_random_dad_joke()
