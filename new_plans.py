import json

if __name__ == "__main__":

    files = ["meal_plan_1691", "meal_plan_2171", "meal_plan_3296", "meal_plan_3389",
             "meal_plan_5021", "meal_plan_5322", "meal_plan_6176", "meal_plan_6282",
             "meal_plan_6335", "meal_plan_7369", "meal_plan_8902", "meal_plan_9030",
             "meal_plan_katc"]

    for filename in files:
        with open(f'./resources/{filename}.json', encoding='utf-8') as f:
            json_file = json.loads(f.read().replace('\n', ''))

        plan = json_file["DATA"]
        new_plan = {}
        tmp = []
        is_date = False
        for menu in plan:
            try:
                date = menu["dates"]
                date = int(date)
            except:
                kind_list = ["brst", "lunc", "dinr", "adspcfd"]
                is_food = [menu[kind] != "" for kind in kind_list]
                if any(is_food) and date == "" and is_date == True:
                    tmp.append(menu)
            else:
                if len(tmp) > 0:
                    new_plan[tmp[0]["dates"]] = tmp
                    tmp = []
                tmp.append(menu)
                is_date = True
        
        final_plan = {}
        for key, val in new_plan.items():
            final_plan[key] = {
                "breakfast": [],
                "lunch": [],
                "dinner": [],
                "etc": []
            }
            for menu in val:
                kind_list = [("breakfast", "brst"), ("lunch", "lunc"), 
                             ("dinner", "dinr"), ("etc", "adspcfd")]
                for i, j in kind_list:
                    foodname = menu[j]
                    if foodname == "":
                        continue
                    foodname = foodname.replace(' ', '')
                    idx = foodname.find('(')
                    if idx != -1:
                        foodname = foodname[:idx]
                    final_plan[key][i].append(foodname)
        filename = filename.split('_')[-1]
        with open(f"./newplans/new_plan_{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(final_plan, f, ensure_ascii=False, indent=2)