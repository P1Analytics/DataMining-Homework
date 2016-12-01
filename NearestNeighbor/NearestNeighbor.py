# encoding=utf-8

import time
import shingle
import similarity

from signature_matrix import SignatureMatrix

def main():

    recipes = get_documents()

    k = 10      # shingle length
    recipe_shingle_diz = {}
    # 1 get shingles for a document
    for link, recipe in recipes.iteritems():
        document = recipe.__str__().replace("||", " ")
        n_shingles, shingles = shingle.get_shingles(document, k=k, filter_stopword=True, filter_punctuation=True, stemming=True)
        if n_shingles > 0:
            recipe_shingle_diz[link] = shingles

    # 2 create the signature matrix
    M = SignatureMatrix(100)
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    #M.store()
    #M.print_signatures()

    similarity.find(M, recipe_shingle_diz)

def jaccard_similarity(a, b):
    a = {i for i in a}
    b = {i for i in b}
    intersection = a & b
    union = a
    union = union.union(b)
    return float(len(intersection))/float(len(union))


def get_documents():
    from excercise_4.data import data_manager
    res, diz = data_manager.read()

    #diz = {}
    #diz[0] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed we can test it on the application of recipe engine (importing him as a library)?"
    #diz[1] = "Hello guys, I m sorry è but tomorrow I will not be able to come at the univerisity. As soon as Possible I send you the updated file of the relation written today Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    #diz[2] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    #diz[3] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    return diz

if __name__ == "__main__":
    main()

