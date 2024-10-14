import random
import tweepy

#insert api keys

client = tweepy.Client(bearer_token = bearer_token,
                                consumer_key = API_KEY, consumer_secret = API_SECRET_KEY,
                                access_token = access_token, access_token_secret = access_token_secret)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, access_token,access_token_secret)
api = tweepy.API(auth)

video_path = '../videos/2 Ahsoka Short (trailer) 30s - Copy.mp4'
media = api.media_upload(video_path)

client.create_tweet(text="Ahsoka", media_ids=[media.media_id])
