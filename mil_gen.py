import os
import json
import random
import calendar

def preprocessed(path):
    breakfasts, lunchs, dinners = [], [], []
    for filename in os.listdir(path):
        with open(path+filename, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        for _, val in plan.items():
            breakfasts.append(val['breakfast'])
            lunchs.append(val['lunch'])
            dinners.append(val['dinner'])
    return breakfasts, lunchs, dinners

def preprocessed_by_month(path):
    breakfasts, lunchs, dinners = {}, {}, {}
    for i in range(1, 13):
        breakfasts[i] = []
        lunchs[i] = []
        dinners[i] = []
    for filename in os.listdir(path):
        with open(path+filename, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        for key, val in plan.items():
            month = int(key[4:6])
            breakfasts[month].append(val['breakfast'])
            lunchs[month].append(val['lunch'])
            dinners[month].append(val['dinner'])
    return breakfasts, lunchs, dinners

def gen(path, month, year):
    breakfasts, lunchs, dinners = preprocessed(path)
    days = calendar.monthrange(year, month)[1]
    random.shuffle(breakfasts)
    random.shuffle(lunchs)
    random.shuffle(dinners)
    breakfasts = breakfasts[:days+1]
    lunchs = lunchs[:days+1]
    dinners = dinners[:days+1]
    gen_plan = {}
    for i, plan in enumerate(zip(breakfasts, lunchs, dinners)):
        breakfast, lunch, dinner = plan
        gen_plan[f'{i+1}일'] = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner
        }
    return gen_plan

def gen_by_month(path, month, year):
    if month in [7, 8, 9]:
        return gen(path, month, year)
    breakfasts, lunchs, dinners = preprocessed_by_month(path)
    days = calendar.monthrange(year, month)[1]
    breakfasts = breakfasts[month]
    lunchs = lunchs[month]
    dinners = dinners[month]
    random.shuffle(breakfasts)
    random.shuffle(lunchs)
    random.shuffle(dinners)
    breakfasts = breakfasts[:days]
    lunchs = lunchs[:days]
    dinners = dinners[:days]
    gen_plan = {}
    for i, plan in enumerate(zip(breakfasts, lunchs, dinners)):
        breakfast, lunch, dinner = plan
        gen_plan[f'{i+1}일'] = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner
    }
    return gen_plan

if __name__ == "__main__":
    path = './newplans/'
    month, year = 7, 2020
    plan = gen_by_month(path, month, year)
    with open(f'{year}년{month}월_식단.json', 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)