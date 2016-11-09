import heapq
import operator

def look_for(query, index_ing, index_met, index_tit, w_ing, w_met, w_tit):
    '''

    :param query:
    :param index_ing:
    :param index_met:
    :param index_tit:
    :param w_ing:
    :param w_met:
    :param w_tit:
    :return: res, list --> if res = -1 something goes wronk
    '''
    print "\t weighted query > looking for ["+query+"]"
    print "\t\tIngredient weight:  "+str(w_ing)
    print "\t\tMethod weight:     " + str(w_met)
    print "\t\tTitle weight:      " + str(w_tit)

    try:
        w_ing = float(w_ing)
        w_met = float(w_met)
        w_tit = float(w_tit)
    except ValueError:
        return -1, []

    res = index_ing.look_for(query, w_ing, 1000)
    h = {}
    for t in res:
        h[index_ing.recipes[t[0]].link] = float(t[1])

    res = index_met.look_for(query, w_met, 1000)
    for t in res:
        try:
            h[index_met.recipes[t[0]].link] = h[index_met.recipes[t[0]].link] + (float(t[1]))
        except Exception:
            h[index_met.recipes[t[0]].link] = float(t[1])

    res = index_tit.look_for(query, w_tit, 1000)
    for t in res:
        try:
            h[index_tit.recipes[t[0]].link] = h[index_tit.recipes[t[0]].link] + float(t[1])
        except Exception:
            h[index_tit.recipes[t[0]].link] = float(t[1])

    return 0, sorted(h.items(), key=operator.itemgetter(1), reverse=True)[:10]