import util

def a__at_least_one_ace_over_three_cards():
    res = []
    util.getFirstXCards(3, res)
    cnt = 0
    for r in res:
        for card in r:
            if (card[0] is 1):
                cnt += 1
                break
    return float(cnt) / float(len(res))

def c__tris_over_three_cards():
    res = []
    util.getFirstXCards(3, res)
    cnt = 0
    for r in res:
        test = True
        curr_value = r[0][0]
        for i in range(1, len(r)):
            if (r[i][0] is not curr_value):
                test = False
                break
        if test:
            cnt+=1
    return float(cnt) / float(len(res))

def b__exactly_one_ace_over_five_cards(naive=0):
    if naive == 1:
        res = []
        util.getFirstXCards(5, res)
        cnt = 0;
        for r in res:
            number_of_aces = 0
            for card in r:
                if (card[0] is 1):
                    number_of_aces += 1
            if number_of_aces is 1:
                cnt += 1
        return float(cnt) / float(len(res))
    elif naive == 0.5:
        ''' semi naive --> just count in a smart way '''
        ace = util.getAces()[0]
        res = []
        util.getFirstXCards(4, res, [ace])
        cnt = 0;
        for r in res:
            number_of_aces = 0
            for card in r:
                if (card[0] == 1):
                    number_of_aces += 1
            if number_of_aces == 1:
                cnt += 20   # because: 4 aces times 5 different position of the ace in the current permutation
        return float(cnt) / float(util.get_combination(52,5)*util.fact(5))
    else:
        ''' #aces . how we can combine the other 4 cards (without aces)
                . all the possible permutation of this 5 cards
                . the permutation of the reamins card '''
        return float((4 * util.get_combination(48, 4) * util.fact(5) * util.fact(47)))/float(util.fact(52))


def d__flush_over_five_cards():
    # compute the size of the permutation when the first five card are diamond
    # number of permutation with 5 generic cards
    res = []
    util.getFirstXCards(5, res, [], "d")
    return float(len(res))/float(util.get_combination(52,5)*util.fact(5))

def e__full_house_over_five_cards(naive=0):
    if naive == 1:
        res = []
        util.getFirstXCards(5, res)
        cnt = 0;
        for r in res:
            if util.is_full_house(r):
                cnt+=1
        return float(cnt) / float(len(res))
    if naive == 0.5:
        res = []
        util.getFirstXCards(5, res)
        cnt = 0;
        for r in res:
            if util.is_full_house(r):
                cnt+=1
        return float(cnt) / float(len(res))



print "Probability to have at least one ace over three cards is", a__at_least_one_ace_over_three_cards()
print "Probability to have exactly one ace over five cards is", b__exactly_one_ace_over_five_cards(0.5)
#print "Probability to have exactly one ace over five cards is", b__exactly_one_ace_over_five_cards()
print "Probability to have a tris over three cards is", c__tris_over_three_cards()
print "Probability to have five diamond cards within the first five cards", d__flush_over_five_cards()
print "Probability to have a full house within the first five cards", e__full_house_over_five_cards(1)


