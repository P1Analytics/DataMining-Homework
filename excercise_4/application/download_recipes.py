# encoding=utf-8
#!/usr/bin/env python

from bs4 import BeautifulSoup
from string import ascii_lowercase
from excercise_4.application import crawl
from excercise_4.cache import Cache
from excercise_4.domain import recipe

class DishLink(object):
    def __init__(self,dish,link):
        self.dish=dish
        self.link=link

    def __str__(self):
        return "<"+self.dish+", "+self.link+">"


target = "http://www.bbc.co.uk"

def start():
    print "*** Start Downloading recipes  ***"

    # 1
    dish_link_list = get_dishes_and_links()

    # 2
    all_recipes_link_list = get_all_recipes_link(dish_link_list)

    # 3
    return get_recipe_link(all_recipes_link_list)



''' 3) Compute the specific link for each recipe '''
def get_recipe_link(all_recipes_link_list=[], search_by_keyword=True, cache=True, cache_file="cache_link_recipes.tsv"):
    print "*** 3) Downloading recipes :: Compute the specific link for each recipe ***"

    recipe_links_dic = {};
    if cache is True:
        if Cache.existsCacheFile(cache_file):
            # If results are cached, return them!
            data_read = Cache.readCacheFileToList(cache_file)
            for line in data_read:
                recipe_title = line[0]
                recipe_link = line[1]
                recipe_links_dic[recipe_link] = recipe.Recipe(recipe_title, recipe_link)
            if len(recipe_links_dic) != 0:
                return recipe_links_dic
        else:
            # Results are not yet cached --> create cache file
            Cache.createCacheFile(cache_file)

    # go to the dish's page --> get all recipes fot that dishes!
    for rl in all_recipes_link_list:
        # check if we want search recipes by keyword
        if not search_by_keyword and "keywords" in rl.link:
            continue
        print "\tcomputing " + rl.dish + "..."

        link_to_crawl = rl.link
        retry = 5
        while True:
            soup = BeautifulSoup(crawl.crawl_page(link_to_crawl), 'html.parser')
            container_article_list = soup.find('div', {"id": "article-list"})
            try:
                article_list = container_article_list.find_all("li", class_="article")
                for article in article_list:
                    article_soup = BeautifulSoup(str(article), 'html.parser')
                    # print article_soup
                    recipe_link = target + article_soup.find("a").attrs["href"]
                    try:
                        recipe_title = article_soup.find("a").contents[1]
                    except IndexError:
                        recipe_title = article_soup.find("a").contents[0]
                    if recipe_link not in recipe_links_dic:
                        recipe_links_dic[recipe_link] = recipe.Recipe(recipe_title, recipe_link)
                    else:
                        print "\t\t\tATT: "+recipe_link+" already got"

                # after we cycle in the article of the current page, it may be possible that other page with other recipes are present
                link_to_crawl = None
                next_page = soup.find_all('a', class_="see-all-search")
                if len(next_page) > 0:
                    for p in next_page:
                        if p.contents[0]=="Next":
                            # next page found, must elaborate it
                            link_to_crawl = target + crawl.decode_url(p.attrs['href'])
                            print "\t\tGo to the next page of recipes: "+link_to_crawl
                            break
                if link_to_crawl is None:
                     break
            except AttributeError:
                print "\t\t*WARNING*: error during parsing the page, tentative number "+str(6-retry)+" to elaborate again!"
                if retry == 0:
                    break
                retry -= 1

    # cache data
    data_to_cache = []
    for link, re in recipe_links_dic.iteritems():
        data_to_cache.append([re.title, re.link])
    Cache.cacheDataToFile(cache_file, data_to_cache)

    return recipe_links_dic

''' 2) given a dish get links for all recipes '''
def get_all_recipes_link(dish_link_list=[], cache = True, cache_file="cache_all_recipes.tsv"):
    print "*** 2) Downloading recipes :: given a dish get links for all recipes ***"

    all_recipes_link_list = []
    if cache is True:
        if Cache.existsCacheFile(cache_file):
            # If results are cached, return them!
            data_read = Cache.readCacheFileToList(cache_file)
            for line in data_read:
                dish = line[0]
                link = line[1]
                all_recipes_link_list.append(DishLink(dish, link))
            if len(all_recipes_link_list) != 0:
                return all_recipes_link_list
        else:
            # Results are not yet cached --> create cache file
            Cache.createCacheFile(cache_file)

    for dl in dish_link_list:
        print "\tcomputing "+dl.dish+"..."
        soup = BeautifulSoup(crawl.crawl_page(dl.link), 'html.parser')
        for soup_link in soup.find_all('a', class_="see-all-search"):
            all_recipes_link_list.append(DishLink(dl.dish, target + soup_link.attrs['href']))

    data_to_cache = []
    for dl in all_recipes_link_list:
        data_to_cache.append([dl.dish, dl.link])
    Cache.cacheDataToFile(cache_file, data_to_cache)

    print "*** END PHASE 1 ***"

    return all_recipes_link_list


''' 1) get dishes and links '''
def get_dishes_and_links(cache=True, cache_file="cache_dish_link.tsv"):

    print "*** 1) Downloading recipes :: get dishes and links ***"

    dish_link_list = []
    if cache is True:
        if Cache.existsCacheFile(cache_file):
            # If results are cached, return them!
            data_read = Cache.readCacheFileToList(cache_file)
            for line in data_read:
                dish = line[0]
                link = line[1]
                dish_link_list.append(DishLink(dish, link))
            return  dish_link_list
        else:
            # Results are not yet cached --> create cache file
            Cache.createCacheFile(cache_file)

    for c in ascii_lowercase:
        print "\tcomputing "+c+"..."
        soup = BeautifulSoup(crawl.crawl_page('http://www.bbc.co.uk/food/dishes/by/letter/' + c), 'html.parser')
        for s in soup.find_all('li', class_="resource food"):
            soup_link = BeautifulSoup(str(s), 'html.parser')
            dish = s.attrs['id']
            link = target + soup_link.a.attrs['href']
            dish_link_list.append(DishLink(dish, link))
    print "\t" + str(len(dish_link_list)) + " different dishes found"

    data_to_cache = []
    for dl in dish_link_list:
        data_to_cache.append([dl.dish, dl.link])
    Cache.cacheDataToFile(cache_file, data_to_cache)

    print "*** END PHASE 1 ***"
    return dish_link_list
