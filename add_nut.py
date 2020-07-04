import json

def add_nutrient(year,menu_json):
    annual_diet=[]
    month_diet={}
    
    for month in range(1,13):
        with open(f'./diet_gen/{year}년{month}월_식단.json', 'r', encoding='utf-8') as f:
            month_meal= json.loads(f.read().replace("\n",""))
            f.close()
            for key,val in month_meal.items():
                new_menu={}
                for k,v in val.items():
                    for menu in v:
                        for m_k,m_v in menu_json.items():
                            if menu ==m_k:
                                new_menu[menu]=m_v
                                break
                    val[k]=new_menu
            month_diet[month]=month_meal
    annual_diet.append(month_diet)
    return annual_diet