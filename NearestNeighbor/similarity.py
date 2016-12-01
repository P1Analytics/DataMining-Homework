import math
import time

b_r = [(25, 1), (15, 1), (10, 1), (20, 3), (5, 1), (3, 1), (5, 2), (5, 3), (1, 1)]

def find(signature_matrix, sets):

    #b_r = [(75, 3), (60, 4), (50, 5), (40, 6), (35, 7), (27, 9), (25, 10), (20, 12), (15, 15)]
    matrix_b_r = []
    for b,r in b_r:
        factor = int(math.sqrt(signature_matrix.n_hash_functions/(b*r)))
        matrix_b_r.append((b*factor, r*factor))

    start = time.time()
    print "Finding similarities..."
    for i in range(len(signature_matrix.document_set)):
        print "\n\t- ", signature_matrix.document_set[i], "VS others"
        j = i + 1
        while j < len(signature_matrix.document_set):
            for b, r in matrix_b_r:
                for b_i in range(b):
                    band_i = signature_matrix.get_signature(signature_matrix.document_set[i], b_i, r)
                    band_j = signature_matrix.get_signature(signature_matrix.document_set[j], b_i, r)

                    are_similar = False
                    for r_i in range(r):
                        are_similar = False
                        if band_i[r_i] != band_j[r_i]:
                            break
                        are_similar = True
                    if are_similar:
                        print "\t\tFind similarity with", signature_matrix.document_set[j]
                        print "\t\tb =", b, " r =", r, " --> threshold:", math.pow((1. / float(b)), 1. / float(r))
                        print "\t\tJaccard Similarity:", jaccard_similarity(sets[signature_matrix.document_set[i]],
                                                                                  sets[signature_matrix.document_set[j]])
                        break
            j += 1
    print "...Finished in", time.time() - start, "seconds"

def jaccard_similarity(a, b):
    a = {i for i in a}
    b = {i for i in b}
    intersection = a & b
    union = a
    union = union.union(b)
    return float(len(intersection))/float(len(union))