import math

seeds = ['h','c','d','s']
number = [x for x in range(1, 14)]
cards = [(n, seed) for n in number
         for seed in seeds]

def getFirstXCards(x, res, notAllowedCards=[]):
    if x is 0:
        res.append([x for x in notAllowedCards])
        return
    for card in cards:
        if card not in notAllowedCards:
            notAllowedCards.append(card)
            getFirstXCards(x - 1, res, notAllowedCards)
            notAllowedCards.remove(card)

def getAces():
    res = []
    for card in cards:
        if card[0] is 1:
            res.append(card)
    return res

def get_combination(a, b):
    if a < b:
        return 0
    return math.factorial(a)/(math.factorial(b)*math.factorial(a-b))

def fact(n):
    if n <= 0:
        return 0
    return math.factorial(n)