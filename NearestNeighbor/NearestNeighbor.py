# encoding=utf-8

import os
import sys
import shingle
import similarity

from signature_matrix import SignatureMatrix

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def main():
    program_name = "NearestNeighbor.py"

    # set default parameters
    default_parameters = {}

    default_parameters["shingle_size"] = 10
    default_parameters["word_shingle"] = False
    default_parameters["filter_stopword"] = True
    default_parameters["filter_punctuation"] = True
    default_parameters["stemming"] = True
    default_parameters["b"] = 10
    default_parameters["r"] = 10

    # read parameter from console
    input_parameters = sys.argv

    for input_par in input_parameters:
        if program_name in input_par:
            continue
        try:
            in_par_name = str(input_par.split("=")[0][1:])
            in_par_value = str(input_par.split("=")[1])

            if in_par_name in default_parameters.keys():
                if in_par_name == "shingle_size" or in_par_name == "b" or in_par_name == "r":
                    in_par_value = int(in_par_value)
                else:
                    in_par_value = in_par_value=="True"
                default_parameters[in_par_name] = in_par_value
        except IndexError:
            continue

    if len(input_parameters) == 1:
        #print how to run the application
        print "\nTo run the application with different parameter you have to write them in this way(separate them with a space):"
        print "\t-parameter_name=parameter_value"

    print "Using parameters:"
    for k, v in default_parameters.iteritems():
        print "\t-" + str(k) + "=" + str(v)

    similar_recipes = ['http://www.bbc.co.uk/food/recipes/currypuffs_71741',
                   'http://www.bbc.co.uk/food/recipes/currypuffs_71740',
                    'http://www.bbc.co.uk/food/recipes/fish_pie_with_garden_36257',
                    'http://www.bbc.co.uk/food/recipes/classic_fish_pie_with_86482',
                    'http://www.bbc.co.uk/food/recipes/arbroath_smokie_cakes_32036',
                    'http://www.bbc.co.uk/food/recipes/smoked_mackerel_44874',
                    'http://www.bbc.co.uk/food/recipes/quick_chicken_curry_94696',
                    'http://www.bbc.co.uk/food/recipes/chickencurry_82610',
                   'http://www.bbc.co.uk/food/recipes/rosemaryssweetpastry_74773',
                    'http://www.bbc.co.uk/food/recipes/rosemaryssavourypast_74777',
                   'http://www.bbc.co.uk/food/recipes/cheesescones_1287',
                   'http://www.bbc.co.uk/food/recipes/sultanascones_1286',
                   'http://www.bbc.co.uk/food/recipes/gingerbread_men_99096',
                    'http://www.bbc.co.uk/food/recipes/christmas_gingerbread_84244',
                   'http://www.bbc.co.uk/food/recipes/simpledaiquari_85329',
                   'http://www.bbc.co.uk/food/recipes/classicdiaquari_86314',
                   'http://www.bbc.co.uk/food/recipes/spicykoftaburgers_70175',
                   'http://www.bbc.co.uk/food/recipes/gourmetburgers_70174',
                    'http://www.bbc.co.uk/food/recipes/beef_bourguignon_09721',
                       'http://www.bbc.co.uk/food/recipes/beef_bourguignon_with_89401']

    recipes = get_documents()

    '''new = {}
    for k,v in recipes.iteritems():
        if k in similar_recipes:
            new[k]=v
    recipes = new'''
    k = 10
    ''' SHINGLE BY CHAR '''
    '''recipe_shingle_diz =  shingle.get_shingles(recipes, shingle_size=k
                                                  , word_shingle=False
                                                  , filter_stopword=True
                                                  , filter_punctuation=True
                                                  , stemming=True)'''
    recipe_shingle_diz = shingle.get_shingles(recipes, **default_parameters)
    # 2 create the signature matrix
    M = SignatureMatrix(default_parameters["b"]*default_parameters["r"])
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    M.print_signatures()

    # 3 find similarities
    similarity.find(default_parameters["b"], default_parameters["r"], M, recipe_shingle_diz)


    ''' SHINGLE BY TOKEN compute the similarity through word-shingle

    recipe_shingle_diz = shingle.get_shingles(recipes, shingle_size=k
                                                     , word_shingle=True
                                                     , filter_stopword=True
                                                     , filter_punctuation=True
                                                     , stemming=True)
    # 2 create the signature matrix
    M = SignatureMatrix(100)
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    #M.print_signatures()

    # 3 find similarity
    similarity.find(M, recipe_shingle_diz)'''


def get_documents():
    from excercise_4.data import data_manager
    res, diz = data_manager.read(1)

    #diz = {}
    #diz["food/recipes_0"] = "bla bla blaaaablaaaaa senso qualcosa di in food/ recipes telligente, bla bla blaaaablaaaaa qualcosa di intelligente"
    #diz["food/recipes_1"] = "bla bla blaaaablaaaaa senso qualcosa di in food/ recipes telligente, bla bla blaaaablaaaaa qualcosa di intelligente"
    #diz["food/recipes_2"] = "bla bla blaaaablaaaaa senso qualcosa di intelligent food/recipes food/recipes food/recipes e, bla bla blaaa Ok deve avere un senso ablaaaaa qualcosa di intelligente"
    #diz["food/recipes_3"] = "Ok deve avere un senso bla bla blaaaablaaaaa senso qualcosa di intelligent "

    return diz

if __name__ == "__main__":
    main()
