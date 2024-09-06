import random
import requests
import tweepy

# Replace these with your own API keys and tokens
btc_clinet_id = 'eHZyQ2JTU3NDcEswNjZfSEsxNE46MTpjaQ'
btc_client_secret = 'ENsN3YTPm1GFr1l8CmyXcpGfZHKOnzzeNiJb5Bn5yLilODkTUJ'
btc_api_key = '2mFpPQSvY0HBHiIQ5RixTMBCS'
btc_api_key_secret = 'GNqD2Hf5orFoMlx84stT5sljIJNaCfGoBSSXrB3ECxugg4tK7e'
btc_access_token = '1831828094526922752-eJauqmb565LTckYzTXl6qajRsaPiTz'
btc_access_token_secret = 'UpcKRDkgJQfJ597UrEL6jEVKnYxxMw1xevjzP64BNwomg'
btc_bearer_token = 'AAAAAAAAAAAAAAAAAAAAABn2vgEAAAAAkOthl1LZODRSlqUmalBGQdyckJk%3DuDHvIq5yfTZbN5PInFw5cm6n3G9N4670sS91GkL3sZ5JbDoNxV'

client = tweepy.Client(bearer_token=btc_bearer_token,
                       consumer_key=btc_api_key, consumer_secret=btc_api_key_secret,
                       access_token=btc_access_token, access_token_secret=btc_access_token_secret)

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(btc_api_key, btc_api_key_secret, btc_access_token, btc_access_token_secret)
api = tweepy.API(auth)
tweet = ''

def get_btc_data():
    # CoinGecko API endpoint for getting current price and price change data
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"

    # Make a GET request to the CoinGecko API
    response = requests.get(url)

    # Initialize an empty string to accumulate the output
    output = ""

    if response.status_code == 200:
        data = response.json()

        # Extract the current price of BTC in USD
        current_price = data['market_data']['current_price']['usd']
        current_price += random.uniform(0, 0.99)

        # Extract the percentage price changes
        price_change_1h_percent = data['market_data']['price_change_percentage_1h_in_currency']['usd']
        price_change_24h_percent = data['market_data']['price_change_percentage_24h_in_currency']['usd']
        price_change_7d_percent = data['market_data']['price_change_percentage_7d_in_currency']['usd']
        price_change_30d_percent = data['market_data']['price_change_percentage_30d_in_currency']['usd']
        price_change_60d_percent = data['market_data']['price_change_percentage_60d_in_currency']['usd']
        price_change_200d_percent = data['market_data']['price_change_percentage_200d_in_currency']['usd']
        price_change_365d_percent = data['market_data']['price_change_percentage_1y_in_currency']['usd']

        # Calculate the historical price for each period
        def calculate_historical_price(change_percent):
            return current_price / (1 + (change_percent / 100))

        price_1h_ago = current_price / (1 + (price_change_1h_percent / 100))
        price_24h_ago = current_price / (1 + (price_change_24h_percent / 100))
        price_7d_ago = current_price / (1 + (price_change_7d_percent / 100))
        price_30d_ago = current_price / (1 + (price_change_30d_percent / 100))
        price_60d_ago = current_price / (1 + (price_change_60d_percent / 100))
        price_200d_ago = current_price / (1 + (price_change_200d_percent / 100))
        price_365d_ago = current_price / (1 + (price_change_365d_percent / 100))

        # Calculate the price change in USD for each time period
        def format_change(start_price, change_percent):
            usd_change = current_price - start_price
            percent_change = (usd_change / start_price) * 100

            # Sign logic based on percentage change
            sign = "+" if percent_change > 0 else "-"

            # Format USD and percentage change with sign
            return f"{sign}${abs(usd_change):,.2f} or {sign}{abs(percent_change):.2f}%"

        # Append the results to the output string
        output += f"Current Bitcoin Price: ${current_price:,.2f}\n\n"
        output += f"Price Change (1 Hour): {format_change(price_1h_ago, price_change_1h_percent)}\n"
        output += f"Price Change (24 Hours): {format_change(price_24h_ago, price_change_24h_percent)}\n"
        # output += f"Price Change (7 Days): {format_change(price_7d_ago, price_change_7d_percent)}\n"
        output += f"Price Change (30 Days): {format_change(price_30d_ago, price_change_30d_percent)}\n"
        # output += f"Price Change (60 Days): {format_change(price_60d_ago, price_change_60d_percent)}\n"
        # output += f"Price Change (200 Days): {format_change(price_200d_ago, price_change_200d_percent)}\n"
        output += f"Price Change (365 Days): {format_change(price_365d_ago, price_change_365d_percent)}\n"

    else:
        output += f"Failed to retrieve data. Status code: {response.status_code}\n"

    output += "#Bitcoin #Crypto #BTC $BTC"  # todo i can add more here
    # Print the accumulated output
    client.create_tweet(text=output)

# Run the function to get BTC data
get_btc_data()
# Post a tweet

print("Tweet posted successfully!")
