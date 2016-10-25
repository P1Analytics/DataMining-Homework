# encoding=utf-8

import nltk
from nltk.stem.snowball import EnglishStemmer
from collections import defaultdict
from excercise_4.util import util

class InvertedIndex(object):

    def __init__(self, name = "InvertedIndex"):
        self.name = name
        self.features = ["title", "link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]
        self.english_stemmer = EnglishStemmer()
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords.append(",")
        self.index = defaultdict(list)
        self.unique_id = int(0)
        self.recipes = {}

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
                print e
                print "*WARNING*" + feature
                return -1
        for token, frequence in nltk.FreqDist(tokens_to_count).iteritems():
            self.index[token].append([self.unique_id, frequence])

        self.recipes[self.unique_id] = recipe
        self.unique_id = self.unique_id + 1
        return 0