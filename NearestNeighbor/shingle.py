import hash
import nltk
import struct

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

    stopwords = []
    if filter_stopword:
        stopwords = nltk.corpus.stopwords.words('english')
    if filter_punctuation:
        stopwords.append(",")
        stopwords.append(".")
        stopwords.append("?")
        stopwords.append("!")
        stopwords.append("(")
        stopwords.append(")")
        stopwords.append("[")
        stopwords.append("]")
        stopwords.append("{")
        stopwords.append("}")

    shingles = {}
    current_shingles = {}
    for i in range(k):
        current_shingles[i]=""

    cnt = 0
    for token in [t.lower() for t in nltk.word_tokenize(document)]:

        if token in stopwords:
            # not consider this token
            continue
        for i in range(k):
            if cnt%k==i:
                if cnt>=k:
                    try:
                        print shingles[hash_shingle(current_shingles[i][:-1])],"already present"
                    except KeyError:
                        pass
                    shingles[hash_shingle(current_shingles[i][:-1])] = current_shingles[i][:-1]
                if len(current_shingles[i]) != 0:
                    current_shingles[i]=""
            current_shingles[i] += token+" "
        cnt+=1
    for i in range(k):
        if cnt % k == i:
            if cnt >= k:
                try:
                    print shingles[hash_shingle(current_shingles[i][:-1])], "already present"
                except KeyError:
                    pass
                shingles[hash_shingle(current_shingles[i][:-1])] = current_shingles[i][:-1]
    return shingles


def hash_shingle(shingle):
    '''
    Return an integer number of 64bit length, that is the hash of the shingle
    The hash function used is always the same!
    :param shingle:
    :return:
    '''
    h = hash.hashFamily()
    return struct.unpack("L", h(shingle))[0]