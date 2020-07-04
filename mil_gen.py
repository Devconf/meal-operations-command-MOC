import os
import json
import random
import calendar
import add_nut

f = open('menu.json', 'r', encoding='utf-8')
menu_json = json.load(f)
f.close()

def check_exception(meal):
    for food in meal:
        try:
            subname = menu_json[food]['subname']
        except:
            return True
        else:
            if subname == '#':
                return True
            else:
                return False

def preprocessed(path):
    breakfasts, lunchs, dinners, etcs = [], [], [], []
    for filename in os.listdir(path):
        with open(path+filename, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        for _, val in plan.items():
            variables = [breakfasts, lunchs, dinners, etcs]
            strings = ['breakfast', 'lunch', 'dinner', 'etc']
            for v, s in zip(variables, strings):
                meal = val[s]
                if not check_exception(meal):
                    v.append(meal)
    return breakfasts, lunchs, dinners, etcs

def preprocessed_by_month(path):
    breakfasts, lunchs, dinners, etcs = {}, {}, {}, {}
    for i in range(1, 13):
        breakfasts[i] = []
        lunchs[i] = []
        dinners[i] = []
        etcs[i] = []
    for filename in os.listdir(path):
        with open(path+filename, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        for key, val in plan.items():
            month = int(key[4:6])
            variables = [breakfasts, lunchs, dinners, etcs]
            strings = ['breakfast', 'lunch', 'dinner', 'etc']
            for v, s in zip(variables, strings):
                meal = val[s]
                if not check_exception(meal):
                    v[month].append(meal)
    return breakfasts, lunchs, dinners, etcs

def gen(path, month, year):
    breakfasts, lunchs, dinners, etcs = preprocessed(path)
    days = calendar.monthrange(year, month)[1]
    random.shuffle(breakfasts)
    random.shuffle(lunchs)
    random.shuffle(dinners)
    random.shuffle(etcs)
    breakfasts = breakfasts[:days]
    lunchs = lunchs[:days]
    dinners = dinners[:days]
    etcs = etcs[:days]
    gen_plan = {}
    for i, plan in enumerate(zip(breakfasts, lunchs, dinners, etcs)):
        breakfast, lunch, dinner, etc = plan
        gen_plan[f'{i+1}'] = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'etc': etc
        }
    return gen_plan

def gen_by_month(path, month, year):
    if month in [7, 8, 9]:
        return gen(path, month, year)
    breakfasts, lunchs, dinners, etcs = preprocessed_by_month(path)
    days = calendar.monthrange(year, month)[1]
    breakfasts = breakfasts[month]
    lunchs = lunchs[month]
    dinners = dinners[month]
    etcs = etcs[month]
    random.shuffle(breakfasts)
    random.shuffle(lunchs)
    random.shuffle(dinners)
    random.shuffle(etcs)
    breakfasts = breakfasts[:days]
    lunchs = lunchs[:days]
    dinners = dinners[:days]
    etcs = etcs[:days]
    gen_plan = {}
    for i, plan in enumerate(zip(breakfasts, lunchs, dinners, etcs)):
        breakfast, lunch, dinner, etc = plan
        gen_plan[f'{i+1}'] = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'etc': etc
    }
    return gen_plan


if __name__ == "__main__":
    path = './newplans/'
    year = 2020
    for month in range(1,13):
        plan= gen_by_month(path, month, year)
        with open(f'./diet_gen/{year}년{month}월_식단.json', 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)

    annual_plan=add_nut.add_nutrient(year,menu_json)
    with open(f'./annual_diet/{year}년_식단.json', 'w', encoding='utf-8') as f:
            json.dump(annual_plan, f, ensure_ascii=False, indent=2)
    
