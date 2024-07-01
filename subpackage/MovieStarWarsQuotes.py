import random

def getCloneWarsQuote(self):
    quotes = {
        1: 'Great leaders inspire greatness in others. -The Clone Wars s1e1',

    }

    quote = quotes[random.randint(1, len(quotes))]
    return quote
