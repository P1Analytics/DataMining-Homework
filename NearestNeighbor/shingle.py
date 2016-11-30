import hash
import nltk
import struct

'''
 1. Implement a class that, given a document, creates its set of character shingles of some length k.
    Then represent the document as the set of the hashes of the shingles, for some hash function.
'''

def get_shingles(document, k=8, filter_stopword=False, filter_punctuation=False):
    '''
    the object returned is a dictionary with:
        - key: the hash of the shingles
        - value: the shingle string
    :param document:
    :param k: number of lenght of a shingle
    :param filter_stopword: if true stpowords are not considered
    :param filter_punctuation: if true punctuation is not considered
    :return: the set of shingles of size k
    '''
    print "SHINGLE > get_shingle ..."
    stopwords = []
    if filter_stopword:
        stopwords = nltk.corpus.stopwords.words('english')
    if filter_punctuation:
        stopwords.append(",")
        stopwords.append(".")
        stopwords.append("?")
        stopwords.append("|")
        stopwords.append("!")
        stopwords.append("(")
        stopwords.append(")")
        stopwords.append("[")
        stopwords.append("]")
        stopwords.append("{")
        stopwords.append("}")

    shingles = []
    current_shingles = {}
    for i in range(k):
        current_shingles[i]=""

    cnt = 0
    document = document.decode("utf8")
    for token in [t.lower() for t in nltk.word_tokenize(document)]:
        if token in stopwords:
            # not consider this token
            continue
        for i in range(k):
            if cnt%k==i:
                if cnt>=k and current_shingles[i][:-1] not in shingles:
                    shingles.append(current_shingles[i][:-1])
                if len(current_shingles[i]) != 0:
                    current_shingles[i]=""
            current_shingles[i] += token+" "
        cnt+=1
    for i in range(k):
        if cnt % k == i:
            if cnt >= k and current_shingles[i][:-1] not in shingles:
                shingles.append(current_shingles[i][:-1])
    return shingles

def hash_shingle(shingle):
    '''
    :param shingle:
    :return:
    '''
    h = hash.hashFamily()
    return h(shingle)
    #return struct.unpack("Q", h(shingle))[0]