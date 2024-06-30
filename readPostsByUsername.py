import requests
import json

username = "starwars"
url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"

r = requests.get(url)

html = r.text

start_str = '<script id="__NEXT_DATA__" type="application/json">'
end_str = '</script></body></html>'

start_index = html.index(start_str) + len(start_str)
end_index = html.index(end_str, start_index)

json_str = html[start_index: end_index]
data = json.loads(json_str)

# Extracting the first tweet's ID and full text
tweet_id = data["props"]["pageProps"]["timeline"]["entries"][0]["content"]["tweet"]["id"]
tweet_full_text = data["props"]["pageProps"]["timeline"]["entries"][0]["content"]["tweet"]["full_text"]
print(f"id found manually:{data["props"]["pageProps"]["latest_tweet_id"]}")

print(f"Tweet ID: {tweet_id}")
print(f"Tweet Full Text: {tweet_full_text}")
