import hash
import nltk
import time
from nltk.stem.snowball import EnglishStemmer


'''
 1. Implement a class that, given a document, creates its set of character shingles of some length k.
    Then represent the document as the set of the hashes of the shingles, for some hash function.
'''

stemmer = EnglishStemmer()

def get_shingles(documents, shingle_size=8, word_shingle=False, filter_stopword=False, filter_punctuation=False, stemming=False):
    print "1) SHINGLE :: get_shingles"
    print "\t"
    shingle_diz = {}

    stopwords = []
    if filter_stopword:
        stopwords = nltk.corpus.stopwords.words('english')
    if filter_punctuation:
        stopwords.append(",")
        stopwords.append(":")
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

    cnt = 0
    percent = 0
    start = time.time()
    for doc_id, document in documents.iteritems():
        cnt += 1
        if cnt >= len(documents) / 100.:
            print "\t\t", percent, "% ..."
            percent += 1
            cnt = 0
        if "food/recipes" not in str(doc_id):
            continue

        document = document.__str__().replace("||", " ")
        n_shingles, shingles = get_document_shingles(document, k=shingle_size, word_shingle=word_shingle, stopwords=stopwords, stemming=stemming)
        if n_shingles > 0:
            shingle_diz[doc_id] = shingles
    print "\tSHINGLE :: get_shingles computed in:", time.time() - start, "seconds"
    return shingle_diz

def get_document_shingles(document, k=8, word_shingle=False, stopwords=[], stemming=False):
    '''
    the object returned is a dictionary with:
        - key: the hash of the shingles
        - value: the shingle string
    :param document:
    :param k: number of lenght of a shingle
    :param stopwords: array of stopwords
    :return: the set of shingles of size k
    '''

    shingles = []
    current_shingles = {}

    if word_shingle is False:
        k = k+1

    for i in range(k):
        current_shingles[i]=""

    cnt = 0
    document = document.decode("utf8")
    for token in [t.lower() for t in nltk.word_tokenize(document)]:
        if token in stopwords:
            # not consider this token
            continue

        if stemming:
            token = stemmer.stem(token)

        if word_shingle is False:
            for c in token:
                cnt = fill_shingle(c, cnt, current_shingles, k, shingles)
        else:
            cnt = fill_shingle(token+" ", cnt, current_shingles, k, shingles)

        if word_shingle is False:
            cnt = fill_shingle(" ", cnt, current_shingles, k, shingles)

    for i in range(k):
        if cnt % k == i:
            if cnt >= k and current_shingles[i][:-1] not in shingles:
                shingles.append(current_shingles[i][:-1])

    return len(shingles), [hash.hashFamily()(x.encode("utf8")) for x in shingles] #shingles


def fill_shingle(c, cnt, current_shingles, k, shingles):
    '''

    :param c: a word or a charachter
    :param cnt:
    :param current_shingles:
    :param k:
    :param shingles:
    :return:
    '''
    for i in range(k):
        if cnt % k == i:
            if cnt >= k and current_shingles[i][:-1] not in shingles:
                shingles.append(current_shingles[i][:-1])
            if len(current_shingles[i]) != 0:
                current_shingles[i] = ""
        current_shingles[i] += c
    cnt += 1
    return cnt
