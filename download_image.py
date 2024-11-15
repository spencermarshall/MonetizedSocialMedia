import tweepy
import time
import requests
import boto3



API_KEY = 'yCGaHjd9563R6uH7WFIrLZd3d'
API_SECRET_KEY = 'z3g6gSjlMVDZk4c6aTbuvjkSi9hl984lUtOJ3kUdC9SXrmij1f'
client_id = 'eHZyQ2JTU3NDcEswNjZfSEsxNE46MTpjaQ'
client_secret = '908AB3em5NuRNKOjhfVEv6gSm5Zak0JRysqdKlRiNk6ORXGFsm'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAABn2vgEAAAAAG%2B%2FCtdrVmqeJTt%2BV6Dk2sK8nAW8%3DZlTeUtYsgRe0axwB0OVf1y0Yiskheqjx9vx8bTJxzYPl2KuoEs'
access_token = '1831828094526922752-CPna733OcTgkgsscCtg5igxT4pOmqF'
access_token_secret = 'fjGfebtR42ZNJVr6JpoQd5AzKTFssrXfqKCLUBhkbFvaT'

# API_KEY = 'og4HjXRYmKAzHHTYP0xFJ6D3q'
# API_SECRET_KEY = 'k3axIzwG18PAVUCmgg2Wwzatc29aiUdvrXy6UIlzMbcESucNj5'
# client_id = 'ZlBDcWxWaUdWeE9RbjFWYTJDams6MTpjaQ'
# client_secret = 'E0tGd957j87G_J42aAcazaZsZeoE0TkT0ad-U7FS4DVZ36lPw7'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHmDwgEAAAAAdta3NLjsPDs4piYh6cUKNw%2B1WU0%3D4jUmVHUEhaKI6RzDxhk26HNHINjq1YCk4zmavEPSpJMvTatlHx'
# access_token = '1849619632052961280-xUY3pvEPa9v0ye2ZMxtoKavSj6j2oh'
# access_token_secret = 'iaTq7GcUqkLU0aBJEX4N1Je59ppJ3xRydUlZCgRtsa87X'
#
# bearer_token = "AAAAAAAAAAAAAAAAAAAAAGscvwEAAAAAD%2BE%2FA1HFvb4hGDFzbZeMyA1hLuc%3D3yngqIcsmqDYyawEm2x3TVYfPEZaKYbnDRtEfFKEc9tPLmV8gk"
# API_KEY = "4ORKKv2122tpa1CKy6yGHZInO"
# API_SECRET_KEY = "35fQjzS0sxk5AverD0ur1YP9fZN8FdkJoS6xUW71Pc4zDGltDv"
# access_token = "1832642294165487616-Ro503mjfYALzFDKhSYqyRThUAiC2R9"
# access_token_secret = "2NsamH45xFXmM5BPUtb8K9pAIdI3hu3lvJqm561YMKSEz"
# #
# API_KEY = 'oBacdNpL8LB50kw8ZcPNIy5e7'
# API_SECRET_KEY = 'rwjBwFW2v6FbNIOG1ua3U7NtJm1SZqSv93e1uE0ucDSggeAWF8'
# access_token = '1798497258469564416-TgvOwczwFOyfwVVQitf0B7u0kXzEP7'
# access_token_secret = 'kZ1WLWeJHKeV3EbnJptyeASuMa91H15U9jUMgRqAMEm7Y'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAADGfuAEAAAAAiKXhRiJILcmDv54r2LVG8PpizMU%3DOveJUzcf8xrH2G1uL32SFFG1WAj0s1He8Wf75y4lYUX0jcOj1K'
# consumer_key = 'WU92SWwzN0xuemN0OTZvcFZOWHg6MTpjaQ'
# consumer_secret = 'eNAjt3FkHSJOJHd6VzDetZrTIhuKP52d_yKtl3RRIFQBv0HInn'

# API_KEY = 'F2qNzaY8nFfo2xL2jQovqPhFP'
# API_SECRET_KEY = 'kDNIb2yTBUyu1vuw8lpodMwQYdSUetdT1H5J68dUsLlA8vHOfT'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOT6vwEAAAAAvWmz9YdCrQgdmBuwQQMLIxuLeXw%3DQH4mvTQ0GvnWWsDetTrR7BDnRxWc6OLfP2ThqBJlwoMAAmNbzt'
# access_token = '1834727038022041601-wWnXmXkoJDQBrXBvrbXwNPZv9W2P87'
# access_token_secret = 'w5x7yOkgbnQGE5s5oMkmoxVYCCXfVR13z6hjc9j3PJrm0'
# #
# client_id = 'cnFHZ0h6LURnVmxqbXVmZW9qWTY6MTpjaQ'
# client_secret = 'gHpeCROnQ330bUhYj9Yry-dWQj01tlnogUUIHRTd8y6TM_rWVL'
# API_KEY = 'm5GPo8zjDkAuWMuZhjTM2ksJu'
# API_SECRET_KEY = 'iBt6OHUdCkq88fvwNVFsnuxL7CAU4avLzemUyU97aP18IWFZmS'
# access_token = '1837346181229563904-49LOpBdittQOb1hHkrEMRk5mzhVXFU'
# access_token_secret = 'HsPyF7XRBkfkhXI0sHUBZRKboPWTgtPRCy7fkHfy65bhU'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAANbewAEAAAAA2dsHWBhQRdWJwY6OhKfhja6fKOY%3DShBe6NotqhviLUXh3tjd2tZIa0rAkPvK654vNKcP93mV5OPIiq'

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token = bearer_token,
    consumer_key = API_KEY,
    consumer_secret = API_SECRET_KEY,
    access_token = access_token,
    access_token_secret = access_token_secret
)
s3 = boto3.client('s3')
BUCKET_NAME = 'lotr.photos'
#search recent tweets of user @elonmusk
tweets=None
try:
    tweets = client.search_recent_tweets(
        query="from:TheLOTRMemes has:media lang:en -is:retweet",
        max_results=3,
        tweet_fields=['created_at', 'public_metrics', 'lang', 'possibly_sensitive', 'text'],
        expansions='author_id,attachments.media_keys',  # Include media keys
        media_fields=['url', 'type', 'preview_image_url'],  # Request media fields
        user_fields=['username', 'public_metrics', 'verified']
    )
except tweepy.TooManyRequests as e:
    reset_time = int(e.response.headers.get("x-rate-limit-reset", 0))
    current_time = int(time.time())
    wait_time = reset_time - current_time

    if wait_time > 0:
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds until rate limit resets.")

print(tweets)
# Dictionary to map media keys to media objects
media_dict = {media.media_key: media for media in tweets.includes.get('media', [])}

for tweet in tweets.data:
    # Print tweet details
    author = next((user for user in tweets.includes['users'] if user.id == tweet.author_id), None)
    author_name = author.username if author else "Unknown"
    print(f"{tweet.text} by {author_name} at {tweet.created_at}")
    print(f"Tweet ID: {tweet.id}")

    # Print media details
    if 'attachments' in tweet and 'media_keys' in tweet.attachments:
        for media_key in tweet.attachments['media_keys']:
            media = media_dict.get(media_key)
            if media and media.url.endswith(('.jpg', '.png')):
                image_url = media.url
                print(f"Downloading {image_url}")

                # Download the image
                response = requests.get(image_url)
                if response.status_code == 200:
                    file_name = os.path.basename(image_url)

                    # Save the file to /tmp (AWS Lambda's writable directory)
                    file_path = f"/tmp/{file_name}"
                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                    # Upload to S3
                    s3.upload_file(file_path, BUCKET_NAME, file_name)
                    print(f"Uploaded {file_name} to S3 bucket {BUCKET_NAME}")

                else:
                    print(f"Failed to download {image_url}")
