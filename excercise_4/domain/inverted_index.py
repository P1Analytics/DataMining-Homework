# encoding=utf-8

import nltk
import math
import heapq
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

    def look_for(self, query, k=10, recipes_filter=None):

        result_list = {}

        # tokenization of the query
        for term in {t.lower() for t in nltk.word_tokenize(query)}:
            # delete stopwrods from the query
            if term in self.stopwords:
                continue
            # stemming the token
            term = self.english_stemmer.stem(term)

            if recipes_filter is None:
                for posting in self.index[term][1:]:
                    recipe_id = posting[0]
                    tfidf = self.vector_space.get_recipe_term_tfidf(recipe_id, term)
                    try:
                        result_list[recipe_id] = float(result_list[recipe_id]) + float(tfidf)
                    except KeyError:
                        result_list[recipe_id] = float(tfidf)
            else:
                for recipe_id in recipes_filter:
                    tfidf = self.vector_space.get_recipe_term_tfidf(recipe_id, term)
                    try:
                        result_list[recipe_id] = float(result_list[recipe_id]) + float(tfidf)
                    except KeyError:
                        result_list[recipe_id] = float(tfidf)

        top_k_heap = []
        for recipe_id, tfidf in result_list.iteritems():
            heapq.heappush(top_k_heap, (tfidf, recipe_id))

        for t in heapq.nlargest(k, top_k_heap):
            recipe_id = t[1]
            tfidf = t[0]
            print recipe_id, tfidf, self.recipes[recipe_id].link

    def and_query(self, query, k=10):

        postings_list = {}
        heap_len_postings = []

        # tokenization of the query
        for term in {t.lower() for t in nltk.word_tokenize(query)}:
            # delete stopwrods from the query
            if term in self.stopwords:
                continue
            # stemming the token
            term = self.english_stemmer.stem(term)

            heapq.heappush(heap_len_postings, (len(self.index[term]), term))

        # sort the term based on the length of the posting lists
        ordered_term = heapq.nsmallest(k, heap_len_postings)
        if len(ordered_term) <= 1:
            # query with only one term --> nothing to AND
            self.look_for(query, k)
        else:
            # first term with the smallest posting list (that is also the maximum result achievable within intersection)
            curr_term = ordered_term[0][1]
            #res = self.index[curr_term][1:]
            res = []
            for posting in self.index[curr_term][1:]:
                res.append(posting[0])
            i = 1
            while i<len(ordered_term):

                # get next posting list, starting from the second element (the first is the IDF of the term)
                posting_to_compare = self.index[ordered_term[i][1]][1:]
                res = self.merge(res, posting_to_compare)
                i=i+1

            self.look_for(query, k, res)


    def merge(self, postings_1, postings_2):
        if len(postings_1)==0:
            return []
        if len(postings_2)==0:
            return []

        index_1 = 0
        index_2 = 0

        res = []
        while index_1<len(postings_1) and index_2<len(postings_2):
            curr_recipe_id1 = postings_1[index_1]
            curr_recipe_id2 = postings_2[index_2][0]
            if curr_recipe_id1==curr_recipe_id2:
                # match found --> add this recipe_in in the final result
                res.append(curr_recipe_id1)
                index_1 += 1
                index_2 += 1
            elif curr_recipe_id1 < curr_recipe_id2:
                index_1 += 1
            else:
                index_2 += 1

        return res

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


        self.recipes[self.unique_id] = recipe
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

    def get_term_id(self, term):
        return self.term_id[term]

    def add_entry_to_vector(self, recipe_id, term, normalized_tfidf):
        self.bag_of_words[recipe_id][term] = normalized_tfidf
        pass

    def get_recipe_term_tfidf(self, recipe_id, term):
        term_id = self.get_term_id(term)
        return self.bag_of_words[recipe_id][term_id]


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