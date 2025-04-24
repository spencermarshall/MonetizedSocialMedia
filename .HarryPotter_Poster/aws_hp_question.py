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


def HarryPotter_question(event, context):
    questions = {
        1: "Which Hogwarts House do you identify with most, and why?",
        2: "What are your thoughts on the house sorting ceremony?",
        3: "What’s your favorite spell from HP?",
        4: "Which book in the series is your favorite?",
        5: "What are your thoughts on the Gryffindor vs. Slytherin rivalry?",
        6: "Which Defense Against the Dark Arts teacher was the best?",
        7: "What’s your opinion on Snape’s true loyalties?",
        8: "What’s your favorite Quidditch moment?",
        9: "Who is the most underrated Weasley sibling?",
        10: "What are your thoughts on the Marauder’s Map?",
        11: "Would you rather have a Firebolt or a Nimbus 2000?",
        12: "Which Dark artifact intrigues you most?",
        13: "What do you think of the portrayal of house elves?",
        14: "What’s your favorite magical creature?",
        15: "What did you think of the Triwizard Tournament?",
        16: "Dobby or Kreacher?",
        17: "Which Horcrux was the most interesting plot device?",
        18: "What are your opinions on the HP Movies vs Books?",
        19: "Which HP character’s arc moved you the most?",
        20: "What do you think of the Floo Network as transportation?",
        21: "What’s your opinion on the Patronus Charm?",
        22: "How did you feel about Sirius’s fate?",
        23: "What are your opinions on the Triwizard Tournament?",
        24: "Would you drink a Felix Felicis potion?",
        25: "What do you think of the Deathly Hallows legend?",
        26: "Which member of the Order of the Phoenix inspires you?",
        27: "What are your thoughts on the portrayal of Umbridge?",
        28: "How do you feel about the Ministry of Magic’s role?",
        29: "What was your reaction to Dumbledore’s death?",
        30: "Which Horcrux hunt location was most atmospheric?",
        31: "What do you think of the Room of Requirement?",
        32: "Would you attend Ilvermorny or Beauxbatons instead?",
        33: "Who is the most compelling HP villain, and why?",
        34: "Which Patronus form resonates with you?",
        35: "What are your thoughts on the Forbidden Forest?",
        36: "Which magical subject at Hogwarts would you study first?",
        37: "How do you feel about the Unforgivable Curses being taught?",
        38: "What’s your opinion on the Weasley twins’ pranks?",
        39: "What are your opinions on Ron and Hermione’s relationship?",
        40: "What are your opinions on Harry’s character development?",
        41: "Who would you choose as a mentor: Dumbledore or McGonagall?",
        42: "What are your thoughts on the role of Muggle-borns?",
        43: "Would you join Dumbledore’s Army?",
        44: "Which wizarding battle would you fight in?",
        45: "What’s your take on the Triwizard Maze?",
        46: "What do you think of Hagrid’s loyalty to Harry?",
        47: "Which magical plants fascinate you most?",
        48: "What are your thoughts on the Horcrux-Hallows connection?",
        49: "Would you dare enter the Chamber of Secrets?",
        50: "What’s your favorite Gryffindor moment?",
        51: "What do you think of the Slytherin ambition theme?",
        52: "Which scene in Diagon Alley is most memorable?",
        53: "What’s your opinion on the Deathly Hallows symbol?",
        54: "What are your opinions on The Cursed Child?",
        55: "Which Hogwarts ghost intrigues you most?",
        56: "What did you think of the Knight Bus introduction?",
        57: "Which magical duel is your favorite?",
        58: "What are your thoughts on the Muggle-Wizard divide?",
        59: "Who is the bravest character in your view?",
        60: "Which Weasley product would you buy?",
        61: "How do you feel about the Invisibility Cloak’s power?",
        62: "What’s your take on the Yule Ball dance scenes?",
        63: "Would you rather own the Elder Wand or Resurrection Stone?",
        64: "What are your opinions on Hogwarts?",
        65: "Which Hogwarts portrait would you visit?",
        66: "What are your thoughts on magical transportation methods?",
        67: "Would you work at Gringotts?",
        68: "What are your opinions of Death Eaters",
        69: "What are your opinons of Kreacher",
        70: "Which Weasley family tradition do you admire?",
        71: "What’s your favorite scene at Hogwarts Express?",
        72: "Would you rather brew Polyjuice or Amortentia?",
        73: "What do you think of Rita Skeeter’s journalism?",
        74: "Which creature in the Department of Mysteries stands out?",
        75: "How do you feel about Voldemort’s origins?",
        76: "What’s your most beloved Fred and George prank?",
        77: "Which character’s backstory would you expand?",
        78: "What are your thoughts on the final Battle of Hogwarts?",
        79: "Which magical item would you steal from Umbridge?",
        80: "What do you think of the Silver Doe patronus event?",
        81: "Which potion-making class memory do you remember?",
        82: "Would you ever join the Death Eaters?",
        83: "What do you think of Harry’s scar?",
        84: "Which Dumbledore memory would you live through?",
        85: "What’s your opinion on the Weasley’s Wizard Wheezes shop?",
        86: "Which epilogue reveal surprised you?",
        87: "What do you think of Neville’s hero journey?",
        88: "What do you think of the role of the Sorting Hat?",
        89: "What’s your favorite scene in the Room of Requirement?",
        90: "What are your opinions on The Sorcerer’s Stone?",
        91: "What are your opinions on Dobby's Death?",
        92: "What are your opinions on Hedwig's Death?",
        93: "What are your opinions on Snape's Death?",
        94: "What are your opinions on Sirius Black's Death?",
        95: "What are your opinions on the Marauder's Map?",
        96: "Which character’s redemption arc is most powerful?",
        97: "What is your favorite Harry Potter book and why?",
        98: "What is your favorite Harry Potter movie and why?",
        99: "What are your opinions on the relationship between Harry and Ginny?",
        100: "If you could rewrite one event in the HP series, what would it be?",
        101: "Who is your favorite Harry Potter character and why?",
        102: "What do you think of the role of the Ministry of Magic?",
        103: "Which character’s death hit you the hardest?",
        104: "What’s your favorite scene in the Forbidden Forest?",
        105: "What are your thoughts on Voldemort as a villain?",
        106: "What are your opinions on The Chamber of Secrets?",
        107: "What are your opinions on The Prisoner of Azkaban?",
        108: "What are your opinions on The Goblet of Fire?",
        109: "What are your opinions on The Order of the Phoenix?",
        110: "What are your opinions on The Half-Blood Prince?",
        111: "What are your opinions on The Deathly Hallows?",
        112: "What are your opinions on Harry Potter as a character?",
        113: "What are your opinions on Hermione Granger as a character?",
        114: "What are your opinions on Ron Weasley as a character?",
        115: "What are your opinions on Draco Malfoy as a character?",
        116: "What are your opinions on Dumbledore as a character?",
        117: "What are your opinions on Severus Snape as a character?",
        118: "What are your opinions on Hagrid as a character?",
        119: "What are your opinions on Minerva McGonagall as a character?",
        120: "What are your opinions on Luna Lovegood as a character?",
        121: "What are your opinions on Neville Longbottom as a character?",
        122: "What are your opinions on Ginny Weasley as a character?",
        123: "What are your opinions on Bellatrix Lestrange as a character?",
        124: "What is your favorite moment from the Harry Potter series?",
        125: "What are your opinions on Mad Eye Moody as a character?",
        126: "What are your opinions on Sirius Black as a character?",
        127: "What are your opinions on Remus Lupin as a character?",
        128: "What are your opinions on Molly Weasley as a character?",
        129: "What are your opinions on Arthur Weasley as a character?",
        130: "What are your opinions on Dolores Umbridge as a character?",
        131: "What are your opinions on Lucius Malfoy as a character?",
        132: "What are your thoughts on the differences between the Harry Potter books and movies?",
        133: "What are your opinions on Peter Pettigrew as a character?",
        134: "If you could attend one class at Hogwarts, which would it be and why?",
        135: "What are your opinions on Flitwick as a character?",
        136: "How do you feel about the epilogue in 'Deathly Hallows'?",
        137: "What are your opinions on Gilderoy Lockhart as a character?",
        138: "What is your favorite quote from the Harry Potter series?",
        139: "Which Hogwarts teacher is your favorite and why?",
        140: "What are your thoughts on the Weasley family?",
        141: "If you could create a new spell, what would it do?",
        142: "What is your favorite Quidditch moment in the series?",
        143: "How do you feel about the time-travel elements in 'Prisoner of Azkaban'?",
        144: "What is your favorite scene in the Harry Potter movies that wasn’t in the books?",
        145: "What is your favorite potion in the Harry Potter universe and why?",
        146: "What is your favorite battle scene in the Harry Potter series?",
        147: "If you could have any magical creature as a pet, which would you choose?",
        148: "Which minor character in Harry Potter deserves more attention and why?",
        149: "What are your opinions on the Hogwarts houses system?",
        150: "What is your favorite magical item from the series?",
        151: "What is your favorite Harry Potter fan theory?",
        152: "What is your favorite Harry Potter meme?",
        153: "",
        154: "What is your favorite Harry Potter fan fiction?",
        155: "What are your thoughts on the portrayal of Severus Snape’s love for Lily?",
        156: "What are your thoughts on Cho Chang as a character?",
        157: "Which Harry Potter character do you think had the most wasted potential?",
        158: "What are your opinions on the Wizarding World’s education system at Hogwarts?",
        159: "What is your favorite Harry Potter soundtrack or musical theme?",
        160: "Which Harry Potter character do you think is the most misunderstood?",
        161: "If you could write a new Harry Potter story, what would it be about?",
        162: "How do you feel about the portrayal of friendship in the Harry Potter series?",
        163: "What did you think of the Battle of Hogwarts?",
        164: "What are your thoughts on the relationship between Harry and Draco?",
        165: "What are your opinions on J.K. Rowling’s writing style?",
        166: "What is your favorite Harry Potter location?",
        167: "What are your thoughts on J.K. Rowling?",
        168: "What are your thoughts on the moving stairs at Hogwarts?",
        169: "Griffindor, Slytherin, Ravenclaw, or Hufflepuff: which house would you choose?",
        170: "Griffindor or Slytherin?",
        171: "Ravenclaw or Hufflepuff?",
        172: "Harry Potter or Star Wars?",
        173: "Harry Potter or Lord of the Rings?",
        174: "What are your opinions on Platform 9¾?",
        175: "McGonagall or Snape?",

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

    bucket_name = 'harrypotter.photos'
    file_key = 'notes/harrypotter_questions.txt'
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

