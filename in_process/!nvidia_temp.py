import requests
from datetime import datetime, timedelta

#todo THIS ISN'T WORKING
def get_stock_data(symbol, api_key):
    # Alpha Vantage API endpoint for daily time series
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'full'
    }

    # Make a GET request to the Alpha Vantage API
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    data = response.json()
    if 'Time Series (Daily)' not in data:
        print("Error: Time Series (Daily) data not found.")
        return None

    # Extract daily time series
    time_series = data['Time Series (Daily)']

    # Get the latest available date
    dates = list(time_series.keys())
    latest_date = max(dates)
    current_price = float(time_series[latest_date]['4. close'])

    # Helper function to calculate percentage change
    def calculate_change(start_price, end_price):
        change = end_price - start_price
        percent_change = (change / start_price) * 100
        sign = "+" if change > 0 else "-"
        return f"{sign}${abs(change):.2f} or {percent_change:.2f}%"

    # Get prices for different periods
    def get_price_n_days_ago(n):
        past_date = (datetime.strptime(latest_date, '%Y-%m-%d') - timedelta(days=n)).strftime('%Y-%m-%d')
        return float(time_series.get(past_date, {'4. close': current_price})['4. close'])

    # Calculate price changes
    price_change_24h = calculate_change(get_price_n_days_ago(1), current_price)
    price_change_7d = calculate_change(get_price_n_days_ago(7), current_price)
    price_change_30d = calculate_change(get_price_n_days_ago(30), current_price)
    price_change_180d = calculate_change(get_price_n_days_ago(180), current_price)
    price_change_365d = calculate_change(get_price_n_days_ago(365), current_price)

    # For 5 years and 15 years, use approximate number of trading days (252 trading days per year)
    trading_days_per_year = 252
    price_change_5y = calculate_change(get_price_n_days_ago(5 * trading_days_per_year), current_price)
    price_change_15y = calculate_change(get_price_n_days_ago(15 * trading_days_per_year), current_price)

    # Print the results
    output = ""
    output += f"Current {symbol} Price: ${current_price:.2f}\n"
    output += f"Price Change (24 Hours): {price_change_24h}\n"
    output += f"Price Change (7 Days): {price_change_7d}\n"
    output += f"Price Change (30 Days): {price_change_30d}\n"
    output += f"Price Change (180 Days): {price_change_180d}\n"
    output += f"Price Change (365 Days): {price_change_365d}\n"
    output += f"Price Change (5 Years): {price_change_5y}\n"
    output += f"Price Change (15 Years): {price_change_15y}\n"

    print(output)


# Replace 'YOUR_API_KEY' with your Alpha Vantage API key
get_stock_data('NVDA', 'YOUR_API_KEY')
