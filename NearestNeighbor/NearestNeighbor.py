# encoding=utf-8

import os
import sys
import shingle
import similarity

from signature_matrix import SignatureMatrix

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def main():
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
                   'http://www.bbc.co.uk/food/recipes/gourmetburgers_70174']

    recipes = get_documents()

    k = 10
    ''' SHINGLE BY CHAR '''
    recipe_shingle_diz =  shingle.get_shingles(recipes, shingle_size=k
                                                      , word_shingle=False
                                                      , filter_stopword=True
                                                      , filter_punctuation=True
                                                      , stemming=True)
    # 2 create the signature matrix
    M = SignatureMatrix(100)
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    #M.print_signatures()

    # 3 find similarities
    similarity.find(M, recipe_shingle_diz)


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
    res, diz = data_manager.read()

    #diz = {}
    #diz["food/recipes_0"] = "bla bla blaaaablaaaaa senso qualcosa di in food/ recipes telligente, bla bla blaaaablaaaaa qualcosa di intelligente"
    #diz["food/recipes_1"] = "bla bla blaaaablaaaaa senso qualcosa di in food/ recipes telligente, bla bla blaaaablaaaaa qualcosa di intelligente"
    #diz["food/recipes_2"] = "bla bla blaaaablaaaaa senso qualcosa di intelligent food/recipes food/recipes food/recipes e, bla bla blaaa Ok deve avere un senso ablaaaaa qualcosa di intelligente"
    #diz["food/recipes_3"] = "Ok deve avere un senso bla bla blaaaablaaaaa senso qualcosa di intelligent "

    return diz

if __name__ == "__main__":
    main()
