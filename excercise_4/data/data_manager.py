#encoding=utf-8
import os
import io
import time

from excercise_4.domain.recipe import Recipe
from excercise_4.domain.inverted_index import InvertedIndex
from excercise_4.util import util

data_path = os.path.dirname(os.path.abspath(__file__))
recipe_features = ["title","link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]

recipe_file_data = "recipe_file_data.tsv"
error_pages_data = "error_pages_data.tsv"
index_file_data = "index_file_data.tsv"

# data needed to keep open file in writing
global file_kept_open
global last_write
file_kept_open = None
last_write = 0

# flush_afetr: in seconds, set the time which the file has to be flushed
def saveRecipe(recipe, keep_open = True, flush_after = 180):
    global file_kept_open
    global last_write

    if not existsDataFile(recipe_file_data):
        io.FileIO(getDataFilePath(recipe_file_data), "w").close()

    if file_kept_open is None:
        data_file = open(getDataFilePath(recipe_file_data), "a")
    else:
        data_file = file_kept_open

    data_file.write(recipe.__str__()+"\n")
    if keep_open is False:
        data_file.close()
    else:
        curr_time = int(round(time.time() * 1000))      # current time in millisecond
        if curr_time-last_write > flush_after*1000:
            # the file has to be flushed
            print "DEBUG: time to flush the file!"
            data_file.flush()
            last_write = curr_time
        file_kept_open = data_file


def read_inverted_index(name="InvertedIndex"):
    '''

    :param name: name of the inverted index to read from memory
    :return: res, index --> 0 if the inverted index is create
    '''
    try:
        print "Reading inverted index [ named " + name + " ] on disk"
        print "\t1. Reading the index.."
        index_file_name = name+"__"+index_file_data
        if not existsDataFile(index_file_name):
            print "Inverted index "+index_file_name+" doesn't exist on disk"
            return -1, None

        index = InvertedIndex(name)
        data_file = open(getDataFilePath(index_file_name), "r")
        for line in data_file.readlines():
            term = line.split(" ")[0]
            postings = []
            for p in line.split(" ")[1][1:-2].split("]["):
                postings.append(map(int, p.split(",")))
            index.add(term, postings)
        data_file.close()

        print "\t2. Reading the recipe id.."
        recipes_file_name = name + "__" + recipe_file_data
        if not existsDataFile(recipes_file_name):
            print "Recipe id file " + recipes_file_name + " doesn't exist on disk"
            return -1, None

        data_file = open(getDataFilePath(recipes_file_name), "r")
        for line in data_file.readlines():
            id = int(line.split(" ")[0])
            link = line.split(" ")[1][:-1]      # doesn't read the last character '\n'
            index.add(id, link, False)
        data_file.close()

        print "\tInverted index [ named " + name + " ] correctly read"
    except Exception as e:
        print "*ERROR* at data_manager.save_inverted_index", e,"Impossible to write the index on disk"
        return -1, None
    return 0, index


def save_inverted_index(index):
    '''
    Save the index (posting list + recipe id) on the disk
    :param index: the inverted index to save
    :return: 0 if the operation goes well, -1 otherwise
    '''
    try:
        print "Saving inverted index [ "+index.name+" ] on disk"
        print "\t1. Saving the index"
        index_file_name = index.name+"__"+index_file_data
        if not existsDataFile(index_file_name):
            io.FileIO(getDataFilePath(index_file_name), "w").close()

        data_file = open(getDataFilePath(index_file_name), "w")
        for term, posting_list in index.iteritems():
            row = term + " "
            for posting in posting_list:
                row += "["+str(posting[0])+","+str(posting[1])+"]"        # [ doc_id , term_frequency ]
            row += "\n"
            data_file.write(util.get_utf8_string(row))
        data_file.close()


        print "\t2. Saving the recipe id"
        recipes_file_name = index.name + "__" + recipe_file_data
        if not existsDataFile(recipes_file_name):
            io.FileIO(getDataFilePath(recipes_file_name), "w").close()

        data_file = open(getDataFilePath(recipes_file_name), "w")
        for id, recipe in index.recipes_iteritems():
            row = str(id) + " " + recipe.link + "\n"
            data_file.write(util.get_utf8_string(row))
        data_file.close()

    except Exception as e:
        print "*ERROR* at data_manager.save_inverted_index", e,"Impossible to write the index on disk"
        return -1
    return 0


def read(max=None):
    '''

    :param max: max number of entry you want to read
    :return: res, diz : if everything goes well res = 0 and diz is the dictionary, otherwise -1, None
    '''
    num_recipe_read = 0
    stop_read = max is not None and isinstance(max, int)
    data_file = open(getDataFilePath(recipe_file_data), "r")
    diz = {}
    for line in data_file.readlines():
        num_recipe_read += 1
        if stop_read and num_recipe_read > max:
            return diz
        i = 0;
        recipe_dic = {}
        for elem in line.split('\t'):
            if elem == "\n":
                break
            recipe_dic[recipe_features[i]] = elem
            i = i+1
        try:
            title = recipe_dic["title"]
            link = recipe_dic["link"]
            del recipe_dic["title"]
            del recipe_dic["link"]
        except KeyError:
            continue
        rec = Recipe(title,link, **recipe_dic)
        diz[rec.link] = rec
    data_file.close()
    return 0, diz


def save_error_pages(**error_pages):
    if not existsDataFile(error_pages_data):
        io.FileIO(getDataFilePath(error_pages_data), "w").close()

    err_file = io.FileIO(getDataFilePath(error_pages_data), "w")
    for link, recipe in error_pages.iteritems():
        err_file.write(link+"\t"+recipe.title+"\n")
    err_file.close()

def close_open_file():
    global file_kept_open
    if file_kept_open is not None:
        file_kept_open.close()

def existsDataFile(file):
    return os.path.isfile(getDataFilePath(file))

def getDataFilePath(file):
    return data_path+'/'+str(file)