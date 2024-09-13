import requests

url = "https://api.quotable.io/quotes"

params = {
    'query': 'Marvel',
    'limit': 1
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for quote in data['results']:
        print(f"{quote['author']}: \"{quote['content']}\"")
else:
    print(f"Error: {response.status_code}")
