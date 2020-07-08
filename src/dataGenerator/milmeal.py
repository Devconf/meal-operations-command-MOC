import json
import csv
import re

class Menu :
    def __init__(self, name, cal, category):
        self.name = name
        self.subname = ""
        self.cal = cal
        self.fat = 0.0
        self.protein = 0.0
        self.carbohydrate = 0.0
        self.sugar=0.0
        self.sodium=0.0
        self.cholesterol=0.0
        self.allergy = []
        self.category = ""
        if category == "adspcfd":
            self.category = "부식"

def menuCheck(json_data, menuInfo):
    for dailyMenu in json_file["DATA"] :
        for kinds in ["brst", "lunc", "dinr", "adspcfd"]:
            check = "false"
            foodName = dailyMenu[kinds]
            foodName = foodName.replace(' ', '')
            idx = foodName.find('(')
            if idx != -1:
                foodName = foodName[:idx]
            for menu in menuInfo :
                if menu.name == foodName :
                    check = "true"
            if check == "false" :
                temp = Menu(foodName, dailyMenu[kinds + "_cal"], kinds)
                for i in range (1, 19) :
                    if dailyMenu[kinds].find(f'({i})') != -1:
                        temp.allergy.append(i)
                if temp.name != "":
                    menuInfo.append(temp)

def map_subname(menuInfo, csv_subname_db):
    subname_dict = {}
    for name, subname, etc in csv_subname_db:
        if "/" not in etc:
            subname_dict[name] = subname
        else:
            subname_dict[name] = "#"
    for menu in menuInfo:
        menu.subname = menu.name
        if menu.name in subname_dict.keys():
            menu.subname = subname_dict[menu.name]

def calc_nutrient(menuInfo, csv_nut_db):
    nut_infos = []
    for info in csv_nut_db:
        nut_infos.append(info)
    for menu in menuInfo:
        for info in nut_infos:
            if menu.subname == info[0] and menu.subname != "#":
                cal = "0" + re.sub('[^\d\.]', '', info[6])
                menu.cal = float("0" + re.sub('[^\d\.]', '', menu.cal))
                info[7] = "0" + re.sub('[^\d\.]', '', info[7])
                info[8] = "0" + re.sub('[^\d\.]', '', info[8])
                info[9] = "0" + re.sub('[^\d\.]', '', info[9])
                info[10] = "0" + re.sub('[^\d\.]', '', info[10])
                info[11] = "0" + re.sub('[^\d\.]', '', info[11])
                info[12] = "0" + re.sub('[^\d\.]', '', info[12])
                #print( info[7]+" "+ info[8]+" "+ info[9]+" "+ info[10])
                if(float(cal) == 0 or menu.cal == 0):
                    break
                if info[7] != '-':
                    menu.protein = float(info[7]) * menu.cal / float(cal)
                if info[8] != '-':
                    menu.fat = float(info[8]) * menu.cal / float(cal)
                if info[9] != '-':
                    menu.carbohydrate = float(info[9]) * menu.cal / float(cal)
                if info[10] != '-':
                    menu.sugar = float(info[10]) * menu.cal / float(cal)
                if info[11] != '-':
                    menu.sodium = float(info[11]) * menu.cal / float(cal)
                if info[12] != '-':
                    menu.cholesterol = float(info[12]) * menu.cal / float(cal)
                break
            elif menu.subname == "#":
                menu.cal = float("0" + re.sub('[^\d\.]', '', menu.cal))
                menu.carbohydrate = 0
                menu.protein = 0
                menu.fat = 0
                menu.sugar=0
                menu.sodium=0
                menu.cholesterol=0
                break

def save_as_json(menuInfo):
    dic = {}
    for menu in menuInfo:
        dic[menu.name] = {
            "subname": menu.subname,
            "cal": menu.cal,
            "fat": menu.fat,
            "protein": menu.protein,
            "carbohydrate": menu.carbohydrate,
            "sugar": menu.sugar,
            "sodium": menu.sodium,
            "cholesterol" : menu.cholesterol,
            "category": menu.category,
            "allergy": menu.allergy
        }

    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=2)

def category_selector(name):
    cat_table = ['밥','국','메인','서브','버거','김치','면','예외']
    for i in cat_table:
        if i[0] == name[0]:
            return i

def fill_category(menuInfo,category_infos):
    category_infos[0][0] = category_infos[0][0].replace('\ufeff', '')
    for menu in menuInfo:
        for category in category_infos:
            if menu.name == category[0]:
                menu.category=category_selector(category[1])

if __name__ == "__main__":

    plans = ["meal_plan_1691", "meal_plan_2171", "meal_plan_3296", "meal_plan_3389",
             "meal_plan_5021", "meal_plan_5322", "meal_plan_6176", "meal_plan_6282",
             "meal_plan_6335", "meal_plan_7369", "meal_plan_8902", "meal_plan_9030",
             "meal_plan_katc"]

    menuInfo = []
    category_infos=[]

    for filename in plans:
        f = open(f'./resources/{filename}.json', encoding='utf-8')
        json_file = json.loads(f.read().replace('\n', ''))
        f.close()
        menuCheck(json_file, menuInfo)

    subname_db = open("./resources/subname_db_20200621.csv", "r", newline="", encoding='utf-8')
    csv_subname_db = csv.reader(subname_db)
    map_subname(menuInfo, csv_subname_db)

    nut_db = open("./resources/nutrient_db_20200625-1.csv", "r", newline="", encoding='utf-8')
    csv_nut_db = csv.reader(nut_db)
    calc_nutrient(menuInfo, csv_nut_db)

    category_db = open("./resources/menu_category.csv","r",newline="",encoding='utf-8')
    csv_category_db =csv.reader(category_db)
    for info in csv_category_db:
        category_infos.append(info)

    fill_category(menuInfo,category_infos)

    save_as_json(menuInfo)