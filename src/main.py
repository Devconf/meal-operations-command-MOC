"""
전체 프로그램을 실행하는 main
mil_gen 로 월별 식단 -> diet_gen 에 저장
add_nut 으로 연간 영양소 계획 -> annual_diet 에 저장
"""
import json

# project packages
from dietGenerator.planGenerator import PlanGenerator

def save_annual_diet(result_path, year, annual_plan):
    with open(
        result_path + f'annual_diet/{year}년_식단.json',
        'w', encoding='utf-8') as annual_meal:
        json.dump(annual_plan, annual_meal, ensure_ascii=False, indent=2)

def make_newplans():
    newplan_generator = NewPlanGenerator()
    newplan_generator.generate_new_plan()

if __name__ == "__main__":
    year = 2020
    result_path = '../result/'
    plan_generator = PlanGenerator()
    annual_plan = plan_generator.generate_annual_plan(year)  # 연간 계획 생성
    save_annual_diet(result_path, year, annual_plan) # json 으로 저장

    food = '핫도그빵'
    print(food)
    print(plan_generator.curator.find_similar_foods(food))
