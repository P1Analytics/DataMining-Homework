import hashlib
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
    h = hashFamily()
    return struct.unpack("L", h(shingle))[0]

def main():

    document = "We have to implement this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily tested, and once it has been developed we can test it on the application of recipe engine (importing him as a library)?"

    # 1. Implement a class that, given a document, creates its set of character shingles of some length k.
    #    Then represent the document as the set of the hashes of the shingles, for some hash function.
    print "Shingle number(Filter stopwords):",len(get_shingles(document, k=3, filter_stopword=True, filter_punctuation=True))
    print get_shingles(document, k=3, filter_stopword=True, filter_punctuation=True)
    print "Shingle number(Do not Filter stopwords):",len(get_shingles(document, 3, False))
    #print doc_shingles


def hashFamily(i=0):
    '''
    Implement a family of hash functions. It hashes strings and takes an # integer to define the member of the family.
    Return a hash function parametrized by i
    :param i:
    :return:
    '''
    resultSize = 8      # how many bytes we want back
    maxLen = 20         # how long can our i be (in decimal)
    salt = str(i).zfill(maxLen)[-maxLen:]
    def hashMember(x):
        return hashlib.sha1(x + salt).digest()[-resultSize:]
    return hashMember

if __name__ == "__main__":
    main()