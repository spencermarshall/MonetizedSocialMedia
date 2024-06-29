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

print(data["props"]["pageProps"]["timeline"]["entries"][0]["content"]["tweet"]["full_text"])