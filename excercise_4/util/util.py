#encoding=utf-8

def get_utf8_string(s):
    if isinstance(s, str):
        s = unicode(s, "utf-8")
    return s.encode("utf-8")

def remove_separator_char(s):
    s = s.replace("\t", " ")
    s = s.prepace("\n", " ")
    return s