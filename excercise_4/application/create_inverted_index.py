#encoding=utf-8

import nltk
from nltk.stem.snowball import EnglishStemmer
from collections import defaultdict
from excercise_4.data import data_manager
from excercise_4.util import util

import sys

features = ["title","link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]
english_stemmer = EnglishStemmer()
stopwords       = nltk.corpus.stopwords.words('english')
index           = defaultdict(list)
unique_id       = int(0)
recipes       = {}

stopwords.append(",")

def start(**recipes_dic):
    print "*** Start creating an inverted index ***"

    for link, recipe in recipes_dic.iteritems():
        res = add(recipe)
        if res == -1:
            print "error occurred"
            return -1

        # Docuement frequencies --> in how many recipes a term
        # for k,v in index.iteritems():
        #     print "term: ",k, " > Df: ", len(v), v
    for k,v in index.iteritems():
        print k, v


def add(recipe):
    '''
    :param recipe: object Recipe to add to the inverted index
    :return: 0 recipe add correctly, -1 in case of error
    '''
    print "\tAdding recipe to the inverted index "+recipe.link
    global unique_id
    global recipes

    tokens_to_count = []
    for feature in features:
        str_to_tokenize = ""
        if feature=="ingredients":
            for sub_recipe, sub_recipe_ingr in recipe.__getattribute__(feature).iteritems():
                sub_recipe = util.get_utf8_string(sub_recipe)
                sub_recipe_ingr = util.get_utf8_string(', '.join(sub_recipe_ingr))
                str_to_tokenize += util.remove_separator_char((sub_recipe + " " + sub_recipe_ingr + " "))
        elif feature=="method":
            for step in recipe.__getattribute__(feature):
                str_to_tokenize+=step+" "
        elif feature=="link":
            continue
        else:
            str_to_tokenize = recipe.__getattribute__(feature)

        str_to_tokenize = util.decode(str_to_tokenize)
        try:
            for token in [t.lower() for t in nltk.word_tokenize(str_to_tokenize)]:
                if token in stopwords:
                    continue
                token = english_stemmer.stem(token)
                tokens_to_count.append(token)
        except Exception as e:
            print e
            print "*WARNING*"+feature
            return -1
    for token, frequence in nltk.FreqDist(tokens_to_count).iteritems():
        index[token].append([unique_id, frequence])

    recipes[unique_id] = recipe
    unique_id = unique_id + 1
    return 0


recipes_dic = data_manager.read()
start(**recipes_dic)