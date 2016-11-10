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
global index_dic        # key: name, value: inverted index

def on_start_up():
    global recipes_dic
    global index
    global index_dic

    index_dic = {}

    print "******************************"
    print "Starting up the application: Reading data from the disk\n"
    res, recipes_dic = data_manager.read()
    if res==0:

        res, index = data_manager.read_inverted_index(recipes_dic)
        index_dic[index.name] = index

        for index_name in os.listdir(data_manager.data_path):
            if index_name.endswith(".tsv") and index_name != "error_pages_data.tsv" and index_name != "recipe_file_data.tsv":
                current_index_name = index_name.split("__")[0]
                if not current_index_name in index_dic.keys():
                    res, temp_index = data_manager.read_inverted_index(recipes_dic, current_index_name)
                    index_dic[current_index_name] = temp_index
            else:
                continue
    print "\nStart up copleted!!"
    print "******************************\n\n\n"

def main():
    global recipes_dic
    global index
    global index_dic

    on_start_up()

    print "Welcome to our recipe engine. Press a menu key to perform the specific job"
    print_menu()
    user_input = raw_input("What's your choice? ")

    while True:
        if user_input == "1":
            recipes_dic = download_recipes.start()

        elif user_input == "2":
            if len(recipes_dic) == 0:
                print "\tWARNING: there is no recipe! Must execute either job 1 (to crawl the web site and download recipes) or 7 (to restore recipes previouslty downloaded) first"
            else:
                preprocess_recipes.start(recipes_dic)

        elif user_input == "3":
            if len(recipes_dic) == 0:
                print "\tWARNING: there is no recipe! Must execute either job 1 (to crawl the web site and download recipes) or 7 (to restore recipes previouslty downloaded) first"
            else:
                # choose a unique name
                print "\tChoose a name different by the those available"
                print_available_indexes()
                custom_index_name = raw_input("What's your index name? ")

                # choose feature that must be processed
                print "\tChoose one or more features"
                custom_features = choose_features()

                # after creating the index, store it in the global dictionary
                res, temp_index = create_inverted_index.start(recipes_dic, False, custom_index_name, True, custom_features)
                if res == 0:
                    index_dic[temp_index.name] = temp_index
                else:
                    print "\t*Error during creating the index..*"

        elif user_input == "4":
            if len(index_dic) == 0:
                print "\tWARNING: there is no index! Must execute either job 3 (to create a customized index) or 7 (to restore default indexes) first"
            else:
                user_input = raw_input("What's your query? ")
                index_dic_name = print_available_indexes()
                chosen_index = choose_index(index_dic_name)

                index_to_query = index_dic[index_dic_name[int(chosen_index)]]
                result_query = index_to_query.look_for(user_input, 10)
                util.print_query_result(result_query, index_to_query)
        elif user_input == "5":
            if ("index_method" not in index_dic.keys()) or ("index_title" not in index_dic.keys()) or ("index_ingredients" not in index_dic.keys()):
                print "WARNING: not possible executing weighted query --> need to restore! (job 7) "
            else:
                query = raw_input("What's your query? ")
                res = -1
                while res!=0:
                    w_ing = raw_input("What's the weight for the ingredient? ")
                    w_met = raw_input("What's the weight for the method? ")
                    w_tit = raw_input("What's the weight for the title? ")

                    res, result_query = query_engine.look_for(query, index_dic["index_ingredients"], index_dic["index_method"], index_dic["index_title"], w_ing, w_met, w_tit)
                    if res == -1:
                        print "Some of your weights is not correct... "

                util.print_weighted_query_result(result_query, recipes_dic)
        elif user_input == "6":
            # AND Query
            if len(index_dic) == 0:
                print "\tWARNING: there is no index! Must execute either job 3 (to create a customized index) or 7 (to restore default indexes) first"
            else:
                user_input = raw_input("The recipe returned will contain every term of your query. What's your query? ")
                index_dic_name = print_available_indexes()
                chosen_index = choose_index(index_dic_name)
                index_to_query = index_dic[index_dic_name[int(chosen_index)]]
                result_query = index_to_query.and_query(user_input, 10)
                util.print_query_result(result_query, index_to_query)
        elif user_input == "7":
            data_manager.restore_backup()
            res, recipes_dic = data_manager.read()
            if res == 0:
                res, index = data_manager.read_inverted_index(recipes_dic)
                index_dic[index.name] = index
                res, index = data_manager.read_inverted_index(recipes_dic, "index_ingredients")
                index_dic[index.name] = index
                res, index = data_manager.read_inverted_index(recipes_dic, "index_method")
                index_dic[index.name] = index
                res, index = data_manager.read_inverted_index(recipes_dic, "index_title")
                index_dic[index.name] = index
        elif user_input == "exit":
            break
        else:
            print "You can tape 1, 2, 3, 4, 5, 6, 7 or exit!!!"

        print "** Operation completed! **"
        print "\n\nPress a menu key to perform the specific job"
        print_menu()
        user_input = raw_input("What's your choice? ")


def choose_index(index_dic_name):
    while True:
        chosen_index = raw_input("What's your index? ")
        try:
            val = int(chosen_index)
            if not (val > 0 and val <= len(index_dic_name)):
                print("\tWARNING: Type an available index id!!!")
                continue
            break
        except ValueError:
            print("\tWARNING: That's not an int!!!")
    return chosen_index


def print_available_indexes():
    print "\tAvailable index:"
    i = 1
    index_dic_name = {}
    for index_name in os.listdir(data_manager.data_path):
        if index_name.endswith(".tsv") and index_name != "error_pages_data.tsv" and index_name != "recipe_file_data.tsv":
            current_index_name = index_name.split("__")[0]
            if not current_index_name in index_dic_name.values():
                print "\t" + str(i) + ") " + current_index_name
                index_dic_name[int(i)] = current_index_name
                i += 1
        else:
            continue
    return index_dic_name


def print_menu():
    print "\t1) Downlaod recipes"
    print "\t2) Preprocess recipes"
    print "\t3) Create the inverted index"
    print "\t4) Query the index"
    print "\t5) Weighted Query"
    print "\t6) AND Query"
    print "\t7) Restore default indexes"
    print "\texit to close the application"

def choose_features():
    std_features = ["title", "link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]
    for i in range(len(std_features)):
        print "\t"+str(i + 1) + ") " + std_features[i]

    error = True
    while error:
        res = []
        chosen_features = raw_input("Type the features index separated by space, and then return. ")
        if chosen_features.lstrip()=="":
            print "\tWARNING: choose at least one feature!"
            continue
        error = False
        for feature in chosen_features.split(" "):
            if feature.lstrip() == "":
                continue
            try:
                val = int(feature)
                if not (val > 0 and val <= len(std_features)):
                    print("\tWARNING: Type an available feature!!!")
                    error = True
                    break
                res.append(std_features[val-1])
            except ValueError:
                print("\tWARNING: some feature ids are not int!!!")
                error = True
                break
    return res

def doMyTest():
    pass


if __name__ == "__main__":
    doMyTest()
    main()