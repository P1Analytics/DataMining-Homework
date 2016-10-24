#encoding=utf-8

import excercise_4.util.util as util

''' title, who wrote it, preparation time,   cooking itme,     number of people it serves, dietary information, ingredients,          method'''
features = ["title","link", "author", "prep_time", "cook_time", "num_people_serves", "diet_inf", "ingredients", "method"]

class Recipe(object):
    def __init__(self, title, link, **features):
        self.title = title
        self.link = link
        for feature, value in features.iteritems():
            if feature == "ingredients":
                ingredients = value
                if isinstance(value, basestring):
                # ingredientrs is a string that has the form: [r1:[x1, y1, z1]r2:[x2, y2, z2] ...] --> dic (r, list of ingr)
                    ingredients = {}
                    if value != "[]" and value!="-1":
                        sub_recipes = value[1:-2].split("]")
                        for sub_recipe in sub_recipes:
                            sub_recipe_name = sub_recipe.split(":")[0]
                            sub_recipe_ingr = []
                            for ingr in sub_recipe.split(":")[1][1:].split(","):
                                sub_recipe_ingr.append(ingr.strip())
                            ingredients[sub_recipe_name] = sub_recipe_ingr
                setattr(self, feature, ingredients)
            elif feature == "method":
                method = value
                if isinstance(value, basestring):
                    # ingredientrs is a string that has the form: [r1:[x1, y1, z1]r2:[x2, y2, z2] ...] --> dic (r, list of ingr)
                    method = []
                    if value != "-1":
                        method = value.split("||")
                setattr(self, feature, method)
            else:
                setattr(self, feature, value)
    ''' try do define a smarter constructor
    def __init__(self,title,link,
                 author,
                 prep_time,
                 cook_time,
                 num_people_serves,
                 diet_inf,
                 ingredients,
                 method):
        self.title=title
        self.link=link
        self.author=author,
        self.prep_time=prep_time,
        self.cook_time=cook_time,
        self.num_people_serves=num_people_serves,
        self.diet_inf=diet_inf,
        self.ingredients=ingredients,
        self.method=method
    '''

    def __str__(self):
        res = ""
        for feature in features:
            try:
                attr = getattr(self, feature, "-1")
                if type(attr) is list:
                    res += util.remove_separator_char(util.get_utf8_string('||'.join(attr)))+"\t"
                elif type(attr) is dict:
                    res+="["
                    for sub_recipe, sub_recipe_ingr in attr.iteritems():
                        sub_recipe = util.get_utf8_string(sub_recipe)
                        sub_recipe_ingr = util.get_utf8_string(', '.join(sub_recipe_ingr))
                        res+=util.remove_separator_char((sub_recipe+":["+sub_recipe_ingr+"]"))
                    res += "]\t"
                else:
                    res = res + util.get_utf8_string(attr)+"\t"
            except AttributeError as a:
                print a
                continue
        return res