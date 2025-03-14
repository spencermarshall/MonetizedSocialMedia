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
        5: "Which Marvel character would you want to be?",
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
        20: "What is your opinion on Ant-Man as a character?",
        21: "What is your opinion on the Guardians of the Galaxy movies?",
        22: "What is your opinion on the Thor movies?",
        23: "What is your opinion on the Captain America movies?",
        24: "What is your opinion on the Iron Man movies?",
        25: "What is your opinion on the Avengers: Infinity War?",
        26: "What is your opinion on the Avengers: Endgame?",
        27: "What is your opinion on the Tom Holland Spider Man movies?",
        28: "What is your opinion on Tobey Maguire as Spider Man?",
        29: "What is your opinion on Andrew Garfield as Spider Man?",
        30: "What is your opinion on the Hulk as a character?",
        31: "What is your opinion on the Black Widow movie?",
        32: "What is your opinion on the Black Panther movies?",
        33: "What is your opinion on the Doctor Strange movies?",
        34: "What is your opinion on the Captain Marvel movie?",
        35: "What is your opinion on the Shang-Chi movie?",
        36: "What is your opinion on the Eternals movie?",
        37: "What is your opinion on the upcoming Marvel movies?",
        38: "What is your opinion on the upcoming Marvel TV shows?",
        39: "What is your opinion on Thor as a character?",
        40: "What is your opinion on Loki as a character?",
        41: "What is your opinion on the Falcon as a character?",
        42: "What is your opinion on the Winter Soldier as a character?",
        43: "What is your opinion on the WandaVision TV show?",
        44: "What is your opinion on the Falcon and the Winter Soldier TV show?",
        45: "What is your opinion on the Loki TV show?",
        46: "What is your opinion on the Hawkeye TV show?",
        47: "What is your opinion on the What If TV show?",
        48: "What is your opinion on the She-Hulk TV show?",
        49: "What is your opinion on the Moon Knight TV show?",
        50: "What is your opinion on the Ms. Marvel TV show?",
        51: "What is your opinion on the Secret Invasion TV show?",
        52: "What is your opinion on Hawkeye as a character?",
        53: "What is your opinion on Black Widow as a character?",
        54: "What is your opinion on Black Panther as a character?",
        55: "What is your opinion on Doctor Strange as a character?",
        56: "What is your opinion on Captain Marvel as a character?",
        57: "What is your opinion on Shang-Chi as a character?",
        58: "What is your opinion on Captain America as a character?",
        59: "What is your opinion on Jane Foster as a character?",
        60: "What is your opinion on Groot as a character?",
        61: "What is your opinion on Rocket as a character?",
        62: "What is your opinion on Drax as a character?",
        63: "What is your opinion on Scarlet Witch as a character?",
        64: "What is your opinion on Vision as a character?",
        65: "What is your opinion on Hank Pym as a character?",
        66: "What is your opinion on Deadpool as a character?",
        67: "What is your opinion on Wolverine as a character?",
        68: "What is your opinion on Thanos as a character?",
        69: "What is your opinion on Ultron as a character?",
        70: "What is your opinion on Venom as a character?",
        71: "What is your opinion on the Venom movies?",
        72: "Why do you like Marvel?",
        73: "On a scale of 1-10, how much do you like Marvel?",
        74: "Captain America or Iron Man?",
        75: "Thor or Loki?",
        76: "Black Widow or Scarlet Witch?",
        77: "Thanos or Ultron?",
        78: "Wolverine or Deadpool?",
        79: "Black Panther or Doctor Strange?",
        80: "Hulk or She-Hulk?",
        81: "Marvel or DC?",
        82: "Marvel or Star Wars",
        83: "Marvel or Harry Potter",
        84: "Marvel or Lord of the Rings",
        85: "Marvel movies or comics?",
        86: "What are your opinions on Iron Man's character development?",
        87: "What are your opinions on Captain America's character development?",
        88: "What are your opinions on Thor's character development?",
        89: "What are your opinions on the death of Tony Stark?",
        90: "What are your opinions on the death of Steve Rogers?",
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
        102: "If Dr. Strange didn't give up the Time Stone, how would the events of Infinity War have changed?"
    }

    # s3 bucket files look up
    lookup = {
        1: "None",
        2: "None",
        3: "None",
        4: "None",
        5: "None",
        6: "None",
        7: "None",
        8: "None",
        9: "None",
        10: "None",
        11: "None",
        12: "None",
        13: "None",
        14: "None",
        15: "None",
        16: "None",
        17: "None",
        18: "None",
        19: "None",
        20: "None",
        21: "None",
        22: "None",
        23: "None",
        24: "None",
        25: "None",
        26: "None",
        27: "None",
        28: "None",
        29: "None",
        30: "None",
        31: "None",
        32: "None",
        33: "None",
        34: "None",
        35: "None",
        36: "None",
        37: "None",
        38: "None",
        39: "None",
        40: "None",
        41: "None",
        42: "None",
        43: "None",
        44: "None",
        45: "None",
        46: "None",
        47: "None",
        48: "None",
        49: "None",
        50: "None",
        51: "None",
        52: "None",
        53: "None",
        54: "None",
        55: "None",
        56: "None",
        57: "None",
        58: "None",
        59: "None",
        60: "None",
        61: "None",
        62: "None",
        63: "None",
        64: "None",
        65: "None",
        66: "None",
        67: "None",
        68: "None",
        69: "None",
        70: "None",
        71: "None",
        72: "None",
        73: "None",
        74: "None",
        75: "None",
        76: "None",
        77: "None",
        78: "None",
        79: "None",
        80: "None",
        81: "None",
        82: "None",
        83: "None",
        84: "None",
        85: "None",
        86: "None",
        87: "None",
        88: "None",
        89: "None",  # "questions/char_Yoda(puppet)/", #yoda puppet
        90: "None",
        91: "None",
        92: "None",
        93: "None",
        94: "None",
        95: "None",
        96: "None",
        97: "None",
        98: "None",
        99: "None",
        100: "None",
        101: "None",
        102: "None",
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
        115: "None",
        116: "None",
        117: "None",
        118: "None",
        119: "None",
        120: "None",
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
        134: "None",
        135: "None",
        136: "None",
        137: "None",
        138: "None",
        139: "None",
        140: "None",
        141: "None",
        142: "None",
        143: "None",
        144: "None",
        145: "None",
        146: "None",
        147: "None",
        148: "None",
        149: "None",
        150: "None",
        151: "None",
        152: "None",
        153: "None",
        154: "None",
        155: "None",
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
        167: "None",
        168: "None",
        169: "None",
        170: "None",
        171: "None",
        172: "None",
        173: "None",
        174: "None",
        175: "None",
        176: "None",
        177: "None",
        178: "None",
        179: "None",
        180: "None",
        181: "None",
        182: "None",
        183: "None",
        184: "None",
        185: "None",
        186: "None",
        187: "None",
        188: "None",
        189: "None",
        190: "None",
        191: "None",
        192: "None",
        193: "None",
        194: "None",
        195: "None",
        196: "None",
        197: "None",
        198: "None",
        199: "None",
        200: "None",
        201: "None",
        202: "None",
        203: "None",
        204: "None",
        205: "None",
        206: "None",
        207: "None",
        208: "None",
        209: "None",
        210: "None",
        211: "None",
        212: "None",
        213: "None",
        214: "None",
        215: "None",  # "questions/char_JudeLaw/",
        216: "None",  # "questions/char_Omega/",
        217: "None",  # "questions/char_Crosshair/",
        218: "None",  # "questions/char_Hunter/",
        219: "None",  # "questions/char_Tech/",
        220: "None",  # "questions/char_Wrecker/",
        221: "None",  # "questions/char_Echo/",
        222: "None",
        223: "None",
        224: "None",
        225: "None",
        226: "None",  # "questions/char_Leia(Kenobi-show)/",
        227: "None",  # "questions/char_Obi-Wan(Kenobi-Show)/",
        228: "None",  # "questions/char_Vader(Kenobi-show)/",
        229: "None",  # "questions/char_OwenBeruLars(Kenobi-show)/",
        230: "None",
        231: "None",  # "questions/char_SenatorOrgana(Kenobi-Show)/",
        232: "None",  # "questions/char_Kumail(Kenobi-Show)/",
        233: "None",  # "questions/char_DarthJarJar/"
        234: "None",
        235: "None",
        236: "None",
        237: "None",
        238: "None",
        239: "None",
        240: "None",
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
        if len(question_indices) > 90:
            question_indices.pop()  # Remove the last element

        updated_content = json.dumps(question_indices)

        s3.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)
        question = questions[index]

        contains_thoughts = "thoughts" in question.lower()
        contains_opinions = "opinions" in question.lower()

        # Only proceed if at least one of the words is present
        if contains_thoughts or contains_opinions:
            # Replace "thoughts" with randomly chosen word
            if contains_thoughts:
                replacement = "thoughts"
                if random.random() < 0.5:
                    replacement = "opinions"
                pattern = r'\bthoughts\b'
                question = re.sub(pattern, replacement, question)
                print("REPLACED")

            # Replace "opinions" with randomly chosen word
            if contains_opinions:
                replacement = "thoughts"
                if random.random() < 0.5:
                    replacement = "opinions"
                pattern = r'\bopinions\b'
                question = re.sub(pattern, replacement, question)

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

