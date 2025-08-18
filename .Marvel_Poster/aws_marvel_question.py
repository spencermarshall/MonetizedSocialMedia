import random
import boto3
import tweepy
import re
import os
import json

# X credentials stored in env variables
API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)


def Marvel_question(event, context):
    questions = {
        1: "Do you prefer MCU movies or comics?",
        2: "Which Marvel character would you want to be friends with?",
        3: "What is your favorite Marvel movie?",
        4: "Who is your favorite Marvel villain?",
        5: "Would you want to live in Wakanda?",
        6: "How old were you when you saw your first Marvel movie?",
        7: "Which Marvel character would you want to be your mentor?",
        8: "Which Marvel character would you want to be your sidekick?",
        9: "How did you get into Marvel?",
        10: "What is your favorite Marvel TV show?",
        11: "What is your favorite Marvel comic?",
        12: "What is your favorite Marvel quote?",
        13: "What is your favorite Marvel scene?",
        14: "What is your favorite Marvel soundtrack?",
        15: "What is your least favorite Marvel movie?",
        16: "Who is your least favorite Marvel character?",
        17: "Who is your least favorite Marvel villain?",
        18: "What is your least favorite Marvel scene?",
        19: "What are your opinions on the direction the MCU is currently headed?",
        20: "What are your opinions on Ant-Man",
        21: "What are your opinions on the Guardians of the Galaxy movies?",
        22: "What are your opinions on the Thor movies?",
        23: "What are your opinions on the Captain America movies?",
        24: "What are your opinions on the Iron Man movies?",
        25: "What are your opinions on the Avengers: Infinity War?",
        26: "What are your opinions on the Avengers: Endgame?",
        27: "What are your opinions on the Tom Holland Spider Man movies?",
        28: "What are your opinions on Tobey Maguire as Spider Man?",
        29: "Did you like Andrew Garfield as Spider Man?",
        30: "What are your opinions on the Hulk?",
        31: "What are your opinions on the Black Widow movie?",
        32: "What are your opinions on the original Black Panther movie?",
        33: "What are your opinions on the original Doctor Strange movie?",
        34: "What are your opinions on the Captain Marvel movie?",
        35: "What are your opinions on the Shang-Chi movie?",
        36: "What are your opinions on the Eternals movie?",
        37: "Are you excited for the upcoming Marvel movies?",
        38: "Are you excited for the upcoming Marvel TV shows?",
        39: "What are your opinions on Thor?",
        40: "What are your opinions on Loki?",
        41: "What are your opinions on the Falcon?",
        42: "What are your opinions on the Winter Soldier?",
        43: "What are your opinions on the WandaVision TV show?",
        44: "What are your opinions on the Falcon and the Winter Soldier TV show?",
        45: "What are your opinions on the Loki TV show?",
        46: "What are your opinions on the Hawkeye TV show?",
        47: "What are your opinions on the What If TV show?",
        48: "What are your opinions on the She-Hulk TV show?",
        49: "What are your opinions on the Moon Knight TV show?",
        50: "What are your opinions on the Ms. Marvel TV show?",
        51: "What are your opinions on the Secret Invasion TV show?",
        52: "What are your opinions on Hawkeye?",
        53: "What are your opinions on Black Widow?",
        54: "What are your opinions on Black Panther?",
        55: "What are your opinions on Doctor Strange?",
        56: "What are your opinions on Captain Marvel?",
        57: "What are your opinions on Shang-Chi?",
        58: "What are your opinions on Captain America?",
        59: "What are your opinions on Jane Foster?",
        60: "What are your opinions on Groot?",
        61: "What are your opinions on Rocket?",
        62: "What are your opinions on Drax?",
        63: "What are your opinions on Scarlet Witch?",
        64: "What are your opinions on Vision?",
        65: "What are your opinions on Hank Pym?",
        66: "What are your opinions on Deadpool?",
        67: "What are your opinions on Wolverine?",
        68: "What are your opinions on Thanos?",
        69: "What are your opinions on Ultron?",
        70: "What are your opinions on Venom?",
        71: "What are your opinions on the Venom movies?",
        72: "Why do you like Marvel?",
        73: "On a scale of 1-10, how much do you like Marvel?",
        74: "Captain America or Iron Man?",
        75: "Thor or Loki?",
        76: "Black Widow or Scarlet Witch?",
        77: "Thanos or Ultron?",
        78: "Wolverine or Deadpool?",
        79: "",
        80: "Hulk or She-Hulk?",
        81: "Marvel or DC?",
        82: "Marvel or Star Wars",
        # 83: "Marvel or Harry Potter",
        83: "Would you want to see Ultron return in any future projects?",
        84: "Marvel or Lord of the Rings",
        85: "Marvel: Movies or Comics?",
        86: "Did you like Iron Man's character development?",
        87: "Did you like Captain America's character development?",
        88: "Did you like Thor's character development?",
        89: "What are your opinions on the death of Tony Stark?",
        90: "What are your opinions on Gamora?",
        91: "What are your opinions on the death of Gamora?",
        92: "What are your opinions on the death of Black Widow?",
        93: "If you could bring back one Marvel character from the dead, who would it be?",
        94: "If you could kill off one Marvel character, who would it be?",
        95: "If you could change one thing about the MCU, what would it be?",
        96: "If you could add one thing to the MCU, what would it be?",
        97: "If you could be any Marvel character, who would you be?",
        98: "If you could have any Marvel character's powers, who would you choose?",
        99: "If you could have any Marvel character's weapon, which would you choose?",
        100: "If you could have any Marvel character's suit, which would you choose?",
        101: "If you could have any Marvel character's abilities, which would you choose?",
        102: "Which Marvel comic would you want a movie about?",
        103: "How do you feel about Marvel's use of post-credit scenes?",
        104: "How do you feel about Marvel's use of humor in their films?",
        105: "What Marvel prop or artifact would you display in your home?",
        106: "Who deserves their own spin-off show?",
        107: "What is your favorite Marvel Easter egg?",
        108: "What is your favorite Marvel crossover event?",
        109: "What is your favorite Marvel team-up?",
        110: "Which MCU Phase is your favorite?",
        111: "Which MCU Phase is your least favorite?",
        112: "Which upcoming MCU Project are you most excited about?",
        113: "Which Marvel character do you think has the best costume?",
        114: "Which Marvel character do you think has the worst costume?",
        115: "What are your opinions on Kevin Feige",
        116: "Which MCU character is most underrated?",
        117: "Which MCU character is most overrated?",
        118: "Would you want to see Thanos return in any future projects?",
        119: "Which Marvel actor's performance do you dislike most?",
        120: "Do you want to see a sequel to the Eternals movie?",
        121: "Which Marvel character's backstory do you find most compelling?",
        122: "What is your favorite fictional location in the MCU?",
        123: "Which planet in the MCU is your favorite?",
        124: "What is your favorite Marvel artifact?",
        125: "If you could recast one Marvel character who would it be?",
        126: "What are your top 3 Marvel movies?",
        127: "If you could have dinner with any Marvel character, who would it be?",
        128: "If you could create your own MCU movie, what would it be about?",
        129: "Who deserves their own movie or series?", #todo maybe delete or comment out idk
        130: "If you could introduce a new character to the MCU, who would it be and how would they fit in?",
        131: "What crossover event would you like to see in future Marvel projects?",
        132: "Which Marvel movie do you think is the most rewatchable?",
        133: "Do you like the idea of the multiverse?",
        134: "What are your thoughts on time travel in Avengers: Endgame?",
        135: "Did you like the relationship between Tony Stark and Peter Parker?",
        136: "Did you like the relationship between Steve Rogers and Bucky Barnes?",
        137: "Did you like the relationship between Thor and Loki?",
        138: "Did you like the relationship between Wanda and Vision?",
        139: "Black Widow or Hawkeye?",
        140: "What are your opinions on the Ant-Man movies?",
        141: "Which Marvel character do you think was best adapted from the comics to the movies?",
        142: "Which Marvel character do you think was worst adapted from the comics to the movies?",
        143: "If you could swap lives with a Marvel character for a day, who would it be?",
        # 144: "What do you think of the MCU’s approach to introducing new characters?",
        144: "Would you want to see Venom return in any future projects?",
        145: "What is your favorite Marvel fan theory?",
        146: "Do you play any Marvel video games?", #maybe more video game questions
        147: "Do you own any Marvel Lego sets?",
        148: "What is your favorite Marvel video game?",
        149: "Which Marvel animated project would you love to see adapted into live action?",
        150: "What is your favorite Marvel animated series?",
        151: "Do you want to see more animated projects in the MCU?",
        152: "What are your opinions on Stan Lee",
        153: "Which Stan Lee cameo is your favorite?",
        154: "Which surprise cameo in a Marvel project blew your mind the most?",
        155: "Which ‘What If…?’ episode would you develop into a full-length movie?",
        156: "How has your opinion of the MCU changed over time?",
        157: "Which Marvel villain do you think deserves a redemption arc, and how would you imagine it happen?",
        158: "If you could explore any untold story from the Marvel universe, what would it be?",
        159: "What’s the most emotional moment in a Marvel movie that still resonates with you?",
        160: "If you could rewrite the ending of any Marvel movie, which one would it be?",
        161: "Which Marvel story do you think deserves a prequel?",
        162: "What tech from the Marvel universe would you want in real life?",
        163: "If you could have a Marvel character as your personal trainer, who would it be?",
        164: "Which Marvel character do you think would make the best detective?",
        165: "What’s the most inspiring act of heroism you’ve seen from a Marvel character?",
        166: "Which Marvel character’s origin story would you most want to see reimagined, and how?",
        167: "Infinity War or Endgame?",
        168: "What are your opinions on Mjolnir?",
        169: "Thor's hammer or Captain America's shield?", #todo add images starting here and below - i stopped here last on 8.15.2025
        170: "Tesseract or Thor's hammer?",
        171: "Tesseract or Captain America's shield?",
        172: "Iron Man or Spider Man?",
        173: "Did you like the Thunderbolts* (The New Avengers) movie?",
        174: "Wakanda or Asgard?",
        175: "Would you want to live in Asgard?",
        176: "What are your opinions on Wakanda?",
        177: "Would you want another Thor movie?",
        178: "Do you enjoy Tom Holland as Spider Man?",
        179: "Would you want to see another Hulk movie?",
        180: "What are your opinions on Black Panther: Wakanda Forever",
        181: "What are your opinions on the movie 'Doctor Strange in the Multiverse of Madness'",
        182: "Do you want to see another Schang-Chi movie?",
        183: "Do you want to see another season of WandaVision?",
        184: "Do you want to see another season of The Falcon and the Winter Soldier?",
        185: "Do you want to see another season of Loki?",
        186: "Would you want to see another season of Hawkeye?", #todo look into working for asking for another season
        187: "Would you want to see another season of 'What If'?", #todo like questions 183-187
        188: "Would you want to see another season of She-Hulk?",
        189: "Do you want to see another season of Moon Knight?",
        190: "Would you want to see another season of Ms. Marvel?", #todo maybe delete
        191: "If you could change one thing about Ms. Marvel show what would it be?",
        192: "If you could change one thing about Moon Knight what would it be?",
        193: "If you could change one thing about She-Hulk what would it be?",
        194: "If you could change one thing about What-If show what would it be?",
        195: "If you could change one thing about the Hawkeye show what would it be?",
        196: "If you could change one thing about the Loki show what would it be?",
        197: "If you could change one thing about the WandaVision show what would it be?", #todo this is a test if this style of questions work, if so add more for all shows and movies
        198: "Would you want to see another season of Secret Invasion?",
        199: "If you could change one thing about the Secret Invasion show what would it be?",
        200: "What future projects do you want to see Hawkeye in?",
        201: "If you could change one thing about Black Widow's character what would you change?",
        202: "What future projects do you want to see Dr. Strange in?",
        203: "What future projects do you want to see Captain Marvel in?",
        204: "What future projects do you want to see Shang-Chi in?",
        205: "What future projects do you want to see Scarlet Witch in?",
        206: "What future projects would you want to see Vision in?",
        207: "What future projects would you want to see Deadpool in?",
        208: "What future projects would you want to see Wolverine in?",
        209: "Did you like how Steve Rogers stayed behind in Endgame?",
        210: "Do you want to see old Steve Rogers return in future projects?",
        211: "Do you want another Venom movie?",
        212: "What are your opinions on Iron Man?",
        213: "What are your opinions on Robert Downey Jr. returning as Doctor Doom?",
        214: "What are your opinions on the Fantastic Four joining the MCU?",
        215: "What are your opinions on the Fantastic Four movie?",
        216: "If you could change one thing about Iron Man, what would it be?",
        217: "If you could change one thing about Captain America, what would it be?",
        218: "If you could change one thing about Thor, what would it be?",
        219: "If you could change one thing about Hulk, what would it be?",
        220: "What are your opinions on Bucky Barnes?",
        221: "What are your opinions on Falcon becoming Captain America?",
        222: "Do you want another Ant-Man movie?",
        223: "Did you like Endgame more than Infinity War?",
        224: "Do you want to see another Fantastic Four movie?",
        225: "When should they stop making new Spider Man movies?",
        226: "On a scale from 1-10, how would you rate Infinity War?",
        227: "On a scale from 1-10, how would you rate Endgame?",
        228: "On a scale from 1-10, how would you rate the original Black Panther movie?",
        229: "On a scale from 1-10, how would you rate the original Doctor Strange movie?",
        230: "On a scale from 1-10, how would you rate the Captain Marvel movie?",
        231: "On a scale from 1-10, how would you rate the Shang-Chi movie?",
        232: "On a scale from 1-10, how would you rate the Eternals movie?",
        233: "On a scale from 1-10, how would you rate the Black Widow movie?",
        234: "On a scale from 1-10, how would you rate the Thor movies?",
        235: "On a scale from 1-10, how would you rate the Iron Man movies?",
        236: "On a scale from 1-10, how would you rate the Captain America movies?",
        237: "On a scale from 1-10, how would you rate the original Avengers movie?",
        238: "On a scale from 1-10, how would you rate the Guardians of the Galaxy movies?",
        239: "Do you think Scarlet Witch deserves her own movie?",
        240: "On a scale from 1-10, how would you rate Black Panther: Wakanda Forever?",

     } #add question about funny mexican guy from antman movies


    # s3 bucket files look up
    lookup = {
        1: "questions/other_MoviesORComics/",
        2: "None",
        3: "None",
        4: "None",
        5: "questions/place_Wakanda/",
        6: "None",
        7: "None",
        8: "None",
        9: "None",
        10: "None",
        11: "questions/other_Comics/",
        12: "None",
        13: "None",
        14: "None",
        15: "None",
        16: "None",
        17: "None",
        18: "None",
        19: "None",
        20: "questions/char_Antman/",
        21: "questions/movie_GuardiansOfGalaxy/",
        22: "questions/movie_ThorAll/",
        23: "questions/movie_CaptainAmericaAll/",
        24: "questions/movie_IronManAll/",
        25: "questions/movie_InfinityWar/",
        26: "questions/movie_Endgame/",
        27: "questions/char_TomHollandSpiderMan/",
        28: "questions/char_TobyMaguireSpiderMan/",
        29: "questions/char_AndrewGarfieldSpiderMan/",
        30: "questions/char_Hulk/",
        31: "questions/movie_BlackWidow/",
        32: "questions/movie_BlankPatherOG/",
        33: "questions/movie_DrStrangeOG/",
        34: "questions/movie_CaptainMarvel/",
        35: "questions/movie_SchangChi/",
        36: "questions/movie_Eternals/",
        37: "None",
        38: "None",
        39: "questions/char_Thor/",
        40: "questions/char_Loki/",
        41: "questions/char_Falcon/",
        42: "questions/char_WinterSoldier/",
        43: "questions/show_WandaVision/",
        44: "questions/show_FalconWinterSoldier/",
        45: "questions/show_Loki/",
        46: "questions/show_Hawkeye/",
        47: "questions/show_WhatIf/",
        48: "questions/show_SheHulk/",
        49: "questions/show_MoonKnight/",
        50: "questions/show_MsMarvel/",
        51: "questions/show_SecretInvasion/",
        52: "questions/char_Hawkeye/",
        53: "questions/char_BlackWidow/",
        54: "questions/char_BlackPanther/",
        55: "questions/char_DrStrange/",
        56: "questions/char_CaptainMarvel/",
        57: "questions/char_ShangChi/",
        58: "questions/char_CaptainAmerica/",
        59: "questions/char_JaneFoster/",
        60: "questions/char_Groot/",
        61: "questions/char_Rocket/",
        62: "questions/char_Drax/",
        63: "questions/char_ScarletWitch/",
        64: "questions/char_Vision/",
        65: "questions/char_HankPym/",
        66: "questions/char_Deadpool/",
        67: "questions/char_Wolverine/",
        68: "questions/char_Thanos/",
        69: "questions/char_Ultron/",
        70: "questions/char_Venom/",
        71: "questions/movies_VenomMovies/",
        72: "None",
        73: "None",
        74: "questions/char_CaptianAmericaORIronMan/",
        75: "questions/char_ThorORLoki/",
        76: "questions/char_BlackWidowORScarletWitch/",
        77: "questions/char_ThanosORUltron/",
        78: "questions/char_WolverineORDeadpool/",
        79: "None",
        80: "questions/char_HulkORSheHulk/",
        81: "questions/other_MarvelORDC/",
        82: "questions/other_MarvelORStarWars/",
        83: "questions/char_Ultron/",
        84: "questions/other_MarvelORLOTR/",
        85: "questions/other_MoviesORComics/",
        86: "questions/char_IronMan/",
        87: "questions/char_CaptainAmerica/",
        88: "questions/char_Thor/",
        89: "questions/other_TonyStarkDeath/",
        90: "questions/char_Gamora/",
        91: "questions/other_GamoraDeath/",
        92: "questions/other_BlackWidowDeath/",
        93: "None",
        94: "None",
        95: "None",
        96: "None",
        97: "None",
        98: "None",
        99: "None",
        100: "None",
        101: "None",
        102: "questions/other_Comics/",
        103: "None",
        104: "None",
        105: "None",
        106: "None",
        107: "None",
        108: "None",
        109: "None",
        110: "None",
        111: "None",
        112: "None",
        113: "None",
        114: "None",
        115: "questions/char_KevinFeige/",
        116: "None",
        117: "None",
        118: "questions/char_Thanos/",
        119: "None",
        120: "questions/movie_Eternals/",
        121: "None",
        122: "None",
        123: "None",
        124: "None",
        125: "None",
        126: "None",
        127: "None",
        128: "None",
        129: "None",
        130: "None",
        131: "None",
        132: "None",
        133: "None",
        134: "questions/movie_Endgame/",
        135: "questions/char_TonyStarkANDPeterParker/",
        136: "questions/char_SteveRogersANDBucky/",
        137: "questions/char_ThorORLoki/",
        138: "questions/char_WandaANDVision/",
        139: "questions/char_BlackWidowORHawkeye/",
        140: "questions/movie_AntMans/",
        141: "questions/other_Comics/",
        142: "questions/other_Comics/",
        143: "None",
        144: "questions/char_Venom/",
        145: "None",
        146: "None",
        147: "questions/other_Lego/",
        148: "None",
        149: "None",
        150: "None",
        151: "None",
        152: "questions/char_StanLee/",
        153: "questions/char_StanLee/",
        154: "None",
        155: "questions/show_WhatIf/",
        156: "None",
        157: "None",
        158: "None",
        159: "None",
        160: "None",
        161: "None",
        162: "None",
        163: "None",
        164: "None",
        165: "None",
        166: "None",
        167: "questions/movie_InfinityWarOREndgame/",
        168: "questions/other_Mjolnir/",
        169: "questions/other_HammerORShield/",
        170: "None",
        171: "None",
        172: "questions/char_IronManORSpiderMan/",
        173: "questions/movie_Thunderbolts",
        174: "questions/other_WakandaORAsgard/",
        175: "questions/place_Asgard/",
        176: "questions/place_Wakanda/",
        177: "questions/movie_ThorAll/",
        178: "questions/char_TomHollandSpiderMan/",
        179: "questions/char_Hulk/",
        180: "questions/movie_BlackPantherWakandaForever/",
        181: "questions/movie_DrStrangeMultiverse/",
        182: "questions/movie_SchangChi/",
        183: "questions/show_WandaVision/",
        184: "questions/show_FalconWinterSoldier/",
        185: "questions/show_Loki/",
        186: "questions/show_Hawkeye/",
        187: "questions/show_WhatIf/",
        188: "questions/show_SheHulk/",
        189: "questions/show_MoonKnight/",
        190: "questions/show_MsMarvel/",
        191: "questions/show_MsMarvel/",
        192: "questions/show_MoonKnight/",
        193: "questions/show_SheHulk/",
        194: "questions/show_WhatIf/",
        195: "questions/show_Hawkeye/",
        196: "questions/show_Loki/",
        197: "questions/show_WandaVision/",
        198: "questions/show_SecretInvasion/",
        199: "questions/show_SecretInvasion/",
        200: "questions/char_Hawkeye/",
        201: "questions/char_BlackWidow/",
        202: "questions/char_DrStrange/",
        203: "questions/char_CaptainMarvel/",
        204: "questions/char_ShangChi/",
        205: "questions/char_ScarletWitch/",
        206: "questions/char_Vision/",
        207: "questions/char_Deadpool/",
        208: "questions/char_Wolverine/",
        209: "questions/char_OldSteveRogers/",
        210: "questions/char_OldSteveRogers/",
        211: "questions/movies_VenomMovies/",
        212: "questions/char_IronMan/",
        213: "questions/char_RDJdrDoom/",
        214: "questions/char_FantasticFour/",
        215: "questions/char_FantasticFour/",
        216: "questions/char_IronMan/",
        217: "questions/char_CaptainAmerica/",
        218: "questions/char_Thor/",
        219: "questions/char_Hulk/",
        220: "questions/char_BuckyBarnes/",
        221: "questions/other_FalconBecomingCA/",
        222: "questions/movie_AntMans/",
        223: "questions/movie_InfinityWarOREndgame/",
        224: "questions/char_FantasticFour/",
        225: "None",
        226: "questions/movie_InfinityWar/",
        227: "questions/movie_Endgame/",
        228: "questions/movie_BlankPatherOG/",
        229: "questions/movie_DrStrangeOG/",
        230: "questions/movie_CaptainMarvel/",
        231: "questions/movie_SchangChi/",
        232: "questions/movie_Eternals/",
        233: "questions/movie_BlackWidow/",
        234: "questions/movie_ThorAll/",
        235: "questions/movie_IronManAll/",
        236: "questions/movie_CaptainAmericaAll/",
        237: "questions/movie_AvengersOG/",
        238: "questions/movie_GuardiansOfGalaxy/",
        239: "questions/char_ScarletWitch/",
        240: "questions/movie_BlackPantherWakandaForever/",
        241: "None",
        242: "None",
        243: "None",
        244: "None",
        245: "None",
        246: "None",
        247: "None",
        248: "None",
        249: "None",
        250: "None",
        251: "None",
        252: "None",
        253: "None",
        254: "None"
    }

    bucket_name = 'marvel.photos'
    file_key = 'notes/marvel_questions.txt'
    s3 = boto3.client('s3')

    try:
        # Fetch the current file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')

        # Convert the file content (string) into a Python list
        question_indices = json.loads(file_content)
        print(question_indices)

        index = random.randint(1, len(questions))

        # try again until we get new item not in list
        while index in question_indices:
            index = random.randint(1, len(questions))
        path = lookup[index]

        question_indices.insert(0, index)
        if len(question_indices) > 120:
            question_indices.pop()  # Remove the last element

        updated_content = json.dumps(question_indices)

        s3.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)
        question = questions[index]

        print("BEFORE")
        print(question)
        # this replaces 'thoughts' or 'opinions' with 50% chance of either
        contains_thoughts = "thoughts" in question.lower()
        contains_opinions = "opinions" in question.lower()


        # Only proceed if at least one of the words is present
        if contains_thoughts or contains_opinions:
            # Replace "thoughts" with randomly chosen word
            ran = random.random()
            if contains_thoughts:
                replacement = "thoughts"
                if random.random() < 0.5:
                    replacement = "opinions"
                if random.random() < 0.2:
                    replacement = "honest " + replacement

                pattern = r'\bthoughts\b'
                question = re.sub(pattern, replacement, question)
                print("REPLACED")

            # Replace "opinions" with randomly chosen word
            if contains_opinions:
                replacement = "thoughts"
                if random.random() < 0.5:
                    replacement = "opinions"
                if random.random() < 0.2:
                    replacement = "honest " + replacement
                pattern = r'\bopinions\b'
                question = re.sub(pattern, replacement, question)
                print("REPLACED")
        # done replacing
        print("AFTER")
        print(question)

        if path == "None":  # upload just text, no image
            client.create_tweet(text=question)
            return f"POSTED TWEET {question} with no image"

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=path)
        if 'Contents' not in response:
            return {
                'statusCode': 404,
                'body': 'No files found in the specified directory.'
            }
        # Extract file keys (paths) from the response
        file_keys = [obj['Key'] for obj in response['Contents'] if obj['Key'] != path]
        # Check if there are files to choose from
        if not file_keys:
            return {
                'statusCode': 404,
                'body': 'No files found in the specified directory.'
            }

        # Pick a random file from the list
        random_file = random.choice(file_keys)

        # these 4 are for image, not implemented yet:
        download_path = f"/tmp/{os.path.basename(random_file)}"
        s3.download_file(bucket_name, random_file, download_path)
        media = api.media_upload(download_path)
        client.create_tweet(text=question, media_ids=[media.media_id])
        return f"tweeted image with question {question}"
    except Exception as e:
        print(e)

