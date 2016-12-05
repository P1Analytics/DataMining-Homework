# encoding=utf-8

import time
import shingle
import similarity

from signature_matrix import SignatureMatrix

def main():

    recipes = get_documents()

    ''' SHINGLE BY CHAR '''

    k = 10      # shingle length
    recipe_shingle_diz =  shingle.get_shingles(recipes, shingle_size=k
                                                      , word_shingle=False
                                                      , filter_stopword=True
                                                      , filter_punctuation=True
                                                      , stemming=True)
    # 2 create the signature matrix
    M = SignatureMatrix(100)
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    # M.print_signatures()

    # 3 find similarities
    similarity.find(M, recipe_shingle_diz)


    ''' SHINGLE BY TOKEN '''

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
    similarity.find(M, recipe_shingle_diz)


def get_documents():
    from excercise_4.data import data_manager
    res, diz = data_manager.read(100)

    #diz = {}
    #diz[0] = "bla bla blaaaablaaaaa senso qualcosa di intelligente, bla bla blaaaablaaaaa qualcosa di intelligente"
    #diz[1] = "Ok deve avere un senso, qualcosa di intelligente, bla bla blaaaablaaaaa qualcosa di intelligente"
    #diz[3] = "Ok deve avere un senso"
    return diz

if __name__ == "__main__":
    main()
