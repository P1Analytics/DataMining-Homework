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
            print "You can tape 1, 2, 3, 4, 5 or exit!!!"

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
    pass

if __name__ == "__main__":
    #doMyTest()
    main()