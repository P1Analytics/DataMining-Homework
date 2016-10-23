seeds = ['h','c','d','s']
number = [x for x in range(1, 14)]
cards = [(n, seed) for n in number
         for seed in seeds]

# print len(cards)
# print cards

res = []

print "/*** TEST FIRST CASE ***/"

def getFirstXCards(x, res, notAllowedCards=[]):
    if x is 0:
        res.append([x for x in notAllowedCards])
        return
    for card in cards:
        if card not in notAllowedCards:
            notAllowedCards.append(card)
            getFirstXCards(x - 1, res, notAllowedCards)
            notAllowedCards.remove(card)
        else:
            continue

def getFirstXCards_mthread(i, j, number_perm):
    notAllowedCards = []
    for x in range(i,j):
        card = cards[x]
        notAllowedCards.append(card)
        getFirstXCards(number_perm-1, res, notAllowedCards)
        notAllowedCards.remove(card)

def a__at_least_one_ace_over_three_cards():
    getFirstXCards(3, res)
    cnt = 0
    for r in res:
        for card in r:
            if (card[0] is 1):
                cnt += 1
                break
    return float(cnt) / float(len(res))

def b__exactly_one_ace_over_three_cards():
    perm_5 = []
    for r in res:
        getFirstXCards(2, perm_5, r)
        for p in perm_5:
            r.append(p)
    print "** b__exactly_one_ace_over_three_cards --> now computre result **"
    cnt = 0;
    for r in res:
        number_of_aces = 0
        for card in r:
            if (card[0] is 1):
                number_of_aces += 1
        if number_of_aces is 1:
            cnt += 1

    return float(cnt) / float(len(res))

#print "Probability to have at least one ace over three cards is", a__at_least_one_ace_over_three_cards()
#print "Probability to have exactly one ace over five cards is", b__exactly_one_ace_over_three_cards()
import thread
import time
def getPercentTime(n):
    f = 0
    while f is not 1.0:
        den = 1
        for i in range(52-n+1, 53):
            den = den * i

        f = float(len(res))/float(den)
        print "% finish: ",f
        time.sleep(5)


import threading
try:
    num_perm = 5;
    t1 = threading.Thread(target=getFirstXCards_mthread, args=(0, 13, num_perm))
    t2 = threading.Thread(target=getFirstXCards_mthread, args=(13, 26, num_perm))
    t3 = threading.Thread(target=getFirstXCards_mthread, args=(26, 39, num_perm))
    t4 = threading.Thread(target=getFirstXCards_mthread, args=(39, 52, num_perm))
    t5 = threading.Thread(target=getPercentTime, args=(num_perm,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print len(res)
    print 52*51*50*49*48

    # print "* Creating threads *"
    # t1 = my_thread(0, 13, 2)
    # t2 = my_thread(13, 26, 2)
    # t3 = my_thread(26, 39, 2)
    # t4 = my_thread(39, 52, 2)
    #
    # print "* Starting threads *"
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    #
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    #
    # print "* every thread is finished *"
except:
    print "Error: unable to start thread"