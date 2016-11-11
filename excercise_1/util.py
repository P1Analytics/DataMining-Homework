import math

seeds = ['h','c','d','s']
number = [x for x in range(1, 14)]
cards = [(n, seed) for n in number
         for seed in seeds]

def getFirstXCards(x, res, notAllowedCards=[], seed = ""):
    if x is 0:
        res.append([x for x in notAllowedCards])
        return
    for card in cards:
        if card not in notAllowedCards:
            if seed == "" or card[1]==seed:
                notAllowedCards.append(card)
                getFirstXCards(x - 1, res, notAllowedCards, seed)
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

def is_full_house(cards):
    rank1 = -1
    rank2 = -1
    n_rank1 = 0
    n_rank2 = 0
    for card in cards:
        if rank1==-1:
            rank1 = card[0]
            n_rank1 += 1
        elif card[0] == rank1:
            n_rank1 += 1
            continue
        elif rank2==-1:
            rank2 = card[0]
            n_rank2 += 1
        elif rank2 != card[0]:
            return False
        else:
            n_rank2+=1

    return n_rank1==2 and n_rank2==3 or n_rank1==3 and n_rank2==2