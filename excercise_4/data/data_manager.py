#encoding=utf-8
import os
import io
import time

from excercise_4.domain.recipe import Recipe

data_path = os.path.dirname(os.path.abspath(__file__))
recipe_features = ["title","link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]

recipe_file_data = "recipe_file_data.tsv"
error_pages_data = "error_pages_data.tsv"

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


def read():
    data_file = open(getDataFilePath(recipe_file_data), "r")
    res = {}
    for line in data_file.readlines():
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
        res[rec.link] = rec
    data_file.close()
    return res


def save_error_pages(**error_pages):
    if not existsDataFile(error_pages_data):
        io.FileIO(getDataFilePath(error_pages_data), "w").close()

    err_file = io.FileIO(getDataFilePath(error_pages_data), "w")
    for link, recipe in error_pages.iteritems():
        err_file.write(link+"\t"+recipe.title)
    err_file.close()

def close_open_file():
    global file_kept_open
    if file_kept_open is not None:
        file_kept_open.close()


def existsDataFile(file):
    return os.path.isfile(getDataFilePath(file))

def getDataFilePath(file):
    return data_path+'/'+str(file)