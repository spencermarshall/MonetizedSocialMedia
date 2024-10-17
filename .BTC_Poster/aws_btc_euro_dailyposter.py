import random
import requests
import tweepy

#these are placeholders, so the real keys aren't in a public repo, the real keys are in aws and in .env
btc_api_key = 'placeholder'
btc_api_key_secret = 'placeholder'
btc_access_token = 'placeholder'
btc_access_token_secret = 'placeholder'
btc_bearer_token = 'placeholder'

client = tweepy.Client(bearer_token=btc_bearer_token,
                       consumer_key=btc_api_key, consumer_secret=btc_api_key_secret,
                       access_token=btc_access_token, access_token_secret=btc_access_token_secret)

auth = tweepy.OAuth1UserHandler(btc_api_key, btc_api_key_secret, btc_access_token, btc_access_token_secret)
api = tweepy.API(auth)

def get_btc_data(event, context):
    # CoinGecko API endpoint for getting current price and price change data in EUR
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    output = ""

    if response.status_code == 200:
        data = response.json()

        # Extract the current price of BTC in EUR
        current_price = data['market_data']['current_price']['eur']
        current_price += random.uniform(0, 0.99)

        output += f"Bitcoin: €{current_price:,.2f}\n\n"


    else:
        output += f"Bitcoin"
    client.create_tweet(text=output)

