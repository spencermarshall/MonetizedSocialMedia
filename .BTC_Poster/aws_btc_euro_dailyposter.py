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

        # Extract the percentage price changes in EUR
        price_change_1h_percent = data['market_data']['price_change_percentage_1h_in_currency']['eur']
        price_change_24h_percent = data['market_data']['price_change_percentage_24h_in_currency']['eur']
        price_change_30d_percent = data['market_data']['price_change_percentage_30d_in_currency']['eur']
        price_change_365d_percent = data['market_data']['price_change_percentage_1y_in_currency']['eur']

        # Calculate the historical price for each period
        def calculate_historical_price(change_percent):
            return current_price / (1 + (change_percent / 100))

        price_1h_ago = current_price / (1 + (price_change_1h_percent / 100))
        price_24h_ago = current_price / (1 + (price_change_24h_percent / 100))
        price_30d_ago = current_price / (1 + (price_change_30d_percent / 100))
        price_365d_ago = current_price / (1 + (price_change_365d_percent / 100))

        def format_change(start_price, change_percent):
            eur_change = current_price - start_price
            percent_change = (eur_change / start_price) * 100

            # Sign logic based on percentage change
            sign = "+" if percent_change > 0 else "-"
            return f"{sign}{abs(percent_change):.2f}% or {sign}€{abs(eur_change):,.2f}"

        # Append the results to the output string
        output += f"Current Bitcoin Price: €{current_price:,.2f}\n\n"


    else:
        output += f"Failed to retrieve data. Status code: {response.status_code}\n"

    output += "#Bitcoin #Crypto #BTC €BTC"  # todo you can add more hashtags here
    client.create_tweet(text=output)

