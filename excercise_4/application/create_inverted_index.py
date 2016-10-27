#encoding=utf-8

from excercise_4.data import data_manager
from excercise_4.domain.inverted_index import InvertedIndex

def start(default=True, name="InvertedIndex", save=True, **recipes_dic):
    print "*** Start creating an inverted index ***"

    if default is True:
        index = InvertedIndex(name)

    print "\t1) Creating inverted index :: add recipes to the inverted index"
    for link, recipe in recipes_dic.iteritems():
        res = index.add_recipe(recipe)
        if res == -1:
            print "error occurred"
            return -1

    print "\t2) Creating inverted index :: computing inverse document frequency"
    index.compute_term_document_frequencies()

    print "\t3) Creating inverted index :: computing vector space"
    index.create_vector_space()

    if save is True:
        print "4) Creating inverted index :: store the inverted index on disk"
        data_manager.save_inverted_index(index)