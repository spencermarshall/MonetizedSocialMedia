import random
import tweepy

hp_api_key = 'placeholder'
hp_api_key_secret = 'placeholder'
hp_bearer_token = 'placeholder'
hp_access_token = 'placeholder'
hp_access_token_secret = 'placeholder'


client = tweepy.Client(bearer_token = hp_bearer_token,
                                consumer_key = hp_api_key, consumer_secret = hp_api_key_secret,
                                access_token = hp_access_token, access_token_secret = hp_access_token_secret)

def post_hp_quote(event, context):
    hp_quotes = {
        0: "\"You're a wizard, Harry.\" -Hagrid",
        1: "\"It does not do to dwell on dreams and forget to live.\" -Albus Dumbledore",
        2: "\"There is no such thing as magic!\" -Uncle Vernon",
        3: "\"I can't be a wizard. I'm just Harry.\" -Harry Potter",
        4: "\"Wingardium Leviosa!\" -Hermione Granger",
        5: "\"You're saying it wrong. It's LeviOsa, not LeviosA!\" -Hermione Granger",
        6: "\"I think it is clear that we can expect great things from you, Mr. Potter.\" -Ollivander",
        7: "\"There is no good and evil, there is only power, and those too weak to seek it.\" -Professor Quirrell",
        8: "\"I shouldn't have said that. I should not have said that.\" -Hagrid",
        9: "\"After all, to the well-organized mind, death is but the next great adventure.\" -Albus Dumbledore",
        10: "\"It is not our abilities that show what we truly are... it is our choices.\" -Albus Dumbledore",
        11: "\"We never left.\" -James Potter",
        12: "\"The Chamber of Secrets has been opened. Enemies of the heir, beware.\" -Message on the wall",
        13: "\"Fawkes is a phoenix, Harry. They burst into flame when it is time for them to die and are reborn from the ashes.\" -Dumbledore",
        14: "\"Dobby is free!\" -Dobby",
        15: "\"Harry Potter must not go back to Hogwarts.\" -Dobby",
        16: "\"When in doubt, go to the library.\" -Ron Weasley",
        17: "\"Fear of a name only increases fear of the thing itself.\" -Hermione Granger",
        18: "\"You’ll find that help will always be given at Hogwarts to those who ask for it.\" -Albus Dumbledore",
        19: "\"Why spiders? Why couldn’t it be follow the butterflies?\" -Ron Weasley",
        20: "\"I solemnly swear that I am up to no good.\" -Harry Potter",
        21: "\"Happiness can be found even in the darkest of times if one only remembers to turn on the light.\" -Albus Dumbledore",
        22: "\"Mischief managed.\" -Harry Potter",
        23: "\"I did my waiting! Twelve years of it, in Azkaban!\" -Sirius Black",
        24: "\"You foul, loathsome, evil little cockroach!\" -Hermione Granger",
        25: "\"Expelliarmus!\" -Harry Potter"
        26: "\"The ones that love us never really leave us.\" -Sirius Black",
        27: "\"Expecto Patronum!\" -Harry Potter",
        28: "\"Don't let the muggles get you down.\" -Ron Weasley",
        29: "\"You look in excellent health to me, Potter, so you will excuse me if I don’t let you off homework today.\" -Professor Snape",
        30: "\"People change in the maze. Oh, find the cup if you can. But be very wary; you could just lose yourselves along the way.\" -Albus Dumbledore",
        31: "\"If you want to know what a man’s like, take a good look at how he treats his inferiors, not his equals.\" -Sirius Black",
        32: "\"I didn’t put my name in that cup! I don’t want eternal glory!\" -Harry Potter",
        33: "\"Eternal glory. That's what awaits the student who wins the Triwizard Tournament.\" -Albus Dumbledore",
        34: "\"What’s life without a little risk?\" -Sirius Black",
        35: "\"I will not have you in the course of a single evening besmirching that name by behaving like a babbling, bumbling band of baboons!\" -Professor McGonagall",
        36: "\"Harry, people die in this tournament.\" -Hermione Granger",
        37: "\"Dark and difficult times lie ahead. Soon we must all face the choice between what is right and what is easy.\" -Albus Dumbledore",
        38: "\"Bloody hell, Harry. That was not funny.\" -Ron Weasley",
        39: "\"You’re the boy who lived.\" -Mad-Eye Moody",
        40: "\"The Ministry has fallen. Scrimgeour is dead. They are coming.\" -Kingsley Shacklebolt",
        41: "\"The world isn’t split into good people and Death Eaters.\" -Sirius Black",
        42: "\"I killed Sirius Black!\" -Bellatrix Lestrange",
        43: "\"Just because you have the emotional range of a teaspoon doesn’t mean we all have.\" -Hermione Granger",
        44: "\"You're a fool, Harry Potter, and you will lose everything.\" -Lord Voldemort",
        45: "\"We’ve got one thing that Voldemort doesn’t have. Something worth fighting for.\" -Harry Potter",
        46: "\"You’re the weak one. And you’ll never know love, or friendship. And I feel sorry for you.\" -Harry Potter",
        47: "\"You’re a really good teacher, Harry.\" -Luna Lovegood",
        48: "\"Working hard is important, but there is something that matters even more: believing in yourself.\" -Harry Potter",
        49: "\"We’re coming with you, Harry.\" -Hermione Granger",
        50: "\"But I am the Chosen One.\" -Harry Potter",
        51: "\"Once again, I must ask too much of you, Harry.\" -Albus Dumbledore",
        52: "\"It was a mistake for you to come here, Tom.\" -Albus Dumbledore",
        53: "\"You dare use my own spells against me, Potter? Yes, I’m the Half-Blood Prince.\" -Professor Snape",
        54: "\"I never realized how beautiful this place was.\" -Professor Slughorn",
        55: "\"You’ve got a bit of dirt on your nose, by the way. Did you know?\" -Hermione Granger",
        56: "\"I am not worried, Harry. I am with you.\" -Albus Dumbledore",
        57: "\"Severus… please.\" -Albus Dumbledore",
        58: "\"It's over. Time to get back to the real world.\" -Professor Slughorn",
        59: "\"You have no idea what he was like, even then.\" -Professor Slughorn",
        60: "\"Dobby never meant to kill. Dobby only meant to maim, or seriously injure.\" -Dobby",
        61: "\"We’re all going to keep fighting, Harry. You know that?\" -Ginny Weasley",
        62: "\"Here lies Dobby, a free elf.\" -Harry Potter",
        63: "\"Come on, Tom. Let’s finish this the way we started. Together!\" -Harry Potter",
        64: "\"Do not pity the dead, Harry. Pity the living.\" -Albus Dumbledore",
        65: "\"After all this time?\" -Albus Dumbledore",
        66: "\"Harry, you wonderful boy. You brave, brave man.\" -Lily Potter",
        67: "\"The Elder Wand belongs to the wizard who killed its last owner.\" -Harry Potter",
        68: "\"We’re with you, whatever happens.\" -Hermione Granger",
        69: "\"NOT MY DAUGHTER, YOU B*TCH!\" -Molly Weasley",
        70: "\"Does it hurt? Dying?\" -Harry Potter",
        71: "\"Of course it’s happening inside your head, Harry, but why on earth should that mean that it is not real?\" -Albus Dumbledore",
        72: "\"I open at the close.\" -Harry Potter",
        73: "\"Together, we’ll be stronger.\" -Hermione Granger"
    }

    tweet_text = hp_quotes[random.randint(0,len(hp_quotes))]
    tweet_text += " #HarryPotter"
    client.create_tweet(text=tweet_text)
