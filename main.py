import mil_gen
import add_nut
import json

if __name__ == "__main__":
    path = './newplans/'
    year = 2020
    for month in range(1,13):
        plan= mil_gen.gen_by_month(path, month, year)
        with open(f'./diet_gen/{year}년{month}월_식단.json', 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)

    annual_plan=add_nut.add_nutrient(year,mil_gen.menu_json)
    with open(f'./annual_diet/{year}년_식단.json', 'w', encoding='utf-8') as f:
            json.dump(annual_plan, f, ensure_ascii=False, indent=2)