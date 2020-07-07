"""
전체 프로그램을 실행하는 main
mil_gen 로 월별 식단 -> diet_gen 에 저장
add_nut 으로 연간 영양소 계획 -> annual_diet 에 저장
"""
import json

# project packages
import config
from dietGenerator import mil_gen
from dietGenerator import add_nut

if __name__ == "__main__":
    year = config.year
    path = config.newplans_path
    result_dst = config.result_path

    for month in range(1,13):
        # 1월 부터 12월 까지 식단 생성
        plan= mil_gen.gen_by_month(path, month, year)
        with open(result_dst + f'diet_gen/{year}년{month}월_식단.json', 'w', encoding='utf-8') as monthly_meal:
            json.dump(plan, monthly_meal, ensure_ascii=False, indent=2)

    annual_plan=add_nut.add_nutrient(year, mil_gen.menu_json)
    with open(result_dst + f'annual_diet/{year}년_식단.json', 'w', encoding='utf-8') as annual_meal:
        # 연간 계획 생성
        json.dump(annual_plan, annual_meal, ensure_ascii=False, indent=2)