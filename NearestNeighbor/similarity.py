import hash
import math
import time

b_r = [(25, 1), (15, 1), (10, 1), (20, 3), (5, 1), (4,1), (3, 1), (5, 2), (5, 3), (1, 1)]

def find(signature_matrix, sets, threshold=0.8):

    # matrix_b_r = []
    # for b,r in b_r:
    #     factor = int(math.sqrt(signature_matrix.n_hash_functions/(b*r)))
    #     if factor == 0:
    #         continue
    #     curr_threshold = math.pow((1. / float(b*factor)), 1. / float(r*factor))
    #     if curr_threshold < threshold - 0.1*(threshold):
    #         continue
    #     matrix_b_r.append((b*factor, r*factor))

    matrix_b_r = [(20,5), (10,10), (25,4), (30,3)]
    bucket = {}
    for b,r in matrix_b_r:
        if b==0 or r==0:
            continue
        bucket[(b,r)] = {}

    hash_function = hash.hashFamily()

    print "\nFinding similarities with LSH..."
    start = time.time()
    for i in range(len(signature_matrix.document_set)):
        set_id = signature_matrix.document_set[i]
        for b, r in matrix_b_r:
            for b_i in range(b):
                try:
                    # bucket for band b_i of (b,r) already existing
                    bucket[(b,r)][b_i]
                except KeyError:
                    # Creating the bucket for band b_i of (b,r)
                    bucket[(b,r)][b_i] = {}

                # r hases of the b_i-th band
                band_signature = signature_matrix.get_signature(signature_matrix.document_set[i], b_i, r)

                band_signature_hash = hash_function(band_signature.__str__())
                try:
                    bucket[(b,r)][b_i][band_signature_hash].append(set_id)
                except KeyError:
                    bucket[(b,r)][b_i][band_signature_hash] = []
                    bucket[(b,r)][b_i][band_signature_hash].append(set_id)


    for (b,r), buckets in bucket.iteritems():
        found_set_lsh = []
        print "b =", b, " r =", r, " --> threshold:", math.pow((1. / float(b)), 1. / float(r))
        for band, band_buckets in buckets.iteritems():
            for hashes, set_ids in band_buckets.iteritems():
                if len(set_ids)>1:
                    for i in range(len(set_ids)-1):
                        for j in range(i+1, len(set_ids)):
                            if (set_ids[i], set_ids[j]) not in found_set_lsh:
                                js = jaccard_similarity(sets[set_ids[i]],sets[set_ids[j]])
                                label = "TRUE POSITIVE"
                                if js < threshold:
                                    label = "FALSE POSITIVE"
                                print "\t-", set_ids[i], "VS", set_ids[j], "JS:", js, label
                                found_set_lsh.append((set_ids[i], set_ids[j]))
                                found_set_lsh.append((set_ids[j], set_ids[i]))
    print "...Finished in", time.time() - start, "seconds\n"

    print "Finding similarities with Jaccard simlarity..."
    start = time.time()
    for i in range(len(signature_matrix.document_set)):
        j = i + 1
        while j < len(signature_matrix.document_set):
            js = jaccard_similarity(sets[signature_matrix.document_set[i]], sets[signature_matrix.document_set[j]])
            if js >= threshold:
                print "\t-",js,":",signature_matrix.document_set[i], "and", signature_matrix.document_set[j]
            j += 1
    print "...Finished in", time.time() - start, "seconds"

def jaccard_similarity(a, b):
    a = set(a)
    b = set(b)
    intersection = a & b
    union = a
    union = union.union(b)
    return float(len(intersection))/float(len(union))