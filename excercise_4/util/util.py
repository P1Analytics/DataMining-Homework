#encoding=utf-8

import re

def get_utf8_string(s):
    if isinstance(s, str):
        s = unicode(s, "utf-8")
    return s.encode("utf-8")

def decode(s):
    return s.decode("utf-8")

def remove_separator_char(s):
    return re.sub(r'[ \t\n]+', " ", s)

def rpad(s, num, c=" "):
    if not isinstance(s, str):
        s = str(s)
    return s.ljust(num)

def print_query_result(result, index):
    print "\t"+rpad("Rank", 4), "|", rpad("Score", 13), "|", rpad("Title", 80), "| Link"
    i = 1
    for t in result:
        print "\t"+rpad(str(i), 4), "|", rpad(t[1], 13), "|", rpad(index.recipes[t[0]].title, 80), "|", index.recipes[t[0]].link
        i = i + 1

def print_weighted_query_result(result, recipes_dic):
    print "\t" + rpad("Rank", 4), "|", rpad("Score", 13), "|", rpad("Title", 80), "| Link"
    i = 1
    for t in result:
        print "\t" + rpad(str(i), 4), "|", rpad(t[1], 13), "|", rpad(recipes_dic[t[0]].title, 80), "|", recipes_dic[t[0]].link
        i = i + 1