import os
import json

if __name__ == "__main__":
    breakfasts, lunchs, dinners = {}, {}, {}
    for i in range(1, 13):
        breakfasts[i] = []
        lunchs[i] = []
        dinners[i] = []
    
    path = './newplans/'
    for filename in os.listdir(path):
        with open(path+filename, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        for key, val in plan.items():
            month = int(key[4:6])
            breakfasts[month].append(val['breakfast'])
            lunchs[month].append(val['lunch'])
            dinners[month].append(val['dinner'])

    for key, val in breakfasts.items():
        print(key, len(val))