import requests

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

        # Extract the percentage price changes
        price_change_1h_percent = data['market_data']['price_change_percentage_1h_in_currency']['usd']
        price_change_24h_percent = data['market_data']['price_change_percentage_24h_in_currency']['usd']
        price_change_7d_percent = data['market_data']['price_change_percentage_7d_in_currency']['usd']
        price_change_30d_percent = data['market_data']['price_change_percentage_30d_in_currency']['usd']
        price_change_365d_percent = data['market_data']['price_change_percentage_1y_in_currency']['usd']

        # Approximate percentage change for 180 days (using linear interpolation between 30 days and 1 year)
        price_change_180d_percent = ((price_change_365d_percent - price_change_30d_percent) / 335) * 180 + price_change_30d_percent

        # Calculate the historical price for each period
        def calculate_historical_price(change_percent):
            return current_price / (1 + (change_percent / 100))

        price_1h_ago = current_price / (1 + (price_change_1h_percent / 100))
        price_24h_ago = current_price / (1 + (price_change_24h_percent / 100))
        price_7d_ago = current_price / (1 + (price_change_7d_percent / 100))
        price_30d_ago = current_price / (1 + (price_change_30d_percent / 100))
        price_180d_ago = calculate_historical_price(price_change_180d_percent)
        price_365d_ago = calculate_historical_price(price_change_365d_percent)

        # Calculate the price change in USD for each time period
        def format_change(start_price, change_percent):
            usd_change = current_price - start_price
            percent_change = (usd_change / start_price) * 100
            sign = "+" if usd_change > 0 else "-"
            return f"{sign}${abs(usd_change):.2f} or {percent_change:.2f}%"

        # Append the results to the output string
        output += f"Current Bitcoin (BTC) Price: ${current_price:.2f}\n"
        output += f"Price Change (1 Hour): {format_change(price_1h_ago, price_change_1h_percent)}\n"
        output += f"Price Change (24 Hours): {format_change(price_24h_ago, price_change_24h_percent)}\n"
        output += f"Price Change (7 Days): {format_change(price_7d_ago, price_change_7d_percent)}\n"
        output += f"Price Change (30 Days): {format_change(price_30d_ago, price_change_30d_percent)}\n"
        output += f"Price Change (180 Days): {format_change(price_180d_ago, price_change_180d_percent)}\n"
        output += f"Price Change (365 Days): {format_change(price_365d_ago, price_change_365d_percent)}\n"

    else:
        output += f"Failed to retrieve data. Status code: {response.status_code}\n"

    output += "#Bitcoin #Crypto" #todo i can add more here
    # Print the accumulated output
    print(output)

# Run the function to get BTC data
get_btc_data()
