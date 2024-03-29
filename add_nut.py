import json

def add_nutrient(year,menu_json):
    annual_diet=[]
   
    
    for month in range(1,13):
        month_diet={}
        with open(f'./diet_gen/{year}년{month}월_식단.json', 'r', encoding='utf-8') as f:
            month_meal= json.loads(f.read().replace("\n",""))
            f.close()
            month_diet["year"]=year
            month_diet["month"]=month
            month_diet["meals"]=[]
            for key,val in month_meal.items():
                meal={}
                meal["day"]=int(key)
                for k,v in val.items():
                    meal[k]=[]
                    for menu in v: 
                        for m_k,m_v in menu_json.items():
                            if menu ==m_k:
                                m_v["title"]=menu
                                for nutrient in ['sodium', 'cholesterol']:
                                    m_v[nutrient] = m_v[nutrient]/1000
                                meal[k].append(m_v)
                                break
  
                month_diet["meals"].append(meal) 
        annual_diet.append(month_diet)
    return annual_diet