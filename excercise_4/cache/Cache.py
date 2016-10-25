# encoding=utf-8

import io
import os

cache_path = os.path.dirname(os.path.abspath(__file__))

def getCacheFilePath(file):
    return cache_path+'/'+file

def existsCacheFile(file):
    return os.path.isfile(getCacheFilePath(file))

def readCacheFileToList(file):
    cache_file = open(getCacheFilePath(file), "r")
    res = []
    for line in cache_file.readlines():
        row = []
        for elem in line.split('\t'):
            row.append(elem)
        res.append(row)
    cache_file.close()
    return res

def cacheDataToFile(file, data):
    print "Cache > saving data to cache file: "+file+"..."
    cache_file = open(getCacheFilePath(file), "w")
    for row in data:
        for elem in row:
            if isinstance(elem, str):
                elem = unicode(elem, "utf-8")
            try:
                cache_file.write(elem.encode("utf-8")+'\t')
            except UnicodeEncodeError:
                print "\tATT: impossibile to save string "+elem
        cache_file.write('\n')
    cache_file.close()
    print "..."+str(len(data))+" rows saved!"

def createCacheFile(file):
    print "Cache > create new cache file: " + file
    io.FileIO(getCacheFilePath(file), "w").close()