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
