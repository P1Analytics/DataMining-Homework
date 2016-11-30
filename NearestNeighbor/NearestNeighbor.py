import shingle

def main():

    document = "We have to implement this nearest neighbour and test it in the recipe engine. What do you think if we develope a sort of python module fon NN, that can be easily tested, and once it has been developed we can test it on the application of recipe engine (importing him as a library)?"

    # 1. Implement a class that, given a document, creates its set of character shingles of some length k.
    #    Then represent the document as the set of the hashes of the shingles, for some hash function.
    print "Shingle number(Filter stopwords and punctuation):",len(shingle.get_shingles(document, k=3, filter_stopword=True, filter_punctuation=True))
    print "\t",shingle.get_shingles(document, k=3, filter_stopword=True, filter_punctuation=True)
    print "\n\nShingle number(Do not Filter stopwords and punctuation):",len(shingle.get_shingles(document, 3, filter_stopword=False, filter_punctuation=False))
    print "\t",shingle.get_shingles(document, 3, filter_stopword=False, filter_punctuation=False)
    #print doc_shingles

if __name__ == "__main__":
    main()