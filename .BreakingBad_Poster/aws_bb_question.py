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
        1: "What are your opinions on Jesse buying his parents house?",
        # 2: "Who was the most surprising character crossover in BCS?",
        2: "Other than Saul Goodman, who deserves a spin-off show?",
        3: "How many times have you watched BCS?",
        4: "",
        5: "Who was the real villain of Breaking Bad?",
        6: "Who had the worst fate in Breaking Bad?",
        7: "Which moment shocked you the most in Breaking Bad?",
        8: "What’s the most iconic scene in Breaking Bad?",
        # 9: "Which Breaking Bad character is most relatable?",
        9: "Who's your favorite BB character that showed up in BCS?",
        10: "On a scale of 1-10, how would you rate Better Call Saul?",
        11: "What's the most controversial decision in Breaking Bad?",
        12: "Who had the most satisfying arc in Breaking Bad?",
        13: "Is Better Call Saul better than Breaking Bad?",
        14: "Why do you think Walter was so obsessed with the idea of being a drug lord?",
        15: "What are your thoughts on Kim Wexler?",
        16: "Was Walter White justified in killing Mike?",
        17: "Was Walter White justified in letting Jane die?",
        18: "I need a new dust filter for my Hoover Max Extract Pressure Pro, Model 60.  Does anyone know who can help me with that?",
        19: "Did you like the ending of Better Call Saul?",
        20: "Did you like the Breaking Bad Pilot?", #todo maybe delete
        21: "Should Skyler have made Walter return the car he bought for Walt Jr?",
        22: "Was Walter White justified in killing Gus?",
        23: "What were your thoughts after watching the BCS Pilot?",
        24: "What are your thoughts on El Camino?",
        25: "Post an unpopular Breaking Bad universe opinion.",
        26: "How much does Walter's family actually influence his choices?",
        27: "Did you feel any sympathy for Lydia?",
        28: "Who is the best written character in BCS?",
        29: "If you could change one thing about Breaking Bad, what would it be?",
        30: "Was Walter White justified in the end for his actions?",
        31: "Do you like the ending Jesse got in El Camino?",
        32: "Which Breaking Bad character changes the most?", #delete if bad
        33: "If you could meet one character from Breaking Bad, who would it be?",
        34: "Is Better Call Saul a worthy spin-off?",
        35: "What is the most memorable quote from Breaking Bad?",
        36: "What is the most memorable quote from Better Call Saul?",
        37: "Who is your favorite character in Better Call Saul?",
        38: "Who is your favorite character in Breaking Bad?",
        39: "Who is your least favorite character in Better Call Saul?",
        40: "Who is the better villain: Gus Fring or Tuco", #maybe say who was scarier
        41: "Should there be a sequel to Breaking Bad? What would it be about?",
        42: "Who is your favorite Breaking Bad villain?",
        43: "If Jimmy and Kim had a baby, what would the name be?",
        44: "Who is your least favorite character in Breaking Bad?",
        45: "What is your favorite Walter White quote?",
        46: "What is Jesse Pinkman's most iconic line?",
        47: "What is your favorite Saul Goodman quote?",
        48: "What are your opinions on Ted Beneke?",
        # 49: "What’s your take on Jimmy’s legal evolution in BCS?",
        49: "Did you like that scene when Hank almost caught Jesse and Walter in the RV?",
        50: "You have to spend a weekend with one character. Who would it be?",
        51: "What is the funniest moment in Breaking Bad?",
        52: "What is the funniest moment from Better Call Saul?",
        53: "Is Albuquerque the right place for Breaking Bad to be set?", #todo maybe delete
        54: "Which season of Breaking Bad is your favorite?",
        55: "What’s the most memorable moment in Better Call Saul?",
        56: "Which is your favorite season of Better Call Saul?",
        57: "Which is your favorite Breaking Bad episode?",
        58: "Which show had the better series finale: Breaking Bad or Better Call Saul?",
        # 59: "Did you like the relationship between Jimmy and Howard?",
        60: "If you could prevent one death in the entire universe, who would it be?",
        61: "Did you like the relationship between Jimmy and Kim?",
        62: "Did you like the relationship between Walter White and Jesse?", #todo 4 comments, maybe delete
        63: "Did you like the scene where Walter and Jesse first meet?",
        # 64: "Did you like the relationship between Walter White and Hank?",
        64: "Would you ever buy a unsliced pizza?",
        65: "Walter White or Gus Fring?",
        66: "Walter White or Saul Goodman?",
        67: "Which Breaking Bad death shocked you the most?",
        68: "Tweet like you're Walt Jr.",
        69: "Did you like the inflatable Statue of Liberty?",
        70: "Did you like Saul Goodman’s office?",
        71: "What are your thoughts on Howard's death?",
        72: "Did you like Saul Goodman’s lawyer commercials?",
        73: "Did you like Saul Goodman just in Breaking Bad?",
        # 74: "How does Saul differ in BCS compared to Breaking Bad?",
        74: "Why do you think Hank was never able to catch Walter?",
        75: "Jimmy McGill or Howard Hamlin?",
        76: "I just finished Season 5 of Better Caul Saul and I realized Lalo and Howard haven't met yet, that would be cool if they meet sometime. Thoughts? /s",
        # 77: "What are your opinions on Kim working at Palm Coast Sprinklers?",
        77: "Should Walter have accepted the money from Elliot and Gretchen?", #todo add separate and new image folder than what is now, s1 scenes only
        78: "Who is the top villain in Breaking Bad?",
        79: "Should Kim have confessed her crimes to the DA?", #todo maybe delete
        80: "Why do you think Saul continued his criminal activities as Gene Takavic?",
        # 81: "Was Gene Takavic a good undercover character?",
        81: "Would you want to be a fast food employee at Los Pollos Hermanos?",
        82: "What is your least favorite scene in BB and why is it when Skyler sings Happy Birthday to Ted?",
        83: "What are your thoughts on Skyler doing the deed with Ted?",
        84: "What are your opinions on Hank's rock collection",
        85: "Are they rocks or minerals?",
        86: "Was Saul working at the Cinnabon a good idea?", #delete if bad
        87: "Do you think Jimmy should have taken the shorter jail time?",
        88: "Should Nacho have survived BCS?", #todo maybe delete or delete the one under this
        # 88: "What are your opinions on Nacho's death in BCS?",
        89: "You're the smartest guy I ever met, and you're too stupid to see he made up his mind 10 minutes ago.", #delete if bad
        90: "What are your opinions on Elliot and Gretchen?",
        91: "What are your opinions on the death of Andrea?",
        92: "Who had the saddest death in all of BB/BCS?",
        93: "Who's death was most surprising in BB/BCS", #delete if bad
        94: "If you could change one thing about BCS what would it be?",  # todo add image
        95: "What is your favorite Walter White moment?",
        96: "What is the smartest Gus Fring move?",
        97: "What is your favorite Gus Fring moment?",
        98: "What is your favorite Saul Goodman moment?",
        99: "What is your favorite Mike Ehrmantraut moment?",
        # 100: "What is your favorite moment involving Hank Schrader?",
        100: "I was just reading this book and it was signed by W.W. What name do you think that is?",
        101: "What are your thoughts on Skyler White?",
        102: "Walter White or Jimmy McGill?",
        103: "Breaking Bad or Better Call Saul?",
        104: "What are your thoughts on Mike Ehrmantraut's death?",
        105: "Did Hank Schrader have to die?",
        106: "What are your thoughts on Gus Fring's death?",
        107: "Should Walter White have gotten away with his crimes?", #todom maybe reword or delete
        108: "Did you like Walter’s transformation throughout Breaking Bad?",
        109: "Tweet like you're Tuco",
        110: "Is Gus Fring the top villain in Breaking Bad?",
        111: "Did you like the cameos in El Camino?",
        112: "Who is the best duo in BCS?",
        113: "Did you like the ending of Breaking Bad?",
        114: "When did you first discover Breaking Bad?", #todo maybe delete
        115: "Did you like the Salamanca family?",
        116: "Did you like the bond between Walt & Jesse?",
        117: "Did you like Lalo Salamanca?", #delete if bad
        118: "What are your thoughts on Nacho?",
        119: "Did you like Hank Schrader as a DEA agent?",
        120: "Did you like Bryan Cranston as Walter White?",
        121: "Did you like Aaron Paul's as Jesse Pinkman?",
        122: "Did you like Bob Odenkirk as Saul Goodman?", #todo maybe reword or delete
        123: "Did you like Jonathan Banks as Mike Ehrmantraut?",
        124: "Did you like Giancarlo Esposito as Gus Fring?",
        125: "On a scale of 1-10, how would you rate El Camino?",
        126: "Did you like Anna Gunn as Skyler White?",
        127: "Did you enjoy Rhea Seehorn as Kim Wexler?",
        128: "Who is your least favorite character in BB and why is it Skyler?",
        129: "Did you like Michael McKean as Chuck McGill?",
        130: "How many times have you watched Breaking Bad?",
        131: "What are your thoughts on Hector Salamanca?",
        132: "What are your thoughts on Mike Ehrmantraut?",
        133: "Did you like Jesse Pinkman?", #maybe reword to thoughts
        134: "",
        135: "Did you like when Kim Wexler met Jesse Pinkman?",
        136: "What are your thoughts on Walter White Jr.?",
        137: "What are your thoughts on Steven Gomez?",
        138: "What are your thoughts on Marie Schrader?",
        139: "What are your thoughts on Tuco Salamanca?",
        140: "What are your thoughts on Todd Alquist?",
        141: "What are your thoughts on Lydia?",
        142: "What are your thoughts on Howard Hamlin?",
        143: "What are your thoughts on Chuck McGill?",
        144: "Ddi you like Gene Takavic?",
        145: "Did you like Francesca?", #todo maybe delete
        146: "What are your thoughts on Huell Babineaux?",
        147: "What are your thoughts on Krazy-8?",
        148: "What are your thoughts on Jane?",
        149: "What are your thoughts on Gale Boetticher?",
        150: "What are your thoughts on Don Eladio?",
        # 151: "What are your thoughts on Wendy?",
        151: "What do you think happened to Huell Babineaux after the events of Breaking Bad?", #todo add image
        152: "Did you like Tyrus Kitt?", #delete if bad
        153: "What are your thoughts on Skinny Pete?",
        154: "What are your thoughts on Badger?",
        155: "What are your thoughts on Combo?",
        156: "Did you like RJ Mitte as Walter White Jr.?",
        157: "What is your favorite part of El Camino?",
        158: "Did you like Tony Dalton as Lalo Salamanca?",
        159: "What is your least favorite part of El Camino?",
        160: "What are your thoughts on the future of the Breaking Bad universe?",
        161: "Should we get another Breaking Bad Spinoff Show?",
        162: "Did you like Bill Burr's cameo?",
        163: "On a scale of 1-10, how would you rate Breaking Bad?",
        164: "Did you like Saul Goodman's fate in Better Call Saul?",
        165: "What are your thoughts on Jane's death?",
        166: "Was Todd justified in killing the kid in the Train Heist episode?",
        167: "Did you like the Fly episode?",
        168: "Do you think the Salamanca twins were good villains?",
        169: "Was Walter White justified in poisoning Brock?",
        170: "What are your thoughts on Ed Galbraith?",
        171: "Why do you think Breaking Bad has such a strong fanbase?",
        172: "Was Walter White justified in killing Krazy-8",
        # 173: "The fly episode is either one of your favorite episodes or one of your least favorite episodes. There is no inbetween.",
        # 174: "What role does family loyalty actually play throughout Breaking Bad?",
        173: "Should we have seen more High School Chemistry teacher scenes?",
        174: "Was it smart for Gus to have gone in business Walter and Jesse?",
        # 175: "How do you think Jane's death affected Jesse throughout the rest of the show?",
        175: "Which Breaking Bad scene made you cry?",
        176: "What affect did Molly have on Walt?", #todo maybe delete idk
        177: "Would you eat at Los Pollos Hermanos?",
        178: "Did you like the train heist idea?", #todo add image
        179: "What are your opinions on the underground lab as a whole?",
        180: "Which Breaking Bad scene made you laugh the most?",
        181: "Which Breaking Bad scene made you cringe the most?",
        182: "Which Breaking Bad episode hit you the hardest?",
        183: "Is the hate on Skyler White justified?",
        184: "What's your favorite BB meme?",
        185: "Post your BB memes below",
        186: "Who is the most underrated character in BB?",
        187: "Who is the most underrated character in BCS?",
        #everything below here is test / demo and new
        188: "What are your opinions on the RV that Walter and Jesse used?",
        189: "What’s your take on Gus’s backstory revealed in BCS?",
        190: "What’s the most shocking BB death scene?",
        191: "What’s the most underrated episode of Breaking Bad?",
        192: "Tweet like you're Walter White",
        # 193: "How do you feel about Walter’s confession tape?",
        193: "What was the most clever scam Jimmy and Kim ever pulled off?",
        194: "What's your favorite Gus Fring quote?",
        195: "What’s your favorite Kim Wexler quote?",
        196: "Which character deserved more screen time?",
        197: "Should there be a spin-off focused on Gus?",
        198: "What’s your favorite Mike Ehrmantraut quote?",
        199: "When did you realize Breaking Bad wasn’t just another show?",
        200: "Who is the funniest side character in Breaking Bad?",
        201: "What’s your favorite Hank Schrader quote?",
        202: "What’s your favorite Saul Goodman quote?",
        203: "What’s the most clever scam in Better Call Saul?",
        204: "Was Hank the real hero of Breaking Bad?",
        205: "What are your opinions on Hank?",
        206: "Tell me your opinion on Breaking Bad which will have everyone react to you like this...",
        207: "Which Breaking Bad scene hit you the hardest?",
        208: "What’s the most rewatchable episode of Better Call Saul?",
        209: "What is your favorite Howard Hamlin quote?",
        210: "What's your favorite Nacho quote?",
        211: "What's your favorite Lalo quote?",
        212: "What’s the most rewatchable episode of Breaking Bad?",
        213: "Tweet like you live in Albuquerque",
        214: "What's a small BB detail you only noticed after multiple rewatches.",
        215: "Tweet like you're Gus Fring",
        216: "Tweet like you're Hank",
        217: "What are your thoughts on Nacho's relationship with his father?",
        218: "Tweet like you're Jesse",
        219: "Tweet like you're Kim Wexler", #delete if bad
        220: "Tweet like you're Lalo",
        221: "Tweet like you're Marie",
        222: "Tweet like you're Mike",
        223: "Tweet like you're Nacho",
        224: "Tweet like you're Saul Goodman",
        225: "Tweet like you're Skyler",
        226: "Tweet like you're Ted",
        227: "Tweet like you're Todd",
        228: "What are your opinions on Los Pollos Hermanos",
        229: "What are your opinions on the underground lab as a whole?", #todo add image
        230: "What’s your take on Jesse’s relationship with Andrea?",
        231: "Who had the best wardrobe in Breaking Bad?",
        232: "Should Mike have trusted Walter more?", #todo add image
        233: "Who had the best one-liner in Breaking Bad?",
        234: "Did Marie Schrader get a fitting end to her story?",
        235: "What’s the most intense chase scene in BCS?",
        236: "What’s the most intense chase scene in Breaking Bad?",
        237: "Which scene is the true turning point where Walt became Heisenberg?",
        238: "Who is the most loyal character in the Breaking Bad universe?",
        239: "Was Gus Fring's revenge on the cartel satisfying?",
        240: "Should there be a spin-off about the Salamanca family?",
        241: "Tweet like you're Skinny Pete",
        242: "Tweet like you're Badger", #delete if bad
        243: "Tweet like you're Combo",
        244: "Did you like the way Hank discovered Walter's secret?", #todo add image
        245: "What are your opinions on the way Walter handled his cancer diagnosis?",
        246: "Who is the smartest character in BCS?",
        247: "What’s your favorite quote from Breaking Bad?",
        248: "What’s your favorite quote from Better Call Saul?",
        249: "Who had the worst luck in the Breaking Bad universe?",
        250: "Was Lalo the scariest villain in BCS?",
        251: "Tweet like you're Gale Boetticher",
        252: "What are your thoughts on the Mesa Verde scam?",
        253: "What’s the best plot twist in Breaking Bad?",
        254: "Should Skyler have divorced Walter earlier?",
        255: "Tweet like you're Hector Salamanca",
        256: "Was Mike's granddaughter storyline necessary?",
        257: "What’s the smartest plan Walter ever pulled off?",
        258: "Who had the best death scene in Breaking Bad?",
        259: "Did you like the way Gus walked out after the explosion?",
        260: "Should there be a spin-off about Mike's past?",
        261: "Who is the best sidekick in Breaking Bad?",
        262: "Tweet like you're Krazy-8",
        263: "Tweet like you're Steven Gomez",
        264: "What’s your favorite cold open in Breaking Bad?",
        265: "What are your opinions on the pink teddy bear?",
        266: "Was Hank's death inevitable?",
        267: "What is the greatest lesson you learned from watching Brekaing Bad?",





        # 181: "What are your opinions on how Money Laundering is portrayed?",
        # 182: "Was it a smart move for them to buy the Car Wash?",

        # 188: "What are your opinions on the RV that Walter and Jesse used?",

        # 192: "Do you think Walter would have lived and recovered if he had never gotten into the meth business?",

        # 200: "Did you enjoy Jesse's magnet idea with the evidence room?",

    }

    # s3 bucket files look up
    lookup = {
        1: "questions/other_JesseBuyingHouse/",
        2: "None",
        3: "questions/show_BetterCallSaul/",
        4: "None",
        5: "questions/char_SaulGoodman/",
        6: "None",
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
        25: "None",
        26: "None",
        27: "None",
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
        43: "None",
        44: "questions/show_BreakingBad/",
        45: "questions/char_WalterWhite/",
        46: "questions/char_Jesse/",
        47: "questions/char_SaulGoodman/",
        48: "questions/char_Ted/",
        49: "questions/other_RvHank/",
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
        68: "questions/char_WaltJr/",
        69: "questions/other_StatueOfLiberty/",
        70: "questions/other_GoodmanOfficeBB/",
        71: "questions/other_HowardDeath/",
        72: "questions/other_SaulGoodmanCommercials/",
        73: "questions/char_SaulGoodmanBB/",
        74: "None",
        75: "questions/other_JimmyHoward/",
        76: "questions/char_LaloSalamanca/",
        77: "questions/char_ElliotAndGretchen/",
        78: "None",
        79: "None",
        80: "questions/char_GeneTakavic/",
        81: "questions/other_LosPollosHermanos/",
        82: "questions/other_SkylerSingsHBD/",
        83: "None",
        84: "None",
        85: "None",
        86: "None",
        87: "None",
        88: "questions/char_Nacho/",
        89: "None",
        90: "questions/char_ElliotAndGretchen/",
        91: "questions/other_AndreaDeath/",
        92: "questions/other_SaddestDeath/",
        93: "None",
        94: "None",
        95: "questions/char_WalterWhite/",
        96: "questions/char_GusFring",
        97: "questions/char_GusFring/",
        98: "questions/char_SaulGoodman/",
        99: "questions/char_MikeE/",
        100: "None",
        101: "questions/char_Skyler/",
        102: "None",
        103: "None",
        104: "questions/other_MikeDeath/",
        105: "questions/other_HankDeath/",
        106: "questions/other_GusDeath/",
        107: "None",
        108: "questions/other_walter_transformation/",
        109: "questions/char_TucoSalamanca/",
        110: "questions/char_GusFring/",
        111: "None",
        112: "None",
        113: "None",
        114: "questions/show_BreakingBad/",
        115: "None",
        116: "None",
        117: "questions/char_LaloSalamanca/",
        118: "questions/char_Nacho/",
        119: "questions/char_Hank/",
        120: "questions/char_WalterWhite/",
        121: "questions/char_Jesse/",
        122: "questions/char_SaulGoodman/",
        123: "questions/char_MikeE/",
        124: "questions/char_GusFring/",
        125: "questions/movie_ElCamino/",
        126: "questions/char_Skyler/",
        127: "questions/char_KimWexler/",
        128: "questions/char_Skyler",
        129: "None",
        130: "questions/show_BreakingBad/",
        131: "questions/char_HectorSalamanca/",
        132: "questions/char_MikeE/",
        133: "questions/char_Jesse/",
        134: "None",
        135: "questions/char_JesseMeetsKim/",
        136: "questions/char_WaltJr/",
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
        150: "questions/char_DonEladio/",
        151: "None",
        152: "questions/char_TyrusKitt/",
        153: "questions/char_SkinnyPete/",
        154: "questions/char_Badger/",
        155: "questions/char_Combo/",
        156: "questions/char_WaltJr/",
        157: "questions/movie_ElCamino/",
        158: "questions/char_LaloSalamanca/",
        159: "questions/movie_ElCamino/",
        160: "None",
        161: "None",
        162: "questions/char_BillBurr/",
        163: "questions/show_BreakingBad/",
        164: "questions/other_BCS_Ending/",
        165: "questions/other_JaneDeath/",
        166: "questions/other_ToddKillsKid/",
        167: "questions/other_Fly/",
        168: "None",
        169: "questions/other_PoisonBrock/",
        170: "questions/char_Ed/",
        171: "questions/show_BreakingBad/",
        172: "None",
        173: "None",
        174: "None",
        175: "None",
        176: "None",
        177: "questions/other_LosPollosHermanos/",
        178: "None",
        179: "None",
        180: "None",
        181: "None",
        182: "None",
        183: "questions/char_Skyler/",
        184: "None",
        185: "None",
        186: "None",
        187: "None",
        188: "None",
        189: "None",
        190: "None",
        191: "questions/show_BreakingBad/",
        192: "questions/char_WalterWhite/",
        193: "None",
        194: "questions/char_GusFring",
        195: "questions/char_KimWexler/",
        196: "None",
        197: "questions/char_GusFring/",
        198: "questions/char_MikeE/",
        199: "None",
        200: "None",
        201: "questions/char_Hank/",
        202: "questions/char_SaulGoodman/",
        203: "None",
        204: "questions/char_Hank/",
        205: "questions/char_Hank/",
        206: "questions/other_SwordUnpopularOpinion/",
        207: "None",
        208: "None",
        209: "questions/char_HowardHamlin/",
        210: "None",
        211: "questions/char_LaloSalamanca/",
        212: "None",
        213: "None",
        214: "questions/char_ChuckMcGill/",
        215: "questions/char_GusFring/",
        216: "questions/char_Hank/",
        217: "None",
        218: "questions/char_Jesse/",
        219: "None",
        220: "questions/char_LaloSalamanca/",
        221: "questions/char_MarieSchrader/",
        222: "questions/char_MikeE/",
        223: "questions/char_Nacho/",
        224: "questions/char_SaulGoodman/",
        225: "questions/char_Skyler/",
        226: "questions/char_Ted/",
        227: "questions/char_ToddAlquist/",
        228: "questions/other_LosPollosHermanos/",
        229: "None",
        230: "None",
        231: "None",
        232: "None",
        233: "None",
        234: "None",
        235: "None",
        236: "None",
        237: "None",
        238: "None",
        239: "None",
        240: "None",
        241: "questions/char_SkinnyPete/",
        242: "None",
        243: "questions/char_Combo/",
        244: "None",
        245: "None",
        246: "None",
        247: "None",
        248: "None",
        249: "None",
        250: "None",
        251: "questions/char_Gale/",
        252: "None",
        253: "None",
        254: "None",
        255: "questions/char_HectorSalamanca/",
        256: "None",
        257: "None",
        258: "None",
        259: "None",
        260: "None",
        261: "None",
        262: "questions/char_Krazy8/",
        263: "questions/char_StevenGomez/",
        264: "questions/show_BreakingBad",
        265: "None",
        266: "None",
        267: "None",
        268: "None",
        269: "None",
        270: "None",
        271: "None",
        272: "None",
        273: "None",
        274: "None",
        275: "None",
        276: "None",
        277: "None",
        278: "None",
        279: "None",
        280: "None",
        281: "None",
        282: "None",
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
        if len(question_indices) > 180:
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




