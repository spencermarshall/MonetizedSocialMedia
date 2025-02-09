import random
import boto3
import tweepy
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


def SW_question(event, context):
    questions = {
        1: "Rebellion or Empire?",
        2: "Stormtrooper or Clone Trooper?",
        3: "Tie Fighter or X-Wing?",
        4: "Prequels or Sequels?",
        5: "What's your favorite Star Wars movie?",
        6: "Who's your favorite Star Wars character and why?",
        7: "What are your opinions on the Gonk Droid?",
        8: "Favorite Trilogy?",
        9: "Oh you're a Star Wars fan? Name every Star.",
        10: "Thoughts on the KOTOR remake?",
        11: "What are your thoughts on Star Wars Resistance?",
        12: "What are your opinions on Star Wars Rebels?",
        13: "What are your thoughts on the Clone Wars show (2003)?",
        14: "What are your thoughts on The Clone Wars?",
        15: "What are your thoughts on The Mandalorian TV Show?",
        16: "What are your opinions on the Bad Batch?",
        17: "What are your opinions on Skeleton Crew?",
        18: "What are your thoughts on Tales of the Jedi?",
        19: "What are your thoughts on Tales of the Empire?",
        20: "What are your thoughts on Star Wars Visions?",
        21: "What are your opinions on The Acolyte?",
        22: "What are your thoughts on the Ahsoka show?",
        23: "What are your thoughts on the Obi-Wan Kenobi show?",
        24: "What are your thoughts on Andor TV Show?",
        25: "What are your opinions on Book of Boba Fett?",
        26: "What are your thoughts on The Phantom Menace?",
        27: "What are your thoughts on Attack of the Clones?",
        28: "What are your thoughts on Revenge of the Sith?",
        29: "What are your thoughts on the original Star Wars movie (A New Hope)?",
        30: "What are your thoughts on The Empire Strikes Back?",
        31: "What are your thoughts on The Return of the Jedi?",
        32: "What are your opinions on The Force Awakens?",
        33: "What are your opinions on The Last Jedi?",
        34: "What are your opinions on The Rise of Skywalker?",
        35: "What are your opinions on Rogue One?",
        36: "What are your opinions on the Han Solo movie?",
        37: "What are your opinions on Bendu?",
        38: "Who's your favorite Mandalorian?",
        39: "Who's your favorite Jedi?",
        40: "Who's your favorite Sith?",
        41: "Who's your favorite Bounty Hunter?",
        42: "Who's your favorite Clone Trooper?",
        43: "Who's your favorite Droid?",
        44: "The ending of Rogue One was super good but I'm sad we have to wait until 1977 for a sequel.",
        45: "How old were you when you first discovered Star Wars?",
        46: "We know about order 66, what about the other 65 orders?",
        47: "What are your opinions on Chopper?",
        48: "Clones or Battle Droids?",
        49: "What are your thoughts on Hondo Ohnaka?",
        50: "Jedi or Sith?",
        51: "What are your thoughts on Pong Krell?",
        52: "Korkie Kryze (Duchess Satine's 'Nephew') definitely looks like he could be a Kenobi? Thoughts...?",
        53: "What are your opinions on BB-8?",
        54: "What are your opinions on Captain Phasma?",
        55: "What are your opinions on Jar Jar Binks?",
        56: "What are your opinions on the Ewoks?",
        57: "What are your opinions on the new (2017) Star Wars Battlefront 2 game?",
        58: "What are your opinions on the original Star Wars Battlefront 2 game?",
        59: "What are your opinions on the Lego Star Wars games?",
        60: "What are your opinions on the newer Lego Star Wars: Skywalker Saga game (2022)?",
        61: "What are your opinions on Jedi Fallen Order?",
        62: "What are your opinions on the Star Wars Squadrons game (2020)?",
        63: "What are your opinions on the Star Wars: Knights Of The Old Republic game?",
        64: "What are your opinions on Jedi Survivor?",
        65: "What are your opinions on Cal Kestis?",
        66: "What are your opinions on Sith Troopers from Ep9?",
        67: "What are your opinions on Babu Frik?",
        68: "What are your thoughts on Darth Revan?",
        69: "What are your honest opinions on Reva?",
        70: "If you could create your own Star Wars story—set in any era, featuring any characters—what would be its main focus?",
        71: "BREAKING: Darth Vader is Luke's father!",
        72: "What are your honest opinions on Dave Filoni?",
        73: "What are your honest opinions on George Lucas?",
        74: "What are you honest opinions on Rey being a Skywalker?",
        75: "How do you pronounce LAAT?",
        76: "Sith or Jedi?",
        77: "Should Disney make a new Star Wars trilogy? When would it be set?",
        78: "What are your opinions on Anakin in the prequels? No hate, just genuinely curious.",
        79: "It is never okay to bully/harass an actor or actress because of the character they played.",
        80: "What are your thoughts on the Star Wars Holiday Special?",
        81: "Which Star Wars ship or vehicle would you most like to pilot, and why?",
        82: "What did you ENJOY about the sequel trilogy?",
        83: "Should Reylo be a thing?",
        84: "Did Mace Windu survive the fall in ROTS?",
        85: "Who is the best Star Wars couple?",
        86: "Which is your favorite Star Wars Trilogy?",
        87: "Which is your favorite Star Wars live action TV show?",
        88: "Which is your favorite Star Wars animated TV show?",
        89: "What are your opinions on Yoda as a Puppet in Ep 1?",
        90: "What are your opinions on Ray Park as Darth Maul",
        91: "What are your thoughts on Qui-Gon Jinn coming back as a Force Ghost in the Kenobi show??",
        92: "What are your thoughts on C-3PO's red arm?",
        93: "What are your thoughts on C-3PO?",
        94: "What are your thoughts on R2-D2?",
        95: "What are your opinions on Ezra Bridger in Rebels",
        96: "What are your opinions on Kanan Jarrus?",
        97: "What are your opinions on the High Republic Era?",
        98: "What are your opinions on the Plagueis book?",
        99: "What are your opinions on Novelizations of the SW movies?",
        100: "What are your opinions on the Star Wars comics?",
        101: "What are your thoughts on the Star Wars novels?",
        102: "What are your opinions on the Star Wars: Galaxy's Edge theme park?",
        103: "What are your thoughts on the Star Wars Expanded Universe (Legends)?",
        104: "If you could create a new Force power, what would it be?",
        105: "What Star Wars creature would you most want as a pet?",
        106: "Would you ever consider joining the Jedi Order or the Sith if you lived in the Star Wars universe?",
        107: "If you could have any Star Wars weapon, which one would you choose?",
        108: "If you were a bounty hunter in the Star Wars universe, who would you want as a partner?",
        109: "What Star Wars character do you think deserves their own spin-off series?",
        110: "Who do you think is the most underrated character in Star Wars?",
        111: "What is your favorite Star Wars quote?",
        112: "What is your favorite Star Wars planet?",
        113: "What is your favorite Star Wars species?",
        114: "What is your favorite Star Wars ship?",
        115: "What do you think would have happened if Anakin had never turned to the Dark Side?",
        116: "Have you read any of the Star Wars books? Legends or Disney Canon?",
        117: "What is your favorite Star Wars book?",
        118: "What is your favorite Star Wars comic?",
        119: "What is your favorite Star Wars planet, and what makes it stand out?",
        120: "If you could spend a day with any Star Wars character, who would it be and why?",
        121: "If you could rewrite one Star Wars character’s arc, who would it be and what would you change?",
        122: "What’s your opinion on the role of politics in the Star Wars universe?",
        123: "What’s the most emotional moment in Star Wars for you?",
        124: "Which Star Wars character do you think had the most wasted potential?",
        125: "Which Star Wars movie or show has the best soundtrack?",
        126: "What’s your opinion on the relationship between Anakin and Padmé?",
        127: "Which Star Wars droid do you think is the most useful?",
        128: "Which Star Wars character do you think had the most tragic backstory?",
        129: "What are your thoughts on the idea of a Star Wars story told from the perspective of a stormtrooper?",
        130: "What are your opinions on the portrayal of the Jedi in the High Republic era?",
        131: "What are your thoughts on the idea of a Star Wars story set entirely in the criminal underworld?",
        132: "What are your opinions on the portrayal of the Empire in the animated shows versus the movies?",
        133: "What are your thoughts on the idea of a Star Wars story told from the perspective of a droid?",
        134: "What are your opinions on the portrayal of the Jedi Council in the prequels?",
        135: "What are your thoughts on the idea of a Star Wars story set during the Old Republic era?",
        136: "What are your opinions on the portrayal of the Sith in the prequels?",
        137: "What are your thoughts on the concept of the World Between Worlds in Star Wars lore?",
        138: "What are your thoughts on the relationship between Obi-Wan Kenobi and Satine Kryze?",
        139: "Do you think the Jedi Council was too rigid in their beliefs? Why or why not?",
        140: "What are your opinions on the portrayal of Anakin Skywalker's fall to the dark side?",
        141: "What are your thoughts on how Clone Troopers were treated after Order 66?",
        142: "How do you feel about Lando Calrissian’s role in both the original trilogy and his return in ep9?",
        143: "If you could choose one non-canon story to make canon, which one would it be and why?",
        # pictures below here
        144: "What are your opinions on Mace Windu?",
        145: "What are your opinions on Chancellor Valorum?",
        146: "What are your opinions on Watto?",
        147: "What are your opinions on Shmi Skywalker?",
        148: "What are your opinions on Jake Lloyd's portrayal of Anakin Skywalker?",
        149: "What are your thoughts on Aura Sing appearing in ep1 during the Pod Race scene?",
        150: "What are your opinions on Jango Fett?",
        151: "What are your thoughts on Count Dooku?",
        152: "What are your opinions on General Grievous?",
        153: "What are your thoughts on Dexter Jettster?",
        154: "What are your opinions on the Kaminoans?",
        155: "What are your thoughts on the Geonosians?",
        156: "What are your thoughts on Natalie Portman's portrayal of Padmé Amidala?",
        157: "What are your thoughts on Ki-Adi-Mundi?",
        158: "What are your thoughts on Kit Fisto?",
        159: "What are your thoughts on Aayla Secura?",
        160: "What are your thoughts on Saw Gerrera?",
        161: "What are your thoughts on the Nightsisters?",
        162: "What are your thoughts on Jyn Erso?",
        163: "What are your thoughts on K-2SO?",
        164: "What are your thoughts on Director Krennic?",
        165: "What are your thoughts on Mon Mothma in Rogue One and Andor?",
        166: "What are your thoughts of Cassion Andor just in Rogue One? What about in his TV show?",
        167: "What are your thoughts on Alden Ehrenreich's portrayal of Han Solo?",
        168: "What are your thoughts on Donald Glover's portrayal of Lando Calrissian?",
        169: "What are your thoughts on Qi'ra character in Solo?",
        170: "What are your thoughts on Tobias Beckett?",
        171: "What are your thoughts on L3-37 in the Han Solo movie?",
        172: "What are your thoughts on Dryden Vos?",
        173: "What are your thoughts on Enfys Nest from the Han Solo Movie?",
        174: "What are your thoughts on Maul's cameo in the Han Solo Movie?",
        175: "What are your thoughts on how Han Solo got his name in the Han Solo Movie?",
        176: "What are your thoughts on Han Solo's origin story in the Han Solo Movie?",
        177: "Should we get a sequel to the Han Solo Movie?",
        178: "What are your thoughts of how they portrayed Luke Skywalker in the Sequel Trilogy?",
        179: "What are your thoughts on how they portrayed Leia in the Sequel Trilogy?",
        180: "What are your thoughts on how they portrayed Han Solo in the Sequel Trilogy?",
        181: "What are your thoughts on how they portrayed R2-D2 and C-3PO in the Sequel Trilogy?",
        182: "What are your thoughts on Poe Dameron?",
        183: "What are your thoughts on Finn?",
        184: "What are your thoughts on Rey?",
        185: "What are your thoughts on Maz Kanata?",
        186: "What are your thoughts on Snoke in the Sequels?",
        187: "What are your thoughts on General Hux in the Sequels?",
        188: "What are your thoughts on Iden Versio?",
        189: "What are your thoughts on J. J. Abrams?",
        190: "What are your thoughts on Rian Johnson?",
        191: "What are your thoughts on Kathleen Kennedy?",
        192: "What are your thoughts on the Sequel Trilogy as a whole?",
        193: "What are your thoughts on the Sequel Trilogy's ending?",
        194: "What are your thoughts on Rosario Dawson as Ahsoka Tano?",
        195: "What are your thoughts on the portrayal of Ahsoka Tano in The Mandalorian?",
        196: "What are your thoughts on the portrayal of Bo-Katan in The Mandalorian?",
        197: "What are your thoughts on the portrayal of Boba Fett in The Mandalorian?",
        198: "What are your thoughts on the portrayal of Luke Skywalker in The Mandalorian?",
        199: "What are your thoughts on Grogu (Baby Yoda) in The Mandalorian?",
        200: "What are your thoughts on Moff Gideon?",
        201: "What are your thoughts on Cara Dune?",
        202: "What are your thoughts on Greef Karga?",
        203: "What are your thoughts on Dave Filoni showing up in The Mandalorian?",
        204: "What are your thoughts on Cobb Vanth?",
        205: "What are your thoughts on the portrayal of the Tusken Raiders in The Mandalorian?",
        206: "What are your thoughts on Fennec Shand?",
        207: "What are your thoughts on Dr. Pershing?",
        208: "What are your thoughts on IG-11?",
        209: "What are your thoughts on Kuiil?",
        210: "What are your thoughts on Bib Fortuna?",
        211: "What are your thoughts on The Armorer?",
        212: "What are your thoughts on Bill Burr appearing in The Mandalorian",
        213: "What are your thoughts on Hera Syndulla's portrayal in live action?",
        214: "Is the Ahsoka show just Rebels Season 5?",
        215: "What are your opinions on Jude Law?",
        216: "What are your thoughts on Omega from The Bad Batch?",
        217: "What are your thoughts on Crosshair from The Bad Batch?",
        218: "What are your thoughts on Hunter from The Bad Batch?",
        219: "What are your thoughts on Tech from The Bad Batch?",
        220: "What are your thoughts on Wrecker from The Bad Batch?",
        221: "What are your thoughts on Echo from The Bad Batch?",
        222: "What are your thoughts on the Bad Batch as a whole?",
        223: "What are your thoughts on the Bad Batch's portrayal of Order 66?",
        224: "What are your thoughts on the Bad Batch's portrayal of the Empire?",
        225: "What are your thoughts on the Bad Batch's portrayal of the Kaminoans?",
        226: "What are your thoughts on Leia's portrayal in the Kenobi Show?",
        227: "What are your thoughts on the Kenobi Show's portrayal of Obi-Wan Kenobi?",
        228: "What are your thoughts on the Kenobi Show's portrayal of Darth Vader?",
        229: "What are your thoughts on the Kenobi Show's portrayal of Owen and Beru Lars?",
        230: "What are your thoughts on the Kenobi Show's portrayal of the Inquisitors?",
        231: "What are your thoughts on the Kenobi Show's portrayal of Senator Organa?",
        232: "What are your thoughts on Kumail Ali Nanjiani's character in the Obi-Wan Kenobi show?",
        233: "What are your thoughts on Darth Jar Jar?"
    }

    # s3 bucket files look up
    lookup = {
        89: "questions/char_Yoda(puppet)/",  # yoda puppet
        215: "questions/char_JudeLaw/",
        216: "questions/char_Omega/",
        217: "questions/char_Crosshair/",
        218: "questions/char_Hunter/",
        219: "questions/char_Tech/",
        220: "questions/char_Wrecker/",
        221: "questions/char_Echo/",
        226: "questions/char_Leia(Kenobi-show)/",
        227: "questions/char_Obi-Wan(Kenobi-Show)/",
        228: "questions/char_Vader(Kenobi-show)/",
        229: "questions/char_OwenBeruLars(Kenobi-show)/",
        230: "None",
        231: "questions/char_SenatorOrgana(Kenobi-Show)/",
        232: "questions/char_Kumail(Kenobi-Show)/",
        233: "questions/char_DarthJarJar/"
    }

    bucket_name = 'starwars.photos'
    file_key = 'notes/SW_questions.txt'
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

        # gets image from s3 bucket, not yet implemented
        # temp = lookup[index]
        # response = s3.list_objects_v2(Bucket=bucket_name, Prefix=temp)
        # if 'Contents' not in response:
        #     return {
        #         'statusCode': 404,
        #         'body': 'No files found in the specified directory.'
        #     }
        # # Extract file keys (paths) from the response
        # file_keys = [obj['Key'] for obj in response['Contents'] if obj['Key'] != temp]
        # # Check if there are files to choose from
        # if not file_keys:
        #     return {
        #         'statusCode': 404,
        #         'body': 'No files found in the specified directory.'
        #     }
        # # Pick a random file from the list
        # random_file = random.choice(file_keys)

        question_indices.insert(0, index)

        # Ensure the list does not exceed its original length
        if len(question_indices) > 100:
            question_indices.pop()  # Remove the last element

        # Convert the updated list back to JSON string
        updated_content = json.dumps(question_indices)

        # Upload the updated content back to S3
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)
        question = questions[index]

        client.create_tweet(text=question)
        # these 4 are for image, not implemented yet:   TODO
        # download_path = f"/tmp/{os.path.basename(random_file)}"
        # s3.download_file(bucket_name, random_file, download_path)
        # media = api.media_upload(download_path)
        # client.create_tweet(text=question, media_ids=[media.media_id])

        return {
            'statusCode': 200,
            'body': f"Updated SW_questions.txt with new index {index}."
        }


    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }

    # post tweet question

    # update 50 most recent dynamo DB, FIFO so it keeps track of 50 most recent questions/id
