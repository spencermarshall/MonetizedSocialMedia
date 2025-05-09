import random
import boto3
import tweepy
import os
import json
import re

# X credentials stored in env variables

# Twitter API authentication setup
bearer_token = "AAAAAAAAAAAAAAAAAAAAAGscvwEAAAAAD%2BE%2FA1HFvb4hGDFzbZeMyA1hLuc%3D3yngqIcsmqDYyawEm2x3TVYfPEZaKYbnDRtEfFKEc9tPLmV8gk"
api_key = "4ORKKv2122tpa1CKy6yGHZInO"
api_key_secret = "35fQjzS0sxk5AverD0ur1YP9fZN8FdkJoS6xUW71Pc4zDGltDv"
access_token = "1832642294165487616-Ro503mjfYALzFDKhSYqyRThUAiC2R9"
access_token_secret = "2NsamH45xFXmM5BPUtb8K9pAIdI3hu3lvJqm561YMKSEz"

# Set up Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)


def office_question(event, context):
    questions = {
        1: "What are your opinions on season 1 of The Office?",
        2: "Who resonates with you more: Jim or Dwight?",
        3: "Which Michael Scott quote resonates most with you and why?",
        4: "What do you think of Pam and Jim’s relationship arc?",
        5: "Who is your favorite character in The Office and why?",
        6: "How did you feel about Toby’s role at Dunder Mifflin?",
        7: "Who’s your favorite employee of the Scranton branch?",
        8: "What’s your take on Michael Scott’s management style?",
        9: "Which cold open from The Office made you laugh the hardest?",
        10: "Dwight or Andy?",
        11: "How do you feel about Angela’s cats?",
        12: "What are your opinions on the Scott’s Tots episode?",
        13: "Which guest star cameo surprised you the most in The Office?",
        14: "What are your opinions on the Pretzel Day episode?",
        15: "What’s your favorite pranking moment by Jim?",
        16: "What are your thoughts on the relationship between Jim and Dwight?",
        17: "What do you think of Michael’s ‘World’s Best Boss’ mug?",
        18: "What are your opinions on the Goodby Toby episode?",
        19: "Who’s the most underrated character in The Office?",
        20: "What is your least favorite character in The Office and why?",
        21: "Which season of The Office do you think is the best and why?",
        22: "Which season of The Office do you think is the worst and why?",
        23: "Should the show have ended after Michael Scott left at the end of Season 7?",
        24: "How did you feel about Jim’s Stamford arc?",
        25: "What is your favorite episode of The Office and why?",
        26: "What do you think of Kelly’s fashion sense?",
        27: "What are your opinions on the Halloween episode?",
        28: "What’s your take on the ‘Office’ theme song?",
        29: "What are your thoughts on the show’s depiction of office culture?",
        30: "Creed or Meredith?",
        31: "What’s your take on Michael and Jan’s relationship?",
        32: "What are your thoughts on the Jim-and-Pam proposal scene?",
        33: "How do you rank the Christmas parties across seasons?",
        34: "Which Halloween Office episode is your favorite?",
        35: "What are your opinions on the Christmas Party episode?",
        36: "Who wore it best: Dwight’s mustard shirt or Michael’s suit?",
        37: "What are your opinions on the Diversity Day episode?",
        38: "What is your least favorite episode of The Office and why?",
        39: "Which side plot in The Office gave you the most laughs?",
        40: "How do you feel about Dwight Schrute's character development?",
        41: "How do you feel about Pam’s art career?",
        42: "Which character had the best character development?",
        43: "What is your favorite quote from The Office?",
        44: "Who is the funniest supporting character in The Office?",
        45: "What’s your opinion on Jan’s candle business?",
        46: "Which Michael Scott Paper Company moment stands out?",
        47: "How did you feel about the Sabre takeover arc?",
        48: "What are your thoughts on Erin and Andy’s relationship?",
        49: "What are your opinions on the Office Olympics episode?",
        50: "What’s the best “Michael moment” in the finale?",
        51: "How do you feel about Pam’s receptionist growth?",
        52: "Which ‘Threat Level Midnight’ cameo is the best?",
        53: "What would your office prank be?",
        54: "What is your opinion on the final season of The Office?",
        55: "What are your thoughts on Dwight’s beet farm?",
        56: "Who should have replaced Michael as regional manager?",
        57: "Which quote by Kelly Kapoor is most relatable?",
        58: "Which episode of The Office made you laugh the hardest and why?",
        59: "Which ‘Beach Games’ challenge is the craziest?",
        60: "What are your opinions on the documentary within The Office?",
        61: "What is your take on Andy Bernard's character?",
        62: "What are your thoughts on the mockumentary style of The Office?",
        63: "What do you think of Gabe Lewis as a character?",
        64: "Who’s the best receptionist: Pam or Erin?",
        65: "What are your thoughts on the relationship between Dwight and Angela?",
        66: "What are your thoughts on Michael Scott’s improv side quest?",
        67: "Which episode had the most emotional impact on you and why?",
        68: "What is your favorite running gag or inside joke from the series?",
        69: "Which episode do you think is the most rewatchable and why?",
        70: "What’s your favorite Michael–Dwight duo moment?",
        71: "How do you feel about Robert California’s character?",
        72: "Which quote by Stanley Hudson is the best?",
        73: "Which episode do you think was the most controversial among fans?",
        74: "What are your opinions on the Dundie Awards episode?",
        75: "How did you feel about the Sabre printer fiasco?",
        76: "What would The Office look like in another country?",
        77: "What are your opinions on the Finale episode?",
        78: "What are your opinions on the Dinner Party episode?",
        79: "What are your opinions on the Stress Relief episode?",
        80: "What are your opinions of the relationship between Roy and Pam?",
        81: "What are your opinions on The Office finale’s time jump?",
        82: "Which Dunder Mifflin branch did you enjoy the least?",
        83: "What’s your favorite Michael Scott “catchphrase”?",
        84: "What are your opinions on the Threat Level Midnight episode?",
        85: "Which Dwight Schrute rule would you adopt?",
        86: "What do you think of Erin’s backstory?",
        87: "Which minor character deserved more screen time?",
        88: "What are your opinions of the relationship between Jim and Karen?",
        89: "Who’s the best duo: Jim & Pam or Dwight & Angela?",
        90: "What’s your favorite ‘Prison Mike’ moment?",
        91: "What are your opinions on the Beach Games episode?",
        92: "What are your thoughts on the relationship between Michael and Holly?",
        93: "What are your thoughts on the relationship between Michael and Jan?",
        94: "What are your thoughts on the relationship between Michael and Ryan?",
        95: "What are your thoughts on the relationship between Michael and Dwight?",
        96: "What is your favorite branch rivalry moment?",
        97: "Who’s the best boss: Michael or Jim?",
        98: "Which Darryl subplot is most memorable?",
        99: "What are your thoughts on the relationship between Jim and Pam?",
        100: "If you ran Dunder Mifflin, what would you change?",
        101: "What are your thoughts on Todd Packer as a character?",
        102: "What are your thoughts on Ryan Howard as a character?",
        103: "What are your thoughts on Creed Bratton as a character?",
        104: "What are your thoughts on Kevin Malone as a character?",
        105: "What are your thoughts on Phyllis Vance as a character?",
        106: "What are your thoughts on Stanley Hudson as a character?",
        107: "What are your thoughts on Angela Martin as a character?",
        108: "What are your thoughts on Pam Beesly as a character?",
        109: "What are your thoughts on Jim Halpert as a character?",
        110: "What are your thoughts on Michael Scott as a character?",
        111: "What are your thoughts on Dwight Schrute as a character?",
        112: "What are your thoughts on Andy Bernard as a character?",
        113: "What are your thoughts on Ryan Howard’s character development?",
        114: "What are your thoughts on Kelly Kapoor as a character?",
        115: "What are your thoughts on Toby Flenderson as a character?",
        116: "What are your thoughts on Meredith Palmer as a character?",
        117: "What are your thoughts on Gabe Lewis as a character?",
        118: "What are your thoughts on Erin Hannon as a character?",
        119: "What are your thoughts on Jan Levinson as a character?",
        120: "What are your thoughts on Karen Filippelli as a character?",
        121: "What are your thoughts on Oscar Martinez as a character?",
        122: "What are your thoughts on Darryl as a character?",
        123: "What are your thoughts on Robert California as a character?",
        124: "What are your thoughts on Jo Bennett as a character?",
        125: "What are your thoughts on David Wallace as a character?",
        126: "What are your thoughts on Will Ferrell’s character?",
        127: "Pam or Karen?",
        128: "What are your opinions on the relationship between Toby and Michael?",
        129: "What are your opinions on Season 9 of The Office?",
        130: "Which character from The Office would you want a spin-off show about?",
        131: "What are your thoughts on Michael Scott as a boss?",
        132: "What are your opinions on Creed as a boss?",
        133: "What are your opinions on Andy as a manager?",
        134: "What are your opinions on Jim as a Manager?",
        135: "What are your opinions on Nellie as a Manager?",
        136: "What are your opinions on Ryan as a temp?",
        137: "What are your opinions on Ryan as working at Corporate?",
        138: "What are your opinions on the Pilot episode of The Office?",
        139: "What are your opinions on the Basketball episode in Season 1?",
        140: "What are your opinions on the Email Surveillance episode?",
        141: "What were your reactions to Michael burning his foot on the George Foreman grill?",
        142: "What are your opinions on the Casino Night episode?",
        143: "What are your opinions on the Stamford branch?",
        144: "What are your opiniosn on the Stamford episodes?",
        145: "What are your opinions on Dwight's initiation with Ryan?",
        146: "What are your opinions on Michael's Movie Mondays?",
        147: "What are your opinions on The Convict episode?",
        148: "What did you think of Dwight working at Staples?",
        149: "What are your opinions on Dwight training Michael on how to negotiate?",
        150: "What are your opinions on Dunder Mifflin Infinity?",
        151: "Which TV ad was better: Pam's or the Ad agency's?",
        152: "What are your opinions on the Local Ad episode?",
        153: "What are your opinions on the Weight Loss initiative?",
        154: "What are your opinions on the Surplus episode?",
        155: "Should Michael have stolen the leads from the Prince Family Paper company?",
        156: "What are your opinions on the Golden Ticket episode?",
        157: "Should Dwight have taken the fall for the Golden Ticket Fiasco?",
        158: "What are your opinions on Charles Miner as a Manager?",
        159: "What are your opinions on Charles Miner as a character?",
        160: "What are your opinions on Michael making his own Paper company?",
        161: "What are your opinions on the Michael Scott Paper Company?",
        162: "Should Pam have left to work at the Michael Scott Paper Company?",
        163: "Did you expect the Michael Scott Paper Company to be bought out?",
        164: "Did you think Niagara was a good place for the wedding?",
        165: "What were your reactions when Michael thought he was dealing with the Mafia?",
        166: "What was your reaction when Michael fell in the Koi Pond?",
        167: "Should Michael have been dating Pam's mom?",
        168: "What were your reactions to Michael's proposal to Holly?",
        169: "What were your reactions to the Murder Mystery episode?",
        170: "What was your reaction to Michael speaking at the Shareholder meeting?",
        171: "What was your opinion on Michael hiring his nephew"


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
        89: "None",
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


    }

    bucket_name = 'office.photoss'
    file_key = 'notes/office_questions.txt'
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
        if len(question_indices) > 60:
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

