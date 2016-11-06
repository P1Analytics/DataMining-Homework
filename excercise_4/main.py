# encoding=utf-8

import sys
import os.path
import heapq
import operator

# make the code run under a console
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import excercise_4.application.download_recipes as download_recipes
import excercise_4.application.preprocess_recipes as preprocess_recipes
import excercise_4.application.create_inverted_index as create_inverted_index
import excercise_4.data.data_manager as data_manager
import excercise_4.util.util as util

global recipes_dic
global index

def on_start_up():
    global recipes_dic
    global index
    print "******************************"
    print "Starting up the application...\n"
    res, recipes_dic = data_manager.read()
    res, index = data_manager.read_inverted_index(recipes_dic)
    print "\nStart up copleted!!"
    print "******************************\n\n\n"

def main():
    global recipes_dic
    global index

    on_start_up()
    print "Welcome to our recipe engine. Press a menu key to perform the specific job"
    print "\t1) Downlaod recipes"
    print "\t2) Preprocess recipes"
    print "\t3) Create the inverted index"
    print "\t4) Query the index"
    print "\teixt() to close the application"
    user_input = raw_input("What's yout choice? ")
    while True:
        if user_input == "1":
            recipes_dic = download_recipes.start()
            break
        elif user_input == "2":
            preprocess_recipes.start(recipes_dic)
            break
        elif user_input == "3":
            create_inverted_index.start(recipes_dic)
            break
        elif user_input == "exit()":
            break
        else:
            user_input = raw_input("You can tape either 1, 2, 3, or exit(): what's your choice? ")

def doMyTest():
    res, recipes_dic = data_manager.read()
    #res, ing = data_manager.read_inverted_index(recipes_dic, "index_ingredients")
    #res, met = data_manager.read_inverted_index(recipes_dic, "index_method")
    #res, tit = data_manager.read_inverted_index(recipes_dic, "index_title")

    res, index = data_manager.read_inverted_index(recipes_dic)

    '''
    print "ingredients"
    res = ing.look_for("cheese mushroom pizza", 1000)
    h = {}
    for t in res:
        h[ing.recipes[t[0]].link] = 0.2 * float(t[1])
    print "method"
    res = met.look_for("cheese mushroom pizza", 1000)
    for t in res:
        try:
            h[met.recipes[t[0]].link] = h[met.recipes[t[0]].link] + 0.4 * (float(t[1]))
        except Exception:
            h[met.recipes[t[0]].link] = 0.4*float(t[1])
    print "title"
    res = tit.look_for("cheese mushroom pizza", 1000)
    for t in res:
        try:
            h[tit.recipes[t[0]].link] = h[tit.recipes[t[0]].link] + 0.4 * float(t[1])
        except Exception:
            h[tit.recipes[t[0]].link] = 0.4*float(t[1])

    sorted_x = sorted(h.items(), key=operator.itemgetter(1), reverse=True)[:10]
    for p in sorted_x:
        print p
    '''

    for t in index.look_for("-1", 10):
        print t[1], index.recipes[t[0]], index.recipes[t[0]].link

    #for t in index.look_for(util.decode(index.recipes[0].__str__()),2):
    #    print index.recipes[0].linkq
    #    print t[1], index.recipes[t[0]].link


if __name__ == "__main__":
    doMyTest()
    #main()