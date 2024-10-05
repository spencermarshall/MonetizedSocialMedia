import requests


def get_random_harry_potter_quote():
    url = 'https://api.portkey.uk/quote'
    response = requests.get(url)

    if response.status_code != 200:
        return

    quote_data = response.json()
    quote = quote_data['quote']
    speaker = quote_data['speaker']
    print(f'"{quote}" -{speaker}')


# Example usage
get_random_harry_potter_quote()
