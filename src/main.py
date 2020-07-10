"""
전체 프로그램을 실행하는 main
mil_gen 로 월별 식단 -> diet_gen 에 저장
add_nut 으로 연간 영양소 계획 -> annual_diet 에 저장
"""
import json

# project packages
from dietGenerator.plan_generator import PlanGenerator # pylint: disable=import-error
from dataGenerator.newplanGenerator import NewPlanGenerator # pylint: disable=import-error

def save_annual_diet(result_path, year, annual_plan):
    with open(result_path + f'annual_diet/{year}년_식단.json', 'w', encoding='utf-8') as annual_json:
        json.dump(annual_plan, annual_json, ensure_ascii=False, indent=2)

def make_newplans():
    newplan_generator = NewPlanGenerator()
    newplan_generator.generate_new_plan()

if __name__ == "__main__":
    YEAR = 2020
    RESULT_PATH = '../result/'
    plan_generator = PlanGenerator()
    ANNUAL_PLAN = plan_generator.generate_annual_plan(YEAR)  # 연간 계획 생성
    save_annual_diet(RESULT_PATH, YEAR, ANNUAL_PLAN) # json 으로 저장

    FOOD = '핫도그빵'
    print(FOOD)
    print(plan_generator.curator.find_similar_foods(FOOD))
