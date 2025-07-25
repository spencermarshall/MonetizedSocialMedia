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
        1: "Which Hogwarts House are you?",
        2: "Do you like the house sorting ceremony?",
        3: "What spell if your favorite?",
        4: "Which book in the series is your favorite?",
        5: "What are your thoughts on the Gryffindor vs. Slytherin rivalry?",
        6: "Who was the best Defense Against the Dark Arts teacher?",
        7: "What’s your opinion on Snape’s true loyalties?",
        8: "What’s your favorite Quidditch moment?",
        9: "Who is your favorite Weasley sibling?",
        10: "What are your thoughts on the Marauder’s Map?",
        11: "Would you rather have a Firebolt or a Nimbus 2000?",
        12: "Which Dark artifact intrigues you most?",
        13: "What do you think of the house elves?",
        14: "Which magical creature is your favorite?",
        15: "Harry Potter or Lord of the Rings?",
        16: "Dobby or Kreacher?",
        17: "Which Horcrux was the most interesting?",
        18: "HP Movies or Books?",
        19: "Which HP character’s arc did you enjoy the most?",
        20: "Did you like the Floo Network as transportation?",
        21: "What’s your opinion on the Patronus Charm?",
        22: "Would you use Floo Network to transport?",
        23: "What are your opinions on the Triwizard Tournament?",
        24: "Ravenclaw or Hufflepuff?",
        25: "How old were you when you first discovered Harry Potter", #What do you think of the Deathly Hallows legend?
        26: "Who's your favorite Order of the Phoenix member?",
        27: "What are your opinions on Platform 9¾?",
        28: "How do you feel about the Ministry of Magic’s role?",
        29: "What was your reaction to Dumbledore’s death?",
        30: "Which Horcrux hunt location did you like the most?",
        31: "What do you think of the Room of Requirement?",
        32: "Harry Potter or Star Wars?",
        33: "Who is the most compelling HP villain?",
        34: "What Patronus are you?",
        35: "Would you want to visit the Forbidden Forest?",
        36: "Which subject at Hogwarts would you study first?",
        37: "Do you think the Unforgivable Curses should be taught at Hogwarts?",
        38: "Did you like the Weasley twins’ pranks?",
        39: "Did you like Ron and Hermione’s relationship?",
        40: "What are your opinions on Harry’s character development?",
        41: "Who's a better mentor: Dumbledore or McGonagall?",
        42: "What are your thoughts on the role of Muggles?",
        43: "Would you join Dumbledore’s Army?",
        44: "Which wizarding battle would you fight in?",
        45: "What are your thoughts on the Triwizard Maze?",
        46: "Why do you think Hagrid has a strong loyalty to Harry?",
        47: "Which magical plants fascinate you most?",
        48: "What would you use as a Horcrux?",
        49: "Would you enter the Chamber of Secrets?",
        50: "What’s your favorite Gryffindor moment?",
        # 51: "What do you think of the Slytherin ambition theme?",
        51: "What change in the movies did you dislike the most?",
        52: "What is your favorite scene in Diagon Alley?",
        53: "Do you like the Deathly Hallows symbol?",
        54: "What are your opinions on The Cursed Child?",
        55: "Which Hogwarts ghost do you like ths most?",
        56: "Would you ride on the Knight Bus?",
        57: "Which duel is your favorite?",
        58: "What are your thoughts on the Muggle-Wizard divide?",
        59: "Who is the bravest character?",
        60: "Which Weasley product would you buy?",
        61: "What are your thoughts on the Invisibility Cloak?",
        62: "Did you enjoy the Yule Ball dance?",
        63: "Would you rather have the Elder Wand or Resurrection Stone?",
        64: "What are your opinions on Hogwarts as a school?",
        65: "Which Hogwarts portrait would you talk to?",
        66: "Which magical transportation method do you like the most?",
        67: "Would you work at Gringotts?",
        68: "What are your opinions of Death Eaters",
        69: "What are your opinions of Kreacher",
        70: "Which Weasley family tradition do you like the most?",
        71: "What’s your favorite scene at Hogwarts Express train?",
        72: "Would you rather brew Polyjuice or Amortentia?",
        73: "Did you like Rita Skeeter’s journalism?",
        74: "Which creature in the Department of Mysteries stands out?",
        75: "What are your opinions of Voldemort’s origins?",
        76: "Which Fred and George prank is your favorite?",
        77: "Which character’s backstory would you expand?",
        78: "What are your thoughts on the final Battle of Hogwarts?",
        # 79: "Which magical item would you steal from Umbridge?",
        79: "What change in the movies did you like the most?",
        80: "Do you want to run through the brick wall at Platform 9¾?",
        # 81: "Which potion-making class memory do you remember?",
        81: "Who is your least favorite HP character?",
        82: "Would you ever join the Death Eaters?",
        83: "Do you like Harry’s lightning scar?",
        84: "Which Dumbledore memory would you live through?",
        85: "What’s your opinion on the Weasley’s Wizard Wheezes shop?",
        86: "Which epilogue reveal surprised you the most?",
        87: "Did you like Neville’s hero journey?",
        88: "Do you like the role of the Sorting Hat?",
        89: "What’s your favorite scene in the Room of Requirement?",
        90: "What are your opinions on The Sorcerer’s Stone?",
        91: "What are your opinions on Dobby's Death?",
        92: "What are your opinions on Hedwig's Death?",
        93: "What are your opinions on Snape's Death?",
        94: "What are your opinions on Sirius Black's Death?",
        95: "What are your opinions on the Marauder's Map?",
        96: "Which character’s redemption arc is your favorite?",
        97: "Which HP book is your favorite?",
        98: "Which HP movie is your favorite?",
        99: "Did you like the relationship between Harry and Ginny?",
        100: "If you could rewrite one event in the HP series what would it be?",
        101: "Who is your favorite HP character?",
        102: "Did you like The Sorcerer's Stone as a book?",
        103: "Who's death hit you the hardest?",
        104: "What’s your favorite scene in the Forbidden Forest?",
        105: "Did you like Voldemort as a villain?",
        106: "Did you like The Chamber of Secrets as a book?",
        107: "Did you like The Prisoner of Azkaban as a book?",
        108: "Did you like The Goblet of Fire as a book?",
        109: "Did you like The Order of the Phoenix as a book?",
        110: "Did you like The Half-Blood Prince as a book?",
        111: "Did you like The Deathly Hallows as a book?",
        112: "What are your opinions on Harry Potter as a character?",
        113: "What are your opinions on Hermione Granger?",
        114: "What are your opinions on Ron Weasley?",
        115: "What are your opinions on Draco Malfoy?",
        116: "What are your opinions on Dumbledore?",
        117: "What are your opinions on Severus Snape?",
        118: "What are your opinions on Hagrid?",
        119: "What are your opinions on Minerva McGonagall?",
        120: "What are your opinions on Luna Lovegood?",
        121: "What are your opinions on Neville Longbottom?",
        122: "What are your opinions on Ginny Weasley?",
        123: "What are your opinions on Bellatrix Lestrange?",
        124: "What is your favorite moment from the Harry Potter series?",
        125: "What are your opinions on Mad Eye Moody?",
        126: "What are your opinions on Sirius Black?",
        127: "What are your opinions on Remus Lupin?",
        128: "What are your opinions on Molly Weasley?",
        129: "What are your opinions on Arthur Weasley?",
        130: "What are your opinions on Dolores Umbridge?",
        131: "What are your opinions on Lucius Malfoy?",
        132: "Did you like the differences between the Harry Potter books and movies?",
        133: "What are your opinions on Peter Pettigrew?",
        134: "If you could attend one class at Hogwarts which would it be?",
        135: "What are your opinions on Flitwick?",
        136: "How do you feel about the epilogue in 'Deathly Hallows'?",
        137: "What are your opinions on Gilderoy Lockhart?",
        138: "What is your favorite quote from the HP series?",
        139: "Which Hogwarts teacher is your favorite?",
        140: "What are your thoughts on the Weasley family?",
        141: "If you could create a new spell what would it do?",
        142: "Do you like Quidditch as a sport?",
        143: "Did you like the time-travel elements in 'Prisoner of Azkaban'?",
        144: "What are your opinions on the new Snape", #todo add image
        145: "What is your favorite potion in the HP universe?",
        146: "What is your favorite battle scene in the HP series?",
        147: "If you could have any magical creature as a pet which would you choose?",
        148: "Which minor character in HP deserves more attention?",
        149: "Do you like the Hogwarts houses system?",
        150: "What is your favorite magical item from the series?",
        151: "What is your favorite Harry Potter fan theory?",
        152: "What is your favorite Harry Potter meme?",
        153: "McGonagall or Snape?",
        154: "What is your favorite Harry Potter fan fiction story?",
        155: "What are your thoughts on Severus Snape’s love for Lily?",
        156: "What are your thoughts on Cho Chang?",
        157: "Which HP character had the most wasted potential?",
        158: "What are your opinions on the Wizarding World’s education system at Hogwarts?",
        159: "What is your favorite HP soundtrack or musical theme?",
        160: "Which HP character is the most misunderstood?",
        161: "If you could write a new HP story, what would it be about?",
        162: "How do you feel about friendship in the HP series?",
        163: "What did you think of the Battle of Hogwarts?",
        164: "Did you like the rivalry between Harry and Draco?",
        165: "Did you like J.K. Rowling’s writing style?",
        166: "What is your favorite HP location?",
        167: "What are your thoughts on J.K. Rowling?",
        168: "What are your thoughts on the moving stairs at Hogwarts?",
        169: "Gryffindor, Slytherin, Ravenclaw, or Hufflepuff: which house would you choose?",
        170: "Gryffindor or Slytherin?",
        171: "Did you like The Sorcerer's Stone as a movie?",
        172: "Did you like The Chamber of Secrets as a movie?",
        173: "Did you like The Prisoner of Azkaban as a movie?",
        174: "Did you like The Goblet of Fire as a movie?",
        175: "Did you like The Order of the Phoenix as a movie?",
        176: "Did you like The Half-Blood Prince as a movie?",
        177: "Did you like The Deathly Hallows as a movie?",
}
    # s3 bucket files look up
    lookup = {
        1: "None",
        2: "None",
        3: "None",
        4: "None",
        5: "questions/other_GryffindorORSlytherin/",
        6: "None",
        7: "questions/char_Snape/",
        8: "questions/other_Quidditch/",
        9: "questions/char_WeasleyFamily/",
        10: "questions/other_MarauderMap/",
        11: "questions/other_FireboltORNimbus2000/",
        12: "None",
        13: "questions/other_HouseElves/",
        14: "None",
        15: "questions/other_hpORlotr/",
        16: "questions/char_DobbyORKreacher/",
        17: "None",
        18: "questions/other_HPbooksORmovies/",
        19: "None",
        20: "questions/other_Floo/",
        21: "questions/other_PatronusCharm/",
        22: "questions/other_Floo/",
        23: "questions/other_TriwizardTournament/",
        24: "None",
        25: "None",
        26: "None",
        27: "questions/other_Platform934/",
        28: "None",
        29: "questions/char_DumbledoreDeath/",
        30: "None",
        31: "questions/other_RoomOfRequirement/",
        32: "None",
        33: "None",
        34: "questions/other_PatronusCharm/",
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
        70: "questions/char_WeasleyFamily/",
        71: "None",
        72: "None",
        73: "None",
        74: "None",
        75: "None",
        76: "None",
        77: "None",
        78: "None",
        79: "None",
        80: "questions/other_Platform934/",
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
        117: "questions/char_Snape/",
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
        132: "questions/other_HPbooksORmovies/",
        133: "None",
        134: "None",
        135: "None",
        136: "None",
        137: "None",
        138: "None",
        139: "None",
        140: "questions/char_WeasleyFamily/",
        141: "None",
        142: "questions/other_Quidditch/",
        143: "None",
        144: "questions/other_HPbooksORmovies/",
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
        170: "questions/other_GryffindorORSlytherin/",
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
        if len(question_indices) > 120:
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

