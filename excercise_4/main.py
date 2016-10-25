# encoding=utf-8

import sys
import os.path

# make the code run under a console
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import excercise_4.application.download_recipes as download_recipes
import excercise_4.application.preprocess_recipes as preprocess_recipes
import excercise_4.data.data_manager as data_manager

def on_start_up():
    recipes_dic = data_manager.read()
    print len(recipes_dic), " reicpes"

def main():
    recipes_dic = on_start_up()
    print "Welcome to our recipe engine. Press a menu key to perform the specific job"
    print "\t1) Downlaod recipes"
    print "\t2) Preprocess recipes"
    print "\teixt() to close the application"
    user_input = raw_input("Make a mess... ")
    while True:
        if user_input == "1":
            recipes_dic = download_recipes.start()
            break
        elif user_input == "2":
            preprocess_recipes.start(**recipes_dic)
            break
        elif user_input == "exit()":
            break
        else:
            user_input = raw_input("You can tape either 1, 2, or exit(): ")

def doMyTest():
    recipes_dic = download_recipes.start()
    preprocess_recipes.start(**recipes_dic)

if __name__ == "__main__":
    doMyTest()
    # main()