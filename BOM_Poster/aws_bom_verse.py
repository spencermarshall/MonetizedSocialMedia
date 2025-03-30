import random
import tweepy
import os
from datetime import datetime

# Twitter API authentication setup
API_KEY = 'iUKkGWeeWWgb7VQHWj44mROSV'
API_SECRET_KEY = 'TjVMwO0NrDjT8aIFQttg4xy5NlzHIs4Askx2Eu5mAVEMv5l4x7'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAN9VxwEAAAAALxyzkCe3PuUNDZxlMJ8E3MUYnLU%3DbJDU9CWl88fyQi6C5K0GWd7cOxekRCEBpGYh7yOYQBfY3PyF7R'
ACCESS_TOKEN = '1831488681640857600-7OjuKVNuY5IsFLZJ1lNE4QW1tHWDGv'
ACCESS_TOKEN_SECRET = 'KpEzU8IarTH4HrifXzpuzHRHGsMgtGXI81x6IdhSAbslZ'
client_id = 'd3JHWnRNbUY2V2p0VjdaZXgzQ0g6MTpjaQ'
client_secret = 'gmTsDtmh1Xcvfmxe8FeIVlTLcQ-x9CAF9FD8qrx2bKWvbmRrG8'

client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)


def bom_daily_verse(event, context):
    today = datetime.today()
    day_num = today.timetuple().tm_yday
    print(day_num)
    print(today)

    daily_verse = {
        1: "But he answered and said, It is written, Man shall not live by bread alone, but by every word that proceedeth out of the mouth of God. -Matthew 4:4",
        2: "But I say unto you, Love your enemies, bless them that curse you, do good to them that hate you, and pray for them which despitefully use you, and persecute you -Matthew 5:44",
        3: "Be ye therefore perfect, even as your Father which is in heaven is perfect. -Matthew 5:48",
        4: "Therefore whosoever heareth these sayings of mine, and doeth them, I will liken him unto a wise man, which built his house upon a rock. -Matthew 7:24",
        5: "Blessed are the peacemakers: for they shall be called the children of God. -Matthew 5:9",
        6: "And Jesus, when he was baptized, went up straightway out of the water: and, lo, the heavens were opened unto him, and he saw the Spirit of God descending like a dove, and lighting upon him. -Matthew 3:16",
        7: "And every one that heareth these sayings of mine, and doeth them not, shall be likened unto a foolish man, which built his house upon the sand. -Matthew 7:26",
        8: "Blessed are the pure in heart: for they shall see God. -Matthew 5:8",
        9: "For what is a man profited, if he shall gain the whole world, and lose his own soul? or what shall a man give in exchange for his soul? -Matthew 16:26",
        10: "Whosoever looketh on a woman to lust after her hath committed adultery with her already in his heart. -Matthew 5:28",
        11: "Blessed are the meek: for they shall inherit the earth. -Matthew 5:5",
        12: "And said, Verily I say unto you, Except ye be converted, and become as little children, ye shall not enter into the kingdom of heaven. -Matthew 18:3",
        13: "Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost -Matthew 28:19",
        14: "Come unto me, all ye that labour and are heavy laden, and I will give you rest. -Matthew 11:28",
        15: "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you. -Matthew 6:33",
        16: "Jesus said unto him, Thou shalt love the Lord thy God with all thy heart, and with all thy soul, and with all thy mind. -Matthew 22:37",
        17: "Not every one that saith unto me, Lord, Lord, shall enter into the kingdom of heaven; but he that doeth the will of my Father which is in heaven. -Matthew 7:21",
        18: "Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you. -Matthew 7:7",
        19: "Lay not up for yourselves treasures upon earth, where moth and rust doth corrupt, and where thieves break through and steal. -Matthew 6:19",
        20: "For every one that asketh receiveth; and he that seeketh findeth; and to him that knocketh it shall be opened. -Matthew 7:8",
        21: "Beware of false prophets, which come to you in sheep's clothing, but inwardly they are ravening wolves. -Matthew 7:15",
        22: "Therefore I say unto you, Take no thought for your life, what ye shall eat, or what ye shall drink; nor yet for your body, what ye shall put on. Is not the life more than meat, and the body than raiment? -Matthew 6:25",
        23: "And she shall bring forth a son, and thou shalt call his name JESUS: for he shall save his people from their sins. -Matthew 1:21",
        24: "No man can serve two masters: for either he will hate the one, and love the other; or else he will hold to the one, and despise the other. Ye cannot serve God and mammon. -Matthew 6:24",
        25: "Take heed that ye do not your alms before men, to be seen of them: otherwise ye have no reward of your Father which is in heaven. -Matthew 6:1",
        26: "For where two or three are gathered together in my name, there am I in the midst of them. -Matthew 18:20",
    }

    tweet_text = daily_verse[random.randint(1, len(daily_verse))] + " "
    print(tweet_text)

    client.create_tweet(text=tweet_text)
