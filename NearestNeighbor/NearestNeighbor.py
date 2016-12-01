# encoding=utf-8

import time
import shingle

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


    M = SignatureMatrix(250)
    M.add_sets(recipe_shingle_diz)
    M.create_signature_matrix(recipe_shingle_diz)
    #M.store()
    #M.print_signatures()

    b_r = [(75,3), (60,4), (50,5), (40,6), (35,7), (30,8), (25,10), (20,12), (15,15)]
    for b,r in b_r:
        start = time.time()
        print "Elaborating b:",b," r:",r,"..."
        for i in range(len(M.document_set)):
            j = i + 1
            while j < len(M.document_set):
                for b_i in range(b):
                    band_i = M.get_signature(M.document_set[i], b_i, r)
                    band_j = M.get_signature(M.document_set[j], b_i, r)

                    are_similar = False
                    for r_i in range(r):
                        are_similar = False
                        if band_i[r_i] != band_j[r_i]:
                            break
                        are_similar = True
                    if are_similar:
                        print "Find two element similar:",M.document_set[i],"and",M.document_set[j]
                        print "\tTheir Jaccard Similarity is", jaccard_similarity(recipe_shingle_diz[M.document_set[i]],recipe_shingle_diz[M.document_set[j]])
                        break
                j += 1
        print "...Finished in",time.time()-start,"seconds"


def jaccard_similarity(a, b):
    a = {i for i in a}
    b = {i for i in b}
    intersection = a & b
    union = a
    union = union.union(b)
    return float(len(intersection))/float(len(union))


def get_documents():
    from excercise_4.data import data_manager
    res, diz = data_manager.read(10)

    #diz = {}
    #diz[0] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed we can test it on the application of recipe engine (importing him as a library)?"
    #diz[1] = "Hello guys, I m sorry è but tomorrow I will not be able to come at the univerisity. As soon as Possible I send you the updated file of the relation written today Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    #diz[2] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    #diz[3] = "We have to implement è this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily è tested, and once it has been developed Simone Caldaro, [27 Nov 2016, 22:54]: ahahaha have I done something that I currently don't know? XD hahahaha Either you love me... Or you hate me... ahahahhaha"
    return diz

if __name__ == "__main__":
    main()

