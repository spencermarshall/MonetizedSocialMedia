import random
import boto3
import tweepy
import os
import json
import re

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


def lotr_question(event, context):
    questions = {
        1: "What are your opinions on Frodo Baggins?",
        2: "What are your opinions on Samwise Gamgee?",
        3: "What are your opinions on Gandalf?",
        4: "What are your opinions on Aragorn?",
        5: "What are your opinions on Legolas?",
        6: "What are your opinions on Gimli?",
        7: "What are your opinions on Gollum?",
        8: "What are your opinions on Saruman?",
        9: "What are your opinions on Sauron?",
        10: "What are your opinions on Galadriel?",
        11: "What are your opinions on Elrond?",
        12: "What are your opinions on Arwen?",
        13: "What are your opinions on Éowyn?",
        14: "What are your opinions on Bilbo Baggins in The Hobbit?",
        15: "What are your opinions on Thorin Oakenshield?",
        16: "What are your opinions on Smaug the Dragon?",
        17: "What are your opinions on Boromir?",
        18: "What is your favorite quote from The Hobbit?",
        19: "What are your opinions on Faramir?",
        20: "What are your opinions on Éomer?",
        21: "What are your opinions on Treebeard?",
        22: "What are your opinions on Bard the Bowman?",
        23: "What are your opinions on Radagast the Brown?",
        24: "What are your opinions on Isildur?",
        25: "What are your opinions on the Balrog?",
        26: "Which scene in The Hobbit films best captures the spirit of the book?",
        27: "Frodo or Sam?",
        28: "What do you think is the most significant sacrifice made by any character in LOTR?",
        29: "What do you think is the most iconic scene in LOTR and why?",
        30: "If you could possess one item from LOTR, what would it be and why?",
        31: "What is the most memorable piece of wisdom offered by Gandalf?",
        32: "How do you think the themes of friendship and loyalty are portrayed in LOTR?",
        33: "What do you think is the most underrated character in LOTR and why?",
        34: "What do you think is the most visually stunning location in Middle-earth?",
        35: "What do you think is the most important lesson we can learn from LOTR?",
        36: "What is the most significant moment in Middle-earth history?",
        37: "Which character from LOTR do you think deserves more recognition?",
        38: "What do you think is the most significant difference between the book and film adaptations of LOTR?",
        39: "What do you think is the most epic battle in LOTR?",
        40: "What do you think is the most tragic moment in LOTR?",
        41: "What do you think is the most heartwarming moment in LOTR?",
        42: "What do you think is the most significant theme in The Hobbit?",
        43: "What do you think is the most iconic creature in Middle-earth?",
        44: "What do you think is the most significant event in the history of Middle-earth?",
        45: "What do you think is the most powerful piece of music in LOTR?",
        46: "What do you think is the most significant relationship in LOTR?",
        47: "What do you think is the most important moral dilemma faced by any character in LOTR?",
        48: "What do you think is the most significant moment of redemption in LOTR?",
        49: "What do you think is the most significant moment of betrayal in LOTR?",
        50: "What do you think is the most significant moment of courage in LOTR?",
        51: "What do you think is the most significant moment of wisdom in LOTR?",
        52: "Which character from The Hobbit do you think deserves more recognition?",
        53: "What is your favorite quote from LOTR?",
        54: "What lasting legacy do the epic tales of LOTR, The Hobbit, and Rings of Power leave on the fantasy genre?",
        55: "How does the beauty of Middle-earth enhance its storytelling?",
        56: "Which character’s growth in Middle-earth inspires you the most?",
        57: "What role does fate play in the journeys of Middle-earth’s heroes?",
        58: "What are your thoughts on the magic in Tolkien’s world?",
        59: "Which moment of friendship in LOTR stands out to you?",
        60: "What is your favorite quote from Bilbo Baggins?", #here has young bilbo picture, maybe not applicable
        61: "What element of Tolkien's world-building captivates you the most?",
        62: "Which character’s journey in LOTR resonated with you the most?",
        63: "If you could write a new Middle-earth story, what would it be about?",
        64: "What do you think is the most powerful symbol in LOTR?",
        65: "What do you think is the most significant lesson learned in Middle-earth?",
        66: "What do you think is the most powerful aspect of Tolkien’s storytelling?",
        67: "What do you think is the most significant act of heroism in LOTR?",
        68: "What do you think is the most significant moment of hope in LOTR?",
        69: "What do you think is the most significant moment of despair in LOTR?",
        70: "What do you think is the most significant moment of triumph in LOTR?",
        71: "What do you think is the most significant moment of loss in LOTR?",
        72: "What do you think is the most significant moment of sacrifice in LOTR?",
        73: "What are your opinions on the killing count game between Gimli and Legolas?",
        74: "What is the most significant moment of loyalty in LOTR?",
        75: "What are some LOTR social media accounts you'd recommend?",
        76: "What is the most significant moment of unity in LOTR?",
        77: "What is the most underrated scene in LOTR?",
        78: "What is the most underrated character in LOTR?",
        79: "What is the most underrated aspect of Middle-earth?",
        80: "What is the most powerful moment in LOTR?",
        81: "What is the most impactful death in the LOTR series?",
        82: "What is your favorite quote from Saruman?",
        83: "What is the most memorable moment from The Hobbit?",
        84: "The Shire or Rivendell: where would you rather live?",
        85: "If you could visit one place in Middle-earth, where would it be?",
        86: "What is the most iconic weapon in LOTR?",
        87: "Which LOTR character would you want as a travel companion?",
        88: "If you could change one event in LOTR, what would it be?",
        89: "If you could wield one weapon from LOTR, what would it be?",
        90: "If you were in the Fellowship, what role would you play?",
        91: "What is the most epic moment in The Hobbit?",
        92: "What is the most memorable scene from Rings of Power?",
        93: "What are your opinions of Rings of Power?",
        94: "What are your opinions on The Hobbit book?",
        95: "What are your opinions of The Hobbit movies?",
        96: "What are your opinions of the LOTR books?",
        97: "What are your opinions of the LOTR movies?",
        98: "What are your opinions of the Silmarillion?",
        99: "What are your opinions of the LOTR fan community?",
        100: "Do you prefer the LOTR movies or books?",
        101: "What are your opinions on the LOTR soundtrack?",
        102: "Which LOTR character would you want to be friends with?",
        103: "Do you prefer The Hobbit movies or books?",
        104: "If you could talk to one LOTR character, who would it be?",
        105: "If you could witness one Middle-earth event, what would it be?",
        106: "Which Middle-earth creature would you want as a pet?",
        107: "What is your favorite Middle-earth location?",
        108: "What is the most iconic line from Gandalf?",
        109: "What is the most iconic line from Aragorn?",
        110: "What is the most iconic line from Legolas?",
        111: "What is the most iconic line from Gimli?",
        112: "What is the most iconic line from Gollum?",
        113: "If you could witness one battle from LOTR, which would it be?",
        114: "What is your favorite moment of humor in LOTR?",
        115: "Which is your favorite movie trilogy: The Lord of the Rings or The Hobbit?",
        116: "What is the most powerful moment of forgiveness in LOTR?", #todo stopped here
        117: "Which is your favorite LOTR movie?",
        118: "Who is your favorite LOTR character?",
        119: "Which is your favorite Hobbit movie?",
        120: "Who is your favorite Hobbit character?",
        121: "What are your opinions on The Shire?",
        122: "What are your opinions on Rivendell?",
        123: "What are your opinions on Mirkwood Forest?",
        124: "What are your opinions on Lothlórien?",
        125: "What are your opinions on Isengard?",
        126: "What are your opinions on Gondor?",
        127: "What are your opinions on Mordor?",
        128: "When did you first learn Aragorn broke his toe in the filming of LOTR?",
        129: "What are your opinions on the LOTR extended editions?",
        130: "When did you first watch/read LOTR?",
        131: "What are your opinions on Merry and Pippin?",
        132: "What is the most iconic line from Frodo?",
        133: "What is the most iconic line from Sam?",
        134: "Dwarves or Elves?", #todo i stopped here
        135: "Dwarves or Hobbits?",
        136: "Elves or Hobbits?",
        137: "What are your opinions on The Fellowship of the Ring as a movie?",
        138: "What are your opinions on The Two Towers as a movie?",
        139: "What are your opinions on The Return of the King as a movie?",
        140: "What are your opinions on The Hobbit: An Unexpected Journey as a movie?",
        141: "What are your opinions on The Hobbit: The Desolation of Smaug as a movie?",
        142: "What are your opinions on The Hobbit: The Battle of the Five Armies as a movie?",
        143: "What are your opinions on The War of the Rohirrim as a movie?",
        144: "Are you happy with how Amazon handled Rings of Power?",
        145: "Which new character introduced in Rings of Power has become your favorite?",
        146: "What are your opinions on Galadriel in Rings of Power?",
        147: "What are your opinions on Sauron in Rings of Power?",
        148: "What are your opinions on Elrond in Rings of Power?",
        149: "What are your opinions on Durin in Rings of Power?",
        150: "What are your opinions on Disa in Rings of Power?",
        151: "Which location shown in Rings of Power would you most love to visit and why?",
        152: "Which is your favorite episode of Rings of Power?",
        153: "What is your least favorite episode of Rings of Power?",
        154: "What are your opinions on the Rings of Power soundtrack?",
        155: "What are your opinions on the Rings of Power cinematography?",
        156: "If you could change one thing about Rings of Power, what would it be?",
        157: "Who is your favorite new character introduced in The Rings of Power?",
        158: "Is Rings of Power Season 2 better than Season 1?",
        159: "Do you think The Rings of Power stays true to the spirit of Tolkien's work?",
        160: "LOTR or Star Wars?",
        161: "LOTR or Harry Potter?",
        162: "What are your opinion on Tolkien's writing style?",
        163: "LOTR or Marvel?",
        164: "What are your opinions on the LOTR fandom?",
        165: "LOTR or Game of Thrones?",
        166: "LOTR or The Hobbit?",
        167: "Aragorn or Legolas?",
        168: "Gandalf or Saruman?",
        169: "Pippin or Merry?",
        170: "Gimli or Legolas?",
        171: "LOTR: Books or movies?",
        172: "The Hobbit: Books or movies?",
        173: "If you could spend the day with one character from LOTR, who would it be?",
        174: "If you could spend the day with one character from The Hobbit, who would it be?",
        175: "If you could have one character as a mentor from LOTR who would it be?",
        176: "If you could have one character as a mentor from The Hobbit who would it be?",
        177: "What are some LOTR YouTube channels you'd recommend?",
        178: "Are there any good LOTR podcasts you'd recommend?",
        179: "What are some LOTR X (Twitter) accounts you'd recommend someone following?",
        180: "What are your opinions on Bilbo Baggins in LOTR?",
        181: "What are your opinions on Boromir's death scene?",
        182: "What are your opinions on Middle-Earth geography?",
        183: "What are your opinions on the LOTR fandom?",
        184: "What are your opinions on the LOTR video games?",
        185: "What are your opinions on the LOTR board games?",
        186: "What are your opinions on the LOTR Lego sets?",
        187: "What are your opinions on the Lego LOTR video games?",
        188: "What are your opinions on the changes made in the Hobbit movies compared to the book?",
        189: "What are your opinions on the changes made in the LOTR movies compared to the book?",
        190: "What are your opinions on J.R.R. Tolkien?",
        191: "What are your opinions on Peter Jackson?",
        192: "What is your opinion on Legolas being in The Hobbit movies but not the book?",
        193: "What is your opinion on Radagast being in The Hobbit movies but not the book?",
        194: "What is your opinion on Galadriel being in The Hobbit movies but not the book?",
        195: "What is your opinion on Tauriel being in The Hobbit movies but not the book?",
        196: "What is your opinion on Azog being in The Hobbit movies but not the book?",
        197: "What is your opinion on Saruman being in The Hobbit movies but not the book?",
        198: "What are your opinions on animated LOTR content such as The War of the Rohirrim?",
        199: "What are your thoughts on the Eagles’ rescue at the end of Return of the King?",
        200: "What are your thoughts on the ending of The Hobbit?",
        201: "What are your thoughts on the ending of LOTR?",
        202: "Which LOTR novel (Fellowship, Two Towers, or Return) resonated with you most, and why?",
        203: "What do you think about Bilbo’s character arc from The Hobbit to LOTR?",
        204: "Rohan or Gondor?",
        205: "Shelob or Balrog?",
        206: "Would you want to see a Silmarillion movie adaptation?",
        207: "Who were you hoping would win the killing count game between Gimli and Legolas?",
        208: "What role do you think C.S. Lewis had in Tolkien writing LOTR?",
        209: "What are your opinions on the direction Rings of Power is heading?",
        210: "Which would be a better title: The Magic Ring or Lord of the Rings?",



        #maybe add more "What are the most iconic lines from..." questions i currently only have frodo and sam, or maybe switch adjective instead of iconic idk




    }

    # deleted because it got no comments in April 2025:
    #        60: "How do you view the transformation of Gollum’s character?",
    #        26: "What do you think makes Aragorn such a compelling leader and hero?",
    #        82: "Book Aragorn or movie Aragorn: which portrayal is better?",
    #        52: "What do you think is the most significant moment of love in LOTR?",
    #        115: "Which character's inner journey do you find most relatable?",
    #        37: "How do you think the concept of 'home' is portrayed in LOTR?",
    #        31: "What do you think is the most powerful moment in The Hobbit?",

    # s3 bucket files look up
    lookup = {
        1: "questions/char_Frodo/",
        2: "questions/char_Samwise/",
        3: "questions/char_Gandalf/",
        4: "questions/char_Aragorn/",
        5: "questions/char_Legolas/",
        6: "questions/char_Gimli/",
        7: "questions/char_Gollum/",
        8: "questions/char_Saruman/",
        9: "questions/char_Sauron/",
        10: "questions/char_galadriel/",
        11: "questions/char_Elrond/",
        12: "questions/char_Arwen/",
        13: "questions/char_Eowyn/",
        14: "questions/char_BilboBagginsYOUNG/",
        15: "questions/char_Thorin/",
        16: "questions/char_Smaug/",
        17: "questions/char_Boromir/",
        18: "None",
        19: "questions/char_Faramir/",
        20: "questions/char_Eomer/",
        21: "questions/char_Treebeard/",
        22: "questions/char_Bard/",
        23: "questions/char_Radagast/",
        24: "questions/char_Isildur/",
        25: "questions/char_Balrog/",
        26: "None",
        27: "questions/char_FrodoORSam/",
        28: "None",
        29: "None",
        30: "None",
        31: "questions/char_Gandalf/",
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
        60: "questions/char_BilboBagginsYOUNG/",
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
        73: "questions/char_GimliORLegolas/",
        74: "None",
        75: "None",
        76: "None",
        77: "None",
        78: "None",
        79: "None",
        80: "None",
        81: "None",
        82: "questions/char_Saruman/",
        83: "None",
        84: "None",
        85: "questions/place_MiddleEarth/",
        86: "None",
        87: "None",
        88: "None",
        89: "None",
        90: "None",
        91: "None",
        92: "questions/show_RingsOfPower/",
        93: "questions/show_RingsOfPower/",
        94: "questions/other_HobbitBook/",
        95: "questions/other_HobbitMovie/",
        96: "questions/other_LOTR-Books/",
        97: "questions/other_LOTR-Movies/",
        98: "questions/other_Silmarillion/",
        99: "None",
        100: "questions/other_LOTR-BooksVMovies/",
        101: "None",
        102: "None",
        103: "questions/other_Hobbit-BookORMovie/",
        104: "None",
        105: "None",
        106: "None",
        107: "questions/place_MiddleEarth/",
        108: "questions/char_Gandalf/",
        109: "questions/char_Aragorn/",
        110: "questions/char_Legolas/",
        111: "questions/char_Gimli/",
        112: "questions/char_Gollum/",
        113: "None",
        114: "None",
        115: "questions/other_movie-LOTRorHobbit/",
        116: "None",
        117: "questions/other_LOTR-Movies/", #maybe delete this one and show just the 3 movie posters if possible idk
        118: "None",
        119: "questions/other_HobbitMovie/", #maybe delete this also and just show hobbit movies
        120: "None",
        121: "questions/place_Shire/",
        122: "questions/place_Rivendell/",
        123: "questions/place_Mirkwood/",
        124: "questions/place_Lothlorien/",
        125: "questions/place_Isengard/",
        126: "questions/place_Gondor/",
        127: "questions/place_Mordor/",
        128: "questions/other_AragornBrokeToe/",
        129: "questions/char_MerryANDPippin/",
        130: "None",
        131: "None",
        132: "questions/char_Frodo/",
        133: "questions/char_Samwise/",
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
        144: "questions/show_RingsOfPower/",
        145: "None",
        146: "None",
        147: "None",
        148: "None",
        149: "None",
        150: "None",
        151: "None",
        152: "questions/show_RingsOfPower/",
        153: "questions/show_RingsOfPower/",
        154: "None",
        155: "None",
        156: "questions/show_RingsOfPower/",
        157: "None",
        158: "None",
        159: "questions/show_RingsOfPower/",
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
        170: "questions/char_GimliORLegolas/",
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
        182: "questions/place_MiddleEarth/",
        183: "None",
        184: "None",
        185: "None",
        186: "None",
        187: "None",
        188: "questions/other_Hobbit-BookORMovie/",
        189: "questions/other_LOTR-BooksVMovies/",
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
        202: "questions/other_LOTR-Books/",
        203: "None",
        204: "None",
        205: "None",
        206: "questions/other_Silmarillion/",
        207: "questions/char_GimliORLegolas/",
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

    bucket_name = 'lotr.photos'
    file_key = 'notes/lotr_questions.txt'
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

        # index = 1
        path = lookup[index]

        question_indices.insert(0, index)
        if len(question_indices) > 150:
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

                if random.random() < 0.5:
                    replacement = "honest " + replacement
                pattern = r'\bthoughts\b'
                question = re.sub(pattern, replacement, question)
                print("REPLACED")

            # Replace "opinions" with randomly chosen word
            if contains_opinions:
                replacement = "thoughts"
                if random.random() < 0.5:
                    replacement = "opinions"

                if random.random() < 0.5:
                    replacement = "honest " + replacement
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

