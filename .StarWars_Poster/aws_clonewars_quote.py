import random
import tweepy
import os

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)


def postCWQuote(event, context):
    quotes = {
        1: 'Great leaders inspire greatness in others. -The Clone Wars s1e1',
        2: 'Belief is not a matter of choice, but of conviction. -The Clone Wars s1e2',
        3: 'Easy is the path to wisdom for those not blinded by ego. -The Clone Wars s1e3',
        4: 'A plan is only as good as those who see it through. -The Clone Wars s1e4',
        5: 'The best confidence builder is experience. -The Clone Wars s1e5',
        6: 'Trust in your friends, and they’ll have reason to trust in you. -The Clone Wars s1e6',
        7: 'You hold onto friends by keeping your heart a little softer than your head. -The Clone Wars s1e7',
        8: 'Heroes are made by the times. -The Clone Wars s1e8',
        9: 'Ignore your instincts at your peril. -The Clone Wars s1e9',
        10: 'Most powerful is he who controls his own power. -The Clone Wars s1e10',
        11: 'The winding path to peace is always a worthy one, regardless of how many turns it takes. -The Clone Wars s1e11',
        12: 'Fail with honor rather than succeed by fraud. -The Clone Wars s1e12',
        13: 'Greed and fear of loss are the roots that lead to the tree of evil. -The Clone Wars s1e13',
        14: 'When surrounded by war, one must eventually choose a side. -The Clone Wars s1e14',
        15: 'Arrogance diminishes wisdom. -The Clone Wars s1e15',
        16: 'Truth enlightens the mind, but won’t always bring happiness to your heart. -The Clone Wars s1e16',
        17: 'Fear is a disease; hope is its only cure. -The Clone Wars s1e17',
        18: 'A single chance is a galaxy of hope. -The Clone Wars s1e18',
        19: 'It is a rough road that leads to the heights of greatness. -The Clone Wars s1e19',
        20: 'The costs of war can never be truly accounted for. -The Clone Wars s1e20',
        21: 'Compromise is a virtue to be cultivated, not a weakness to be despised. -The Clone Wars s1e21',
        22: 'A secret shared is a trust formed. -The Clone Wars s1e22',
        23: 'A lesson learned is a lesson earned. -The Clone Wars s2e1',
        24: 'Overconfidence is the most dangerous form of carelessness. -The Clone Wars s2e2',
        25: 'The first step to correcting a mistake is patience. -The Clone Wars s2e3',
        26: 'A true heart should never be doubted. -The Clone Wars s2e4',
        27: 'No gift is more precious than trust. -The Clone Wars s2e6',
        28: 'Sometimes, accepting help is harder than offering it. -The Clone Wars s2e7',
        29: 'Attachment is not compassion. -The Clone Wars s2e8',
        30: 'For everything you gain, you lose something else. -The Clone Wars s2e9',
        31: 'It is the quest for honor that makes one honorable. -The Clone Wars s2e10',
        32: 'Easy isn’t always simple. -The Clone Wars s2e11',
        33: 'If you ignore the past, you jeopardize the future. -The Clone Wars s2e12',
        34: 'Fear not for the future, weep not for the past. -The Clone Wars s2e13',
        35: 'In war, truth is the first casualty. -The Clone Wars s2e14',
        36: 'Searching for the truth is easy. Accepting the truth is hard. -The Clone Wars s2e15',
        37: 'A wise leader knows when to follow. -The Clone Wars s2e16',
        38: 'Courage makes heroes, but trust builds friendships. -The Clone Wars s2e17',
        39: 'Choose what is right, not what is easy. -The Clone Wars s2e18',
        40: 'The most dangerous beast is the beast within. -The Clone Wars s2e19',
        41: 'Who my father was matters less than my memory of him. -The Clone Wars s2e20',
        42: 'Adversity is a friendship’s truest test. -The Clone Wars s2e21',
        43: 'Revenge is a confession of pain. -The Clone Wars s2e22',
        44: 'Brothers in arms are brothers for life. -The Clone Wars s3e1',
        45: 'Fighting a war tests a soldier’s skills, defending his home tests a soldier’s heart. -The Clone Wars s3e2',
        46: 'Where there’s a will, there’s a way. -The Clone Wars s3e3',
        47: 'Sphere of Influence: A child stolen is a hope lost. -The Clone Wars s3e4',
        48: 'The challenge of hope is to overcome corruption. -The Clone Wars s3e5',
        49: 'Those who enforce the law must obey the law. -The Clone Wars s3e6',
        50: 'The future has many paths - choose wisely. -The Clone Wars s3e7',
        51: 'A failure in planning is a plan for failure. -The Clone Wars s3e8',
        52: 'Love comes in all shapes and sizes. -The Clone Wars s3e9',
        53: 'Fear is a great motivator. -The Clone Wars s3e10',
        54: 'Truth can strike down the spectre of fear. -The Clone Wars s3e11',
        55: 'The swiftest path to destruction is through vengeance. -The Clone Wars s3e12',
        56: 'Evil is not born, it is taught. -The Clone Wars s3e13',
        57: 'The path to evil may bring great power, but not loyalty. -The Clone Wars s3e14',
        58: 'Balance is found in the one who faces his guilt. -The Clone Wars s3e15',
        59: 'He who surrenders hope, surrenders life. -The Clone Wars s3e16',
        60: 'Who seeks to control fate shall never find peace. -The Clone Wars s3e17',
        61: 'Adaptation is the key to survival. -The Clone Wars s3e18',
        62: 'Anything that can go wrong will. -The Clone Wars s3e19',
        63: 'Without honor, victory is hollow. -The Clone Wars s3e20',
        64: 'Without humility, courage is a dangerous game. -The Clone Wars s3e21',
        65: 'A great student is what the teacher hopes to be. -The Clone Wars s3e22',
        66: 'When destiny calls, the chosen have no choice. -The Clone Wars s4e1',
        67: 'Only through fire is a strong sword forged. -The Clone Wars s4e2',
        68: 'Crowns are inherited, kingdoms are earned. -The Clone Wars s4e3',
        69: 'Who a person truly is cannot be seen with the eye. -The Clone Wars s4e4',
        70: 'Understanding is honoring the truth beneath the surface. -The Clone Wars s4e5',
        71: 'Who’s the more foolish, the fool or the fool who follows him? -The Clone Wars s4e6',
        72: 'The first step towards loyalty is trust. -The Clone Wars s4e7',
        73: 'The path of ignorance is guided by fear. -The Clone Wars s4e8',
        74: 'The wise man leads, the strong man follows. -The Clone Wars s4e9',
        75: 'Our actions define our legacy. -The Clone Wars s4e10',
        76: 'Where we are going always reflects where we came from. -The Clone Wars s4e11',
        77: 'Those who enslave others, inevitably become slaves themselves. -The Clone Wars s4e12',
        78: 'Great hope can come from small sacrifices. -The Clone Wars s4e13',
        79: 'Friendship shows us who we really are. -The Clone Wars s4e14',
        80: 'All warfare is based on deception. -The Clone Wars s4e15',
        81: 'Keep your friends close, but keep your enemies closer. -The Clone Wars s4e16',
        82: 'The strong survive, the noble overcome. -The Clone Wars s4e17',
        83: 'Trust is the greatest of gifts, but it must be earned. -The Clone Wars s4e18',
        84: 'One must let go of the past to hold on to the future. -The Clone Wars s4e19',
        85: 'Who we are never changes, who we think we are does. -The Clone Wars s4e20',
        86: 'A fallen enemy may rise again, but the reconciled one is truly vanquished. -The Clone Wars s4e21',
        87: 'The enemy of my enemy is my friend. -The Clone Wars s4e22',
        88: 'Strength of character can defeat strength in numbers. -The Clone Wars s5e1',
        89: 'Fear is a malleable weapon. -The Clone Wars s5e2',
        90: 'To seek something is to believe in its possibility. -The Clone Wars s5e3',
        91: 'Struggles often begin and end with the truth. -The Clone Wars s5e4',
        92: 'He who faces himself, finds himself. -The Clone Wars s5e6',
        93: 'The young are often underestimated. -The Clone Wars s5e7',
        94: 'When we rescue others, we rescue ourselves. -The Clone Wars s5e8',
        95: 'Choose your enemies wisely, as they may be your last hope. -The Clone Wars s5e9',
        96: 'Humility is the only defense against humiliation. -The Clone Wars s5e10',
        97: 'When all seems hopeless, a true hero gives hope. -The Clone Wars s5e11',
        98: 'A soldier’s most powerful weapon is courage. -The Clone Wars s5e12',
        99: 'You must trust in others or success is impossible. -The Clone Wars s5e13',
        100: 'One vision can have many interpretations. -The Clone Wars s5e14',
        101: 'Alliances can stall true intentions. -The Clone Wars s5e15',
        102: 'Morality separates heroes from villains. -The Clone Wars s5e16',
        103: 'Sometimes even the smallest doubt can shake the greatest belief. -The Clone Wars s5e17',
        104: 'Courage begins by trusting oneself. -The Clone Wars s5e18',
        105: 'Never become desperate enough to trust the untrustworthy. -The Clone Wars s5e19',
        106: 'Never give up hope, no matter how dark things seem. -The Clone Wars s5e20',
        107: 'The truth about yourself is always the hardest to accept. -The Clone Wars s6e1',
        108: 'The wise benefit from a second opinion. -The Clone Wars s6e2',
        109: 'When in doubt, go to the source. -The Clone Wars s6e3',
        110: 'The popular belief isn’t always the correct one. -The Clone Wars s6e4',
        111: 'To love, is to trust. To trust is to believe. -The Clone Wars s6e5',
        112: 'Jealousy is the path to chaos. -The Clone Wars s6e6',
        113: 'Deceit is the weapon of greed. -The Clone Wars s6e7',
        114: 'Without darkness there cannot be light. -The Clone Wars s6e8',
        115: 'Wisdom is born in fools as well as wise men. -The Clone Wars s6e9',
        116: 'What is lost is often found. -The Clone Wars s6e10',
        117: 'Madness can sometimes be the path to truth. -The Clone Wars s6e11',
        118: 'Death is just the beginning. -The Clone Wars s6e12',
        119: 'Facing all that you fear will free you from yourself. -The Clone Wars s6e13',
        120: 'Embrace others for their differences, for that makes you whole. -The Clone Wars s7e1',
        121: 'The search for truth begins with belief. -The Clone Wars s7e2',
        122: 'Survival is one step on the path to living. -The Clone Wars s7e3',
        123: 'Trust placed in another is trust earned. -The Clone Wars s7e4',
        124: 'If there is no path before you, create your own. -The Clone Wars s7e5',
        125: 'Mistakes are valuable lessons often learned too late. -The Clone Wars s7e6',
        126: 'Who you were does not have to define who you are. -The Clone Wars s7e7',
        127: 'You can change who you are, but you cannot run from yourself. -The Clone Wars s7e8',
        128: 'Believe in yourself or no one else will. -The Clone Wars s2e5',
        129: 'Disobedience is a demand for change. -The Clone Wars s5e5'
    }

    tweet_text = quotes[random.randint(1, len(quotes))] + " "

    tagsString = f""
    ran = random.random()
    if ran < 0.04:
        tweet_text += " #swtwt"
    elif ran < 0.05:
        tweet_text += " #StarWars"
    elif ran < 0.06:
        tweet_text += " #TheCloneWars"
    elif ran < 0.07:
        tweet_text += " #StarWarsQuotes"

    client.create_tweet(text=tweet_text)
