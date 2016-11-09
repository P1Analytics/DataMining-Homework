# encoding=utf-8

import sys
import os.path


# make the code run under a console
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import excercise_4.application.download_recipes as download_recipes
import excercise_4.application.preprocess_recipes as preprocess_recipes
import excercise_4.application.create_inverted_index as create_inverted_index
import excercise_4.application.query_engine as query_engine
import excercise_4.data.data_manager as data_manager
import excercise_4.util.util as util

global recipes_dic
global index
global index_ing
global index_met
global index_tit

def on_start_up():
    global recipes_dic
    global index
    global index_ing
    global index_met
    global index_tit
    print "******************************"
    print "Starting up the application: Reading data from the disk\n"
    res, recipes_dic = data_manager.read()
    if res==0:
        res, index = data_manager.read_inverted_index(recipes_dic)
        res, index_ing = data_manager.read_inverted_index(recipes_dic, "index_ingredients")
        res, index_met = data_manager.read_inverted_index(recipes_dic, "index_method")
        res, index_tit = data_manager.read_inverted_index(recipes_dic, "index_title")
    print "\nStart up copleted!!"
    print "******************************\n\n\n"

def main():
    global recipes_dic
    global index

    on_start_up()
    print "Welcome to our recipe engine. Press a menu key to perform the specific job"
    print_menu()
    user_input = raw_input("What's your choice? ")
    while True:
        if user_input == "1":
            recipes_dic = download_recipes.start()

        elif user_input == "2":
            preprocess_recipes.start(recipes_dic)

        elif user_input == "3":
            create_inverted_index.start(recipes_dic)

        elif user_input == "4":
            user_input = raw_input("What's your query? ")
            result_query = index.look_for(user_input, 10)
            util.print_query_result(result_query, index)
        elif user_input == "5":
            query = raw_input("What's your query? ")
            res = -1
            while res!=0:
                w_ing = raw_input("What's the weight for the ingredient? ")
                w_met = raw_input("What's the weight for the method? ")
                w_tit = raw_input("What's the weight for the title? ")

                res, result_query = query_engine.look_for(query, index_ing, index_met, index_tit, w_ing, w_met, w_tit)
                if res == -1:
                    print "Some of your weights is not correct... "

            util.print_weighted_query_result(result_query, recipes_dic)
        elif user_input == "exit":
            break
        else:
            user_input = raw_input("You can tape 1, 2, 3, 4, 5 or exit: what's your choice? ")

        print "\n\nPress a menu key to perform the specific job"
        print_menu()
        user_input = raw_input("What's your choice? ")


def print_menu():
    print "\t1) Downlaod recipes"
    print "\t2) Preprocess recipes"
    print "\t3) Create the inverted index"
    print "\t4) Query the index"
    print "\t5) Weighted Query"
    print "\texit to close the application"


def doMyTest():
    res, recipes_dic = data_manager.read()

    res, index = data_manager.read_inverted_index(recipes_dic)

    '''
    print "ingredients"
    res = ing.look_for("cheese mushroom pizza", 0.7, 1000)
    h = {}
    for t in res:
        h[ing.recipes[t[0]].link] = float(t[1])
    print "method"
    res = met.look_for("cheese mushroom pizza", 0.1, 1000)
    for t in res:
        try:
            h[met.recipes[t[0]].link] = h[met.recipes[t[0]].link] + (float(t[1]))
        except Exception:
            h[met.recipes[t[0]].link] = float(t[1])
    print "title"
    res = tit.look_for("cheese mushroom pizza", 0.2, 1000)
    for t in res:
        try:
            h[tit.recipes[t[0]].link] = h[tit.recipes[t[0]].link] + float(t[1])
        except Exception:
            h[tit.recipes[t[0]].link] = float(t[1])

    sorted_x = sorted(h.items(), key=operator.itemgetter(1), reverse=True)[:10]
    i=0
    for p in sorted_x:
        i = i + 1
        ind = str(i)
        if i < 10:
            ind = " " + str(i)
        print ind + ")", p[1], recipes_dic[p[0]].title.ljust(69+18), recipes_dic[p[0]].link
'''
    i=0
    for rec, r in recipes_dic.iteritems():
        print rec
        for t in index.look_for(r.__str__()):
            i = i + 1
            ind = str(i)
            if i < 10:
                ind = " " + str(i)

            print ind + ")", t[1], index.recipes[t[0]].title.ljust(69 + 17), index.recipes[t[0]].link
        break

    i = 0
    for t in index.and_query("mushroom cheese"):
        i = i + 1
        ind = str(i)
        if i<10:
            ind = " "+str(i)

        print ind + ")", t[1], index.recipes[t[0]].title.ljust(69+17 ), index.recipes[t[0]].link


    #for t in index.look_for(util.decode(index.recipes[0].__str__()),2):
    #    print index.recipes[0].linkq
    #    print t[1], index.recipes[t[0]].link

def fill(str):
    return str

if __name__ == "__main__":
    #doMyTest()
    main()