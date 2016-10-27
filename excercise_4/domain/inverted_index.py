# encoding=utf-8

import nltk
import math
from nltk.stem.snowball import EnglishStemmer
from collections import defaultdict
from excercise_4.util import util

class InvertedIndex(object):

    def __init__(self, name):
        self.name = name
        self.features = ["title", "link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]
        self.english_stemmer = EnglishStemmer()
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords.append(",")
        self.index = defaultdict(list)
        self.unique_id = int(0)     # counter that represents an id, to identificate a recipe
        self.recipes = {}
        self.vector_space = VectorSpace()

    def iteritems(self):
        return self.index.iteritems()

    def recipes_iteritems(self):
        return self.recipes.iteritems()

    def add(self, key, value, is_posting = True):
        '''

        :param key: if is_posting = True --> it is a term, otherwise it is a recipe_id
        :param value: if is_posting = True --> it is a posting_list, otherwise it is the link of the recipe
        :param is_posting: True when adding a pair (term, posting_list), False when adding a pair(recipe_id, recipe_link)
        :return:
        '''
        if is_posting:
            self.index[key] = value
        else:
            self.recipes[key] = value

    def add_recipe(self, recipe):
        '''
        :param recipe: object Recipe to add to the inverted index
        :return: 0 recipe add correctly, -1 in case of error
        '''
        print "\tAdding recipe to the inverted index " + recipe.link

        tokens_to_count = []
        for feature in self.features:
            str_to_tokenize = ""
            if feature == "ingredients":
                for sub_recipe, sub_recipe_ingr in recipe.__getattribute__(feature).iteritems():
                    sub_recipe = util.get_utf8_string(sub_recipe)
                    sub_recipe_ingr = util.get_utf8_string(', '.join(sub_recipe_ingr))
                    str_to_tokenize += util.remove_separator_char((sub_recipe + " " + sub_recipe_ingr + " "))
            elif feature == "method":
                for step in recipe.__getattribute__(feature):
                    str_to_tokenize += step + " "
            elif feature == "link":
                continue
            else:
                str_to_tokenize = recipe.__getattribute__(feature)

            str_to_tokenize = util.decode(str_to_tokenize)
            try:
                for token in [t.lower() for t in nltk.word_tokenize(str_to_tokenize)]:
                    if token in self.stopwords:
                        continue
                    token = self.english_stemmer.stem(token)
                    tokens_to_count.append(token)
            except Exception as e:
                print "*WARNING*", e, feature
                return -1


        for token, frequence in nltk.FreqDist(tokens_to_count).iteritems():
            self.index[token].append([self.unique_id, frequence])


        self.recipes[self.unique_id] = [recipe, 0]
        self.unique_id = self.unique_id + 1
        return 0

    def compute_term_document_frequencies(self):
        num_recipes = len(self.recipes)
        for term, posting_list in self.index.iteritems():
            # compute the idf of a term
            df = len(posting_list)
            idf = math.log(float(num_recipes)/float(df), 10)
            self.index[term].insert(0, idf)

    def create_vector_space(self):
        self.vector_space.create(self)

    def bag_of_words_iteritems(self):
        return self.vector_space.bag_of_words.iteritems()

class VectorSpace(object):
    def __init__(self):
        self.bag_of_words = defaultdict(dict)  # see a recipe as a bag of words (stemmed and without stopwords)
        self.term_id = {}  # used in the vecotr space model --> identifier of a term

    def set_term_id(self, term, term_id):
        self.term_id[term] = term_id

    def add_entry_to_vector(self, recipe_id, term, normalized_tfidf):
        self.bag_of_words[recipe_id][term] = normalized_tfidf
        pass

    def create(self, index):
        print "\t\tIndex > VectorSpace :: start creating"
        term_id = 0
        for term, posting_list in index.iteritems():
            print "\t\t\tComputing term "+term+" > assign it the id "+str(term_id)
            # assign an id to a term --> used in the VSM
            self.term_id[term] = term_id
            term_id += 1

            # compute tf-idf for every entry in our space
            idf = 0.
            for posting in posting_list:
                try:
                    recipe_id = posting[0]
                    tf = posting[1]
                    if self.bag_of_words[recipe_id] is None:
                        self.bag_of_words[recipe_id] = {}
                    self.bag_of_words[recipe_id][self.term_id[term]] = tf * idf
                except Exception:
                    idf = posting

        # The real "vector" that represents a recipe is created, as a bag of tf-idf
        # --> we consider only the entry where tf-idf is not equal to 0
        for recipe_id, tfidf_terms in self.bag_of_words.iteritems():
            print "\t\t\tNormalize the the vector that corresponds to the recipe "+str(recipe_id)
            # compute lenght of a recipe
            len = 0.
            for term, tfidf in tfidf_terms.iteritems():
                len = len + (tfidf * tfidf)
            len = math.sqrt(len)

            # normalize the recipe vector
            for term, tfidf in tfidf_terms.iteritems():
                self.add_entry_to_vector(recipe_id, term, tfidf/len)