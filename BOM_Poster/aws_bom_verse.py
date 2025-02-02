import random
import tweepy
import os
from datetime import datetime

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)


def bom_daily_verse(event, context):
    today = datetime.today()
    day_num = today.timetuple().tm_yday
    print(day_num)
    print(today)

    daily_verse = {
        1: "We believe in God, the Eternal Father, and in His Son, Jesus Christ, and in the Holy Ghost.",
        2: "We believe that men will be punished for their own sins, and not for Adam’s transgression.",
        3: "We believe that through the Atonement of Christ, all mankind may be saved, by obedience to the laws and ordinances of the Gospel.",
        4: "We believe that the first principles and ordinances of the Gospel are: first, Faith in the Lord Jesus Christ; second, Repentance; third, baptism by immersion for the remission of sins; fourth, Laying on of hands for the gift of the Holy Ghost.",
        5: "We believe that a man must be called of God, by prophecy, and by the laying on of hands by those who are in authority, to preach the Gospel and administer in the ordinances thereof.",
        6: "We believe in the same organization that existed in the Primitive Church, namely, apostles, prophets, pastors, teachers, evangelists, and so forth.",
        7: "We believe in the gift of tongues, prophecy, revelation, visions, healing, interpretation of tongues, and so forth.",
        8: "We believe the Bible to be the word of God as far as it is translated correctly; we also believe the Book of Mormon to be the word of God.",
        9: "We believe all that God has revealed, all that He does now reveal, and we believe that He will yet reveal many great and important things pertaining to the Kingdom of God.",
        10: "We believe in the literal gathering of Israel and in the restoration of the Ten Tribes; that Zion (the New Jerusalem) will be built upon the American continent; that Christ will reign personally upon the earth; and, that the earth will be renewed and receive its paradisiacal glory.",
        11: "We claim the privilege of worshiping Almighty God according to the dictates of our own conscience, and allow all men the same privilege, let them worship how, where, or what they may.",
        12: "We believe in being subject to kings, presidents, rulers, and magistrates, in obeying, honoring, and sustaining the law.",
        13: "We believe in being honest, true, chaste, benevolent, virtuous, and in doing good to all men; indeed, we may say that we follow the admonition of Paul—We believe all things, we hope all things, we have endured many things, and hope to be able to endure all things. If there is anything virtuous, lovely, or of good report or praiseworthy, we seek after these things.",
        14: "I will go and do the things which the Lord hath commanded, for I know the Lord prepares a way. -1 Nephi 3:7",
        15: "Feast upon the words of Christ; for behold, the words of Christ will tell you all things what ye should do. -2 Nephi 32:3",
        16: "After ye have received the Holy Ghost ye can speak with the tongue of angels. -2 Nephi 32:2",
        17: "He inviteth them all to come unto him and partake of his goodness. -2 Nephi 26:33",
        18: "In the strength of the Lord thou canst do all things which are expedient unto him. -Moroni 7:33",
        19: "Awake, my sons; put on the armor of righteousness. -2 Nephi 1:23",
        20: "If ye have faith ye can do all things which are expedient unto me. -Moroni 10:23",
        21: "If ye would hearken unto the Spirit which teacheth a man to pray, ye would know that ye must pray. -2 Nephi 32:8",
        22: "There is no other name given whereby salvation cometh; therefore, take upon you the name of Christ. -Mosiah 5:8",
        23: "They never did look upon death with any degree of terror, for their hope was in Christ and the resurrection. -Alma 27:28",
        24: "I know that I am nothing; therefore I will not boast of myself, but I will boast of my God. -Alma 26:12",
        25: "Remember, remember that there is no other way nor means whereby man can be saved, only through Christ. -Helaman 5:9",
        26: "For behold, I have refined thee, I have chosen thee in the furnace of affliction. -1 Nephi 20:10",
        27: "We labor diligently to write, to persuade our children and brethren to believe in Christ. -2 Nephi 25:23",
        28: "Whosoever shall put their trust in God shall be supported in their trials, troubles, and afflictions. -Alma 36:3",
        29: "Counsel with the Lord in all thy doings, and he will direct thee for good. -Alma 37:37",
        30: "I know that God loveth his children; nevertheless, I do not know the meaning of all things. -1 Nephi 11:17",
        31: "If this be the desire of your hearts, what have you against being baptized in the name of the Lord? -Mosiah 18:10"
        32: "Adam fell that men might be; and men are, that they might have joy. -2 Nephi 2:25",
        33: "Wherefore, ye must press forward with a steadfastness in Christ, having a perfect brightness of hope, and a love of God and of all men. -2 Nephi 31:20",
        34: "Yea, and are willing to mourn with those that mourn; yea, and comfort those that stand in need of comfort. -Mosiah 18:9",
        35: "And now, my sons, remember, remember that it is upon the rock of our Redeemer, who is Christ, the Son of God, that ye must build your foundation. -Helaman 5:12",
        36: "This life is the time for men to prepare to meet God. -Alma 34:32",
        37: "We talk of Christ, we rejoice in Christ, we preach of Christ. -2 Nephi 25:26",
        38: "The natural man is an enemy to God. -Mosiah 3:19",
        39: "Wickedness never was happiness. -Alma 41:10",
        40: "Press forward with a steadfastness in Christ. -2 Nephi 31:20",
        41: "Ye receive no witness until after the trial of your faith. -Ether 12:6",
        42: "This life is the time for men to prepare to meet God. -Alma 34:32",
        43: "By small and simple things are great things brought to pass. -Alma 37:6",
        44: "When ye are in the service of your fellow beings ye are only in the service of your God. -Mosiah 2:17",
        45: "And moreover, I would desire that ye should consider on the blessed and happy state of those that keep the commandments of God. For behold, they are blessed in all things, both temporal and spiritual. -Mosiah 2:41",
        46: "And now, my beloved brethren, I would that ye should come unto Christ, who is the Holy One of Israel, and partake of his salvation, and the power of his redemption. -2 Nephi 31:13",
        47: "Men are free according to the flesh; they can choose liberty and eternal life, or captivity and death. -2 Nephi 2:27",
        48: "My soul delighteth in the scriptures, and my heart pondereth them. -2 Nephi 4:15",
        49: "If ye believe all these things see that ye do them. -Mosiah 4:10",
        50: "Believe in God; believe that he is, and that he created all things, both in heaven and in earth. -Mosiah 4:9",
        51: "Have ye spiritually been born of God? -Alma 5:14",
        52: "If ye have felt to sing the song of redeeming love, I would ask, can ye feel so now? -Alma 5:26",
        53: "Faith is not to have a perfect knowledge of things; ye hope for things which are not seen. -Alma 32:21",
        54: "Learn wisdom in thy youth; learn in thy youth to keep the commandments of God. -Alma 37:35",
        55: "He shall go forth, suffering pains and afflictions of every kind. -Alma 7:11",
        56: "Pray in your families, always in my name, that your wives and your children may be blessed. -3 Nephi 18:21",
        57: "If men come unto me I will show unto them their weakness, that they may be humble. -Ether 12:27",
        58: "The Spirit of Christ is given to every man, that he may know good from evil. -Moroni 7:16",
        59: "When ye shall receive these things, I would exhort you to ask God if they are not true. -Moroni 10:4"
        60: "He suffereth the pains of all men, that they might repent and come unto him. -2 Nephi 9:21"
        61: "It must needs be, that there is an opposition in all things. -2 Nephi 2:11",
        62: "My God hath been my support; he hath led me through mine afflictions. -2 Nephi 4:20",
        63: "Before ye seek for riches, seek ye for the kingdom of God. -Jacob 2:18",
        64: "My soul hungered; I cried unto him in mighty prayer all the day long. -Enos 1:4",
        65: "If you do keep his commandments he doth bless you and prosper you. -Mosiah 2:22",
        66: "There is no other name given whereby salvation can come except in Christ. -Mosiah 3:17",
        67: "He will take upon him death, that he may loose the bands of death which bind his people. -Alma 7:12",
        68: "I know that which the Lord hath commanded me, and I glory in it. -Alma 29:9",
        69: "Nothing could be so bitter as my pains, nor so sweet as my joy. -Alma 36:21",
        70: "They did wax stronger in humility, firmer in faith, filling their souls with joy. -Helaman 3:35",
        71: "By the power of the Holy Ghost ye may know the truth of all things. -Moroni 10:5",
        72: "If ye will come unto me ye shall have eternal life; mine arm of mercy is extended. -3 Nephi 9:14",
        73: "I would that ye should be perfect even as I, or your Father who is in heaven is perfect. -3 Nephi 12:48",
        74: "There was no contention because of the love of God which did dwell in their hearts. -4 Nephi 1:15",
        75: "Repent, be baptized, and lay hold upon the gospel of Christ which shall be set before you. -Mormon 7:8",
        76: "God is the same yesterday, today, and forever; in him there is no change. -Mormon 9:9",
        77: "Whoso believeth in God might with surety hope for a better world. -Ether 12:4",
        78: "Pray unto the Father that ye may be filled with this love, which is bestowed upon true followers of Christ. -Moroni 7:48",
        79: "That which is of God inviteth and enticeth to do good continually. -Moroni 7:13",
        80: "The first fruits of repentance is baptism. -Moroni 8:25"
        81: "Whoso would hearken unto the word of God and hold fast unto it would never perish. -1 Nephi 15:24",
        82: "When they are learned they think they are wise, and they hearken not unto the counsel of God. -2 Nephi 9:28",
        83: "If ye shall believe in Christ ye will believe these words, for they are the words of Christ. -2 Nephi 33:10",
        84: "One being is as precious in his sight as the other. -Jacob 2:21",
        85: "Come unto him, and offer your whole souls as an offering unto him. -Omni 1:26",
        87: "If you will turn to the Lord with full purpose of heart, and put your trust in him, he will deliver you. -Mosiah 7:33",
        88: "I would that ye should be humble, be submissive and gentle, easy to be entreated. -Alma 7:23",
        89: "What shall I do that I may have this eternal life of which thou hast spoken? -Alma 22:15",
        90: "I ought to be content with the things which the Lord hath allotted unto me. -Alma 29:4",
        91: "Awake and arouse your faculties, even to an experiment upon my words. -Alma 32:27",
        92: "The way is prepared, and if we will look we may live forever. -Alma 37:44",
        93: "The Lord is merciful unto all who will, in the sincerity of their hearts, call upon his holy name. -Helaman 3:27",
        94: "If ye believe on his name ye will repent of all your sins, that ye may have remission of them. -Helaman 14:13",
        95: "Blessed are ye because of your faith. And now behold, my joy is full. -3 Nephi 17:20",
        96: "Know ye not that ye are in the hands of God? -Mormon 5:23",
        97: "God is good"
    }

    tweet_text = daily_verse[random.randint(1, len(daily_verse))] + " "
    print(tweet_text)

    client.create_tweet(text=tweet_text)
