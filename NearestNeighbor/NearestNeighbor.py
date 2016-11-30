# encoding=utf-8

import shingle
from signature_matrix import SignatureMatrix
def main():

    recipes = get_documents()
    recipe_shingle_diz = {}
    # 1 get shingles for a document
    for link, recipe in recipes.iteritems():
        document = recipe.__str__().replace("||", " ")
        recipe_shingle_diz[link] = shingle.get_shingles(document, k=4, filter_stopword=True, filter_punctuation=True)

    # 2 create the signature matrix
    M = SignatureMatrix(50)
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    M.print_signatures()


def get_documents():
    from excercise_4.data import data_manager
    res, diz = data_manager.read(80)

    #diz = {}
    #diz[0] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed we can test it on the application of recipe engine (importing him as a library)?"
    #diz[1] = "Hello guys, I m sorry è but tomorrow I will not be able to come at the univerisity. As soon as Possible I send you the updated file of the relation written today Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    #diz[2] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    return diz

if __name__ == "__main__":
    main()

