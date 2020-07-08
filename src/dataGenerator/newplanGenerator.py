import os
import json

class NewPlanGenerator:
    def __init__(self, rsc_path='../rsc/'):
        self.times = { # convert raw data 의 이름 -> new data 이름
            "brst":"breakfast",
            "lunc":"lunch",
            "dinr":"dinner",
            "adspcfd":"etc"}
        meal_plan_path = rsc_path + 'rawdata/'
        self.new_plan_path = rsc_path + 'newplans/'
        self.raw_plans = self.load_raw_plans(meal_plan_path)

    def load_raw_plans(self, meal_plan_path):
        raw_plans = dict()
        for meal_plan_file in os.listdir(meal_plan_path):
            with open(meal_plan_path + meal_plan_file, 'r', encoding='utf-8') as meal_plan_json:
                raw_data = json.loads(meal_plan_json.read().replace('\n', ''))
                plan = raw_data["DATA"]

            identifier = meal_plan_file.split('_')[-1] # identifier 만 가져옴
            raw_plans[identifier] = self.filter_validate(plan)
        return raw_plans

    def generate_new_plan(self):
        for identifier, raw_plan in self.raw_plans.items():
            new_plan = dict()
            for date, menus in raw_plan.items():
                new_plan[date] = {
                    "breakfast": list(),
                    "lunch": list(),
                    "dinner": list(),
                    "etc": list()}
                for menu in menus:
                    for time in self.times:
                        food_name = self.clean_food_name(menu[time])
                        if food_name: # 음식이름 존재, 추출 성공
                            new_plan[date][self.times[time]].append(food_name)

            with open(self.new_plan_path + f"new_plan_{identifier}.json",
                'w', encoding='utf-8') as new_plan_file:
                json.dump(new_plan, new_plan_file, ensure_ascii=False, indent=2)

    def filter_validate(self, plan):
        validate_plan = dict()
        is_date = False

        menus = list()
        for daily_plan in plan:
            try:
                # date 정보를 가지고 있는 경우
                date = int(daily_plan["dates"])
            except ValueError:
                has_data = list(daily_plan[time] != "" for time in self.times)
                if any(has_data) and (not date) and is_date:
                    menus.append(daily_plan)
            else:
                if menus:
                    date = menus[0]["dates"]
                    validate_plan[date] = menus
                    menus = []
                menus.append(daily_plan)
                is_date = True
        return validate_plan

    @staticmethod
    def clean_food_name(food_name):
        if not food_name:
            return None
        food_name = food_name.replace(' ', '')
        idx = food_name.find('(')
        if idx != -1: # 알레르기 정보 이전까지만 가져옴
            food_name = food_name[:idx]
        return food_name
