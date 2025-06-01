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


def BB_question(event, context):
    questions = {
        1: "What's the most underrated episode in Breaking Bad?",
        2: "What's the most underrated episode in Better Call Saul?",
        3: "How many times have you watched Better Call Saul?",
        4: "What are your thoughts on Jesse’s struggle in Breaking Bad?",
        5: "What makes Saul so intriguing in Breaking Bad/Better Call Saul?",
        6: "Does Kim Wexler resonate with you in Better Call Saul?",
        7: "Which moment shocked you the most in Breaking Bad?",
        8: "What’s the most iconic scene in Breaking Bad?",
        9: "Which Breaking Bad character is most relatable?",
        10: "On a scale of 1-10, how would you rate Better Call Saul?",
        11: "What's the most controversial decision in Breaking Bad?",
        12: "Which character had the most satisfying arc in Breaking Bad?",
        13: "Is Better Call Saul better than Breaking Bad?",
        14: "Do you like how law enforcement is portrayed in Breaking Bad?",
        15: "What are your thoughts on Kim Wexler as a character?",
        16: "Was Walter White justified in killing Mike?",
        17: "Was Walter White justified in letting Jane die?",
        18: "I need a new dust filter for my Hoover Max Extract Pressure Pro, Model 60.  Does anyone know who can help me with that?",
        19: "Did you like the ending of Better Call Saul?",
        20: "What were your thoughts after watching the first episode of Breaking Bad?",
        21: "What are your thoughts on how Breaking Bad addresses addiction?",
        22: "Was Walter White justified in killing Gus?",
        23: "What were your thoughts after watching the first episode of Better Call Saul?",
        24: "What are your thoughts on El Camino?",
        25: "Who is the most underrated character in Better Call Saul?",
        26: "How much does Walter's family actually influence his choices?",
        27: "Who is the most overrated character in Better Call Saul?",
        28: "Who is the best written character in Better Call Saul?",
        29: "If you could change one thing about Breaking Bad, what would it be?",
        30: "Was Walter White justified in the end for his actions?",
        31: "Did Jesse Pinkman get the ending he deserved in El Camino?",
        32: "Which Breaking Bad character transforms most dramatically?",
        33: "If you could meet one character from Breaking Bad, who would it be?",
        34: "Is Better Call Saul a worthy spin-off?",
        35: "What is the most memorable quote from Breaking Bad?",
        36: "What is the most memorable quote from Better Call Saul?",
        37: "Who is your favorite character in Better Call Saul?",
        38: "Who is your favorite character in Breaking Bad?",
        39: "Who is your least favorite character in Better Call Saul?",
        40: "What are your thoughts on how the legal system is portrayed in Better Call Saul?",
        41: "Should there be a sequel to Breaking Bad? What would it be about?",
        42: "Who is your favorite Breaking Bad villain?",
        43: "Do you like how Jesse evolves throughout Breaking Bad?",
        44: "Who is your least favorite character in Breaking Bad?",
        45: "What is your favorite Walter White quote?",
        46: "What is your favorite Jesse Pinkman quote?",
        47: "What is your favorite Saul Goodman quote?",
        48: "Which Breaking Bad character is most misunderstood?",
        49: "What’s your take on Jimmy’s legal evolution in Better Call Saul?",
        50: "What legacy do Breaking Bad and Better Call Saul leave?",
        51: "What is the funniest moment in Breaking Bad?",
        52: "What is the funniest moment from Better Call Saul?",
        53: "Does Albuquerque set the right mood in Breaking Bad?",
        54: "Which is your favorite season of Breaking Bad?",
        55: "What’s the most memorable moment in Better Call Saul?",
        56: "Which is your favorite season of Better Call Saul?",
        57: "Which is your favorite episode of Breaking Bad?",
        58: "Which is your favorite episode of Better Call Saul?",
        59: "What are your thoughts on the relationship between Jimmy and Howard in Better Call Saul?",
        60: "What are your thoughts on the relationship between Jimmy and Chuck in Better Call Saul?",
        61: "What are your thoughts on the relationship between Jimmy and Kim in Better Call Saul?",
        62: "What are your thoughts on the relationship between Walter White and Jesse in Breaking Bad?",
        63: "What are your thoughts on the relationship between Walter White and Skyler in Breaking Bad?",
        64: "What are your thoughts on the relationship between Walter White and Hank in Breaking Bad?",
        65: "Walter White or Gus Fring?",
        66: "What are your thoughts on the relationship between Walter White and Saul Goodman in Breaking Bad?",
        67: "What are your thoughts on the relationship between Jesse Pinkman and Jane in Breaking Bad?",
        68: "How did you first hear about Breaking Bad?",
        69: "What are your thoughts on Saul Goodman’s inflatable Statue of Liberty?",
        70: "What are your thoughts on Saul Goodman’s office in Breaking Bad?",
        71: "What are your thoughts on Lalo killing Howard in Better Call Saul?",
        72: "What are your opinions on Saul Goodman’s lawyer commercials?",
        73: "What are your thoughts on Saul Goodman just in Breaking Bad?",
        74: "How does Saul differ in Better Call Saul compared to Breaking Bad?",
        75: "Jimmy McGill or Howard Hamlin?",
        76: "I just finished Season 5 of Better Caul Saul and I realized Lalo and Howard haven't met yet, that would be cool if they meet sometime. Thoughts? /s",
        77: "What are your opinions on Kim working at Palm Coast Sprinklers?",
        78: "What are your opinions on Kim's character development throughout BCS?",
        79: "What are your opinions on Kim confessing her crimes to the DA?",
        80: "Why do you think Saul continued his criminal activities as Gene Takavic?",
        81: "Was Gene Takavic a good undercover character?",
        82: "What were your thoughts when Gene Takavic got recognized as Saul Goodman?",
        83: "What are your opinions on the mall theft scenes in BCS?",
        84: "What are your opinions on Hank's rock collection",
        85: "Are they rocks or minerals?",
        86: "Was Saul working at the Cinnabon a good idea?",
        87: "Do you think Jimmy should have taken the shorter jail time?",
        88: "What are your opinions on Nacho's death in BCS?",
        89: "You're the smartest guy I ever met, and you're too stupid to see he made up his mind 10 minutes ago.",
        90: "What are your opinions on the use of black and white scenes in BCS?",
        91: "What are your opinions on the death of Andrea?",
        92: "Who had the saddest death in all of BB/BCS?",
        93: "Who's death was most surprising in BB/BCS",
        94: "If you could change one thing about Better Call Saul what would it be?",  # maybe image maybe delete idk
        95: "What is your favorite moment involving Walter White?",
        96: "What is your favorite moment involving Jesse Pinkman?",
        97: "What is your favorite moment involving Gus Fring?",
        98: "What is your favorite moment involving Saul Goodman?",
        99: "What is your favorite moment involving Mike Ehrmantraut?",
        100: "What is your favorite moment involving Hank Schrader?",
        101: "What is your favorite moment involving Skyler White?",
        102: "Walter White or Jimmy McGill?",
        103: "Breaking Bad or Better Call Saul?",
        104: "What are your thoughts on Mike Ehrmantraut's death in Breaking Bad?",
        105: "What are your thoughts on Hank Schrader's death in Breaking Bad?",
        106: "What are your thoughts on Gus Fring's death in Breaking Bad?",
        107: "What are your thoughts on Walter White's death in Breaking Bad?",
        108: "What are your thoughts on Walter’s transformation throughout Breaking Bad?",
        109: "What are your thoughts on Jimmy turning into Saul in Better Call Saul?",
        110: "Is Gus Fring the top villain in Breaking Bad?",
        111: "What are your thoughts on the cameos in El Camino?",
        112: "Are Jimmy & Kim the best duo in Better Call Saul?",
        113: "Did you like the ending of Breaking Bad?",
        114: "How old were you when you first watched Breaking Bad?",
        115: "What are your views on the Salamanca family in Breaking Bad?",
        116: "What are your thoughts on the bond between Walt & Jesse strong in Breaking Bad?",
        117: "What are your thoughts on Lalo Salamanca in Better Call Saul?",
        118: "What are your thoughts on Nacho in Better Call Saul?",
        119: "What are your thoughts on Hank Schrader as a DEA agent in Breaking Bad?",
        120: "What are your thoughts on Bryan Cranston's portrayl of Walter White?",
        121: "What are your thoughts on Aaron Paul's portrayal of Jesse Pinkman?",
        122: "What are your thoughts on Bob Odenkirk's portrayal of Saul Goodman?",
        123: "What are your thoughts on Jonathan Banks' portrayal of Mike Ehrmantraut?",
        124: "What are your thoughts on Giancarlo Esposito's portrayal of Gus Fring?",
        125: "On a scale of 1-10, how would you rate El Camino?",
        126: "What are your thoughts on Anna Gunn's portrayal of Skyler White?",
        127: "What are your thoughts on Rhea Seehorn's portrayal of Kim Wexler?",
        128: "What are your thoughts on Patrick Fabian's portrayal of Howard Hamlin?",
        129: "What are your thoughts on Michael McKean's portrayal of Chuck McGill?",
        130: "How many times have you watched Breaking Bad?",
        131: "What are your thoughts on Hector Salamanca in Breaking Bad?",
        132: "What are your thoughts on Mike Ehrmantraut in Breaking Bad?",
        133: "What are your thoughts on Jesse Pinkman in Breaking Bad?",
        134: "What are your thoughts on the Breaking Bad Cameo's in Better Call Saul?",
        135: "What are your thoughts on the music in Breaking Bad?",
        136: "What are your thoughts on Walter White Jr. in Breaking Bad?",
        137: "What are your thoughts on Steven Gomez in Breaking Bad?",
        138: "What are your thoughts on Marie Schrader in Breaking Bad?",
        139: "What are your thoughts on Tuco Salamanca in Breaking Bad?",
        140: "What are your thoughts on Todd Alquist in Breaking Bad?",
        141: "What are your thoughts on Lydia Rodarte-Quayle in Breaking Bad?",
        142: "What are your thoughts on Howard Hamlin in Better Call Saul?",
        143: "What are your thoughts on Chuck McGill in Better Call Saul?",
        144: "What are your thoughts on Gene Takavic as a character in Better Call Saul?",
        145: "What are your thoughts on Francesca in Better Call Saul?",
        146: "What are your thoughts on Huell Babineaux in Breaking Bad?",
        147: "What are your thoughts on Krazy-8 in Breaking Bad?",
        148: "What are your thoughts on Jane from Breaking Bad?",
        149: "What are your thoughts on Gale Boetticher in Breaking Bad?",
        150: "What are your thoughts on Don Eladio in Breaking Bad?",
        151: "What are your thoughts on Wendy in Breaking Bad?",
        152: "Thoughts on Tyrus Kitt in Breaking Bad?",
        153: "What are your thoughts on Skinny Pete in Breaking Bad?",
        154: "What are your thoughts on Badger in Breaking Bad?",
        155: "What are your thoughts on Combo in Breaking Bad?",
        156: "What are your thoughts on RJ Mitte's portrayal of Walter White Jr. in Breaking Bad?",
        157: "What is your favorite part from El Camino?",
        158: "What are your thoughts on Tony Dalton's portrayal of Lalo Salamanca in Better Call Saul?",
        159: "What is your least favorite part from El Camino?",
        160: "What are your thoughts on the future of the Breaking Bad universe?",
        161: "Should we get another Breaking Bad Spinoff Show?",
        162: "What are your thoughts on Bill Burr's cameo in Breaking Bad?",
        163: "On a scale of 1-10, how would you rate Breaking Bad?",
        164: "What are your thoughts on Saul Goodman's fate in Better Call Saul?",
        165: "What are your thoughts on Jane's death in Breaking Bad?",
        166: "Was Todd justified in killing the kid in the Train Heist episode?",
        167: "What are your thoughts on the Fly episode?",
        168: "What are your thoughts on the character development in Breaking Bad?",
        169: "Was Walter White justified in poisoning Brock?",
        170: "What are your thoughts on Ed Galbraith?",
        171: "Why do you think Breaking Bad has such a strong fanbase?",
        172: "Was Walter White justified in killing Krazy-8",
        173: "The fly episode is either one of your favorite episodes or one of your least favorite episodes. There is no inbetween.",
        174: "What role does family loyalty actually play throughout Breaking Bad?",
        175: "How do you think Jane's death affected Jesse throughout the rest of the show?",
        176: "What role do you think Molly had in Walter White's decisions?",
        177: "What are your opinions on the entire plane crash incident?",
        178: "What are your opinions on the entire train heist idea?",
        179: "What are your opinions on the underground lab as a whole?",
        180: "Would you eat at Los Pollos Hermanos?",
        181: "What are your opinions on how Money Laundering is portrayed?",
        182: "What are your opinions on Walter buying the Car Wash?",
        183: "Would you ever buy a unsliced pizza?",
        184: "Should Walter have accepted the money from Elliot and Gretchen?",
        185: "What are your opinions on Elliot and Gretchen?",
        186: "Do you think Walter should have gotten equity in Gray Matter?",
        187: "With a qualified background, why do you think Walter stayed as a High School Chemistry teacher?",
        188: "What are your opinions on the RV that Walter and Jesse used?",
        189: "What are your opinions on the scene where Hank almost caught Jesse and Walter in the RV?",
        190: "What are your opinions on when Hank beat up Jesse?",
        191: "What are your opinions on the scene where Walter and Jesse first meet?",
        192: "Do you think Walter would have lived and recovered if he had never gotten into the meth business?",
        193: "Why do you think Walter was so obsessed with the idea of being a drug lord?",
        194: "Why do you think Hank was never able to catch Walter?",
        195: "I was just reading this book and it was signed by W.W. What name do you think that is?",
        196: "Do you think Gus should have never gotten involved with Walter and Jesse?",
        197: "Why do you think Gus initially didn't want to work with Walter and Jesse but later decided to?",
        198: "Would you want to be a fast food employee at Los Pollos Hermanos?",
        199: "What are your opinions on how Jesse's clothing?",
        200: "Do you think the pink teddy bear was a good symbol for the show?",
        201: "Who's your favorite BB character that showed up in BCS?",
        202: "Who's your least favorite BB character that showed up in BCS?",
        203: "What's the most surprising character crossover in BCS?",
        204: "What are your opinions on Jesse buying his parents house?",
        205: "Do you think the Salamanca twins were good villains?",
        206: "What are your opinions on Ted Beneke?",
        207: "What are your opiniosn on Skyler doing the deed with Ted?",
        208: "Which is your least favorite scene in BB and why is it when Skyler sings Happy Birthday to Ted?",
        209: "Who is your least favorite character in BB and why is it Skyler?",
        210: "What are your opinions when Kim Wexler met Jesse Pinkman?",
        211: "What are your opinions on Jesse's magnet idea with the evidence room?",
        212: "Should Skyler have made Walter return the car he bought for Walt Jr?",
    }

    # s3 bucket files look up
    lookup = {
        1: "questions/show_BreakingBad/",
        2: "questions/show_BetterCallSaul/",
        3: "questions/show_BetterCallSaul/",
        4: "questions/char_Jesse/",
        5: "questions/char_SaulGoodman/",
        6: "questions/char_KimWexler/",
        7: "questions/show_BreakingBad/",
        8: "questions/show_BreakingBad/",
        9: "None",
        10: "questions/show_BetterCallSaul/",
        11: "None",
        12: "questions/show_BreakingBad/",
        13: "None",
        14: "None",
        15: "questions/char_KimWexler/",
        16: "questions/other_MikeDeath/",
        17: "questions/other_JaneDeath/",
        18: "None",
        19: "questions/other_BCS_Ending/",
        20: "questions/other_BBPilot/",
        21: "None",
        22: "questions/other_GusDeath/",
        23: "questions/other_BCSPilot/",
        24: "questions/movie_ElCamino/",
        25: "questions/show_BetterCallSaul/",
        26: "None",
        27: "questions/show_BetterCallSaul/",
        28: "questions/show_BetterCallSaul/",
        29: "questions/show_BreakingBad/",
        30: "None",
        31: "questions/other_Jesse_CaminoEnding/",
        32: "None",
        33: "questions/show_BreakingBad/",
        34: "questions/show_BetterCallSaul/",
        35: "questions/show_BreakingBad/",
        36: "questions/show_BetterCallSaul/",
        37: "questions/show_BetterCallSaul/",
        38: "questions/show_BreakingBad/",
        39: "questions/show_BetterCallSaul/",
        40: "questions/other_BCSCourt/",
        41: "None",
        42: "None",  # gus or walter or ...
        43: "questions/char_Jesse/",
        44: "questions/show_BreakingBad/",
        45: "questions/char_WalterWhite/",
        46: "questions/char_Jesse/",
        47: "questions/char_SaulGoodman/",
        48: "None",
        49: "questions/char_SaulGoodman/",
        50: "None",
        51: "questions/show_BreakingBad/",
        52: "questions/show_BetterCallSaul/",
        53: "None",
        54: "questions/show_BreakingBad/",
        55: "questions/show_BetterCallSaul/",
        56: "questions/show_BetterCallSaul/",
        57: "questions/show_BreakingBad/",
        58: "questions/show_BetterCallSaul/",
        59: "questions/other_JimmyHoward/",
        60: "None",
        61: "None",
        62: "None",
        63: "None",
        64: "None",
        65: "None",
        66: "None",
        67: "None",
        68: "questions/show_BreakingBad/",
        69: "questions/other_StatueOfLiberty/",
        70: "questions/other_GoodmanOfficeBB/",
        71: "questions/other_HowardDeath/",
        72: "questions/other_SaulGoodmanCommercials/",
        73: "questions/char_SaulGoodmanBB/",
        74: "questions/char_SaulGoodman/",
        75: "questions/other_JimmyHoward/",
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
        89: "None",
        90: "None",
        91: "questions/other_AndreaDeath/",
        92: "questions/other_SaddestDeath/",
        93: "None",
        94: "None",
        95: "questions/char_WalterWhite/",
        96: "questions/char_Jesse/",
        97: "questions/char_GusFring/",
        98: "questions/char_SaulGoodman/",
        99: "None",
        100: "None",
        101: "None",
        102: "None",
        103: "None",
        104: "questions/other_MikeDeath/",
        105: "None",
        106: "questions/other_GusDeath/",
        107: "None",
        108: "questions/other_walter_transformation/",
        109: "None",
        110: "questions/char_GusFring/",
        111: "None",
        112: "None",
        113: "None",
        114: "questions/show_BreakingBad/",
        115: "None",
        116: "None",
        117: "None",
        118: "None",
        119: "None",
        120: "questions/char_WalterWhite/",
        121: "questions/char_Jesse/",
        122: "questions/char_SaulGoodman/",
        123: "None",
        124: "questions/char_GusFring/",
        125: "questions/movie_ElCamino/",
        126: "None",
        127: "questions/char_KimWexler/",
        128: "None",
        129: "None",
        130: "questions/show_BreakingBad/",
        131: "None",
        132: "None",
        133: "questions/char_Jesse/",
        134: "None",
        135: "None",
        136: "None",
        137: "questions/char_StevenGomez/",
        138: "questions/char_MarieSchrader/",
        139: "questions/char_TucoSalamanca/",
        140: "questions/char_ToddAlquist/",
        141: "questions/char_LydiaR/",
        142: "questions/char_HowardHamlin/",
        143: "questions/char_ChuckMcGill/",
        144: "questions/char_GeneTakavic/",
        145: "questions/char_Francesca/",
        146: "questions/char_Huell/",
        147: "questions/char_Krazy8/",
        148: "questions/char_Jane/",
        149: "questions/char_Gale/",
        150: "None",
        151: "None",
        152: "None",
        153: "questions/char_SkinnyPete/",
        154: "questions/char_Badger/",
        155: "questions/char_Combo/",
        156: "None",
        157: "questions/movie_ElCamino/",
        158: "None",
        159: "questions/movie_ElCamino/",
        160: "None",
        161: "None",
        162: "questions/char_BillBurr/",
        163: "questions/show_BreakingBad/",
        164: "questions/other_BCS_Ending/",
        165: "questions/other_JaneDeath/",
        166: "questions/other_ToddKillsKid/",
        167: "questions/other_Fly/",
        168: "questions/show_BreakingBad/",
        169: "questions/other_PoisonBrock/",
        170: "questions/char_Ed/",
        171: "questions/show_BreakingBad/",
        172: "None",
        173: "questions/other_Fly/",
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
        233: "None"  # "questions/char_DarthJarJar/"
    }

    bucket_name = 'bb.photos'
    file_key = 'notes/BB_questions.txt'
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
        if len(question_indices) > 150:
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




