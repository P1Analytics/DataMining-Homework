# encoding=utf-8

from bs4 import BeautifulSoup
from excercise_4.application import crawl
from excercise_4.data import data_manager


def start(crawl_again=False, **recipes_dic):
    print "*** Start Preprocessing recipes ***"

    # 1
    store_information(recipes_dic)

''' 1) Parse the web page, and get data! '''
def store_information(recipes_dic):
    print "*** 1) Preprocessing :: crawl web page and get data ***"
    recipe_error_dic = {}
    for link, recipe in recipes_dic.iteritems():
        num_attempt = 5
        print "\tParsing " + link
        while num_attempt > 0:
            print "\t\tAttempt no: " + str(6 - num_attempt)
            soup = BeautifulSoup(crawl.crawl_page(link), 'html.parser')
            try:
                # chef name
                getting = "chef name"
                chef_name = ""
                try:
                    chef_name = soup.find("div", class_="chef__name").a.contents[0]
                except:
                    pass
                recipe.author = chef_name

                # preparation time
                getting = "preparation time"
                prep_time = soup.find("p", class_="recipe-metadata__prep-time").contents[0]
                recipe.prep_time = prep_time

                # cook_time
                getting = "cook_time"
                cook_time = soup.find("p", class_="recipe-metadata__cook-time").contents[0]
                recipe.cook_time = cook_time

                # num people serves
                getting = "num people serves"
                num_people_serves = ""
                try:
                    num_people_serves = soup.find("p", class_="recipe-metadata__serving").contents[0]
                except:
                    pass
                recipe.num_people_serves = num_people_serves

                # dietary inf
                getting = "dietary inf"
                diet_inf = ""
                try:
                    dietary_div = soup.find("div", class_="recipe-metadata__dietary")
                    dietaries = dietary_div.find_all("a")
                    for dietary in dietaries:
                        diet_inf+=str(dietary.find("p").contents[0]).strip()+" "
                except:
                    pass
                recipe.diet_inf = diet_inf

                # ingredients
                getting = "ingredients"
                ingredients = {}
                ingredients_div = soup.find("div", class_="recipe-ingredients-wrapper")
                sub_recipe_list_h3 = ingredients_div.find_all("h3", class_="recipe-ingredients__sub-heading")
                sub_recipe_ingr_ul = ingredients_div.find_all("ul", class_="recipe-ingredients__list")
                for i in range(0, len(sub_recipe_list_h3)):
                    sub_recipe_name = sub_recipe_list_h3[i].contents[0]
                    sub_recipe_ingr = []
                    for ingredient_li in sub_recipe_ingr_ul[i].find_all("li"):

                        # an li tag can contains: "p1"<a href....>"p2"</a>"p3" --> our final string must be "p1 p2 p3 .."
                        plaintext_ingredient = ""
                        for ingredient_part_of_li in ingredient_li.contents:
                            if isinstance(ingredient_part_of_li, basestring):
                                # row txt
                                plaintext_ingredient += ingredient_part_of_li.strip()+" "
                            else:
                                # link --> get content
                                 plaintext_ingredient += ingredient_part_of_li.contents[0]

                        sub_recipe_ingr.append(plaintext_ingredient)
                    ingredients[sub_recipe_name] = sub_recipe_ingr
                recipe.ingredients = ingredients

                # method
                getting = "method"
                method = []
                method_list_li = soup.find_all("li", class_="recipe-method__list-item")
                for li in method_list_li:
                    method.append(li.p.contents[0].strip())
                recipe.method = method

            except Exception as e:
                print "\t\t*WARNING* error(" + e.__str__() + ") during try to get " + str(getting)
                num_attempt = num_attempt - 1
                continue
            break

        if num_attempt == 0:
            recipe_error_dic[link] = recipe

        data_manager.saveRecipe(recipe)
    data_manager.close_open_file()
    data_manager.save_error_pages(**recipe_error_dic)