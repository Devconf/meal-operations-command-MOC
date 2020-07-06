import mil_gen
import json
import random
from numpy import dot
from numpy.linalg import norm
import numpy as np

def add_star():
    f = open('menu.json', 'r', encoding='utf-8')
    menus = json.load(f)
    f.close()
    for menu in menus:
        menus[menu]['rate'] = random.randint(0, 5)
    return menus

def menu2vector(menu):
    return np.array(list(map(lambda x : float(x), list(menu.values())[1:8])))

def similarity(menu_a, menu_b):
    vector_a = menu2vector(menu_a)
    vector_b = menu2vector(menu_b)
    return float(dot(vector_a, vector_b)/(norm(vector_a)*norm(vector_b)))

def finder(name):
    menus = add_star()
    origin = menus[name]
    alters = list()
    for menu_name in menus:
        menu = menus[menu_name]
        if (menu['category'] == origin['category'] and
            menu['rate'] > origin['rate'] and
            similarity(menu, origin)) > float(0.8):
            alters.append(menu_name)
    return alters

if __name__ == "__main__":
    print(finder("영양밥"))