# encoding=utf-8

import requests
import time
import urllib

last_req = 0

def crawl_page(url):
    global last_req

    curr_time = int(round(time.time() * 1000))      # current time in millisecond
    if curr_time - last_req < 1000:
        time.sleep(1-((curr_time-last_req)/1000.))

    last_req = int(round(time.time() * 1000))
    response = requests.get(url)
    return response.content

def decode_url(url):
    if isinstance(url, str):
        url = unicode(url, "utf-8")
    return urllib.unquote(url.encode("utf-8"))

