import os
import json
import random
import calendar

# project packages
import config


rsc_path = config.resource_path
f = open(rsc_path + 'menu.json', 'r', encoding='utf-8')
menu_json = json.load(f)
f.close()

class PlanGenerator:
    """
    annual_plan: dict, 1년 식단 {month:plan}
      month: int, (1 ~ 12)
      plan: dict, 1달 식단 {time:meal}
            time: str, (breakfast, lunch, dinner, etc)
            meal: list, 그 때의 식단 (아침, 점심, 저녁)
    """
    def __init__(self, path):
        self.annual_plan = self.preprocess(path)

    def preprocess(self, path):
        """
        연간 식단을 반환함
        월별 {[각 시간대 별 메뉴] 리스트} 딕셔너리를 반환함
        @parm:
            path: str, newplans path
        @return
            plans: dict, {month:plan}
            -> plan: dict, {time:meal}
        """
        plans = dict() # month:plan
        for month in range(1, 13):
            # plans를 월 별로 initialize
            plans[month] = {
                # 각 시간대 별로 meal list 가지고 있음
                'breakfast': list(),
                'lunch': list(),
                'dinner': list(),
                'etc': list()
                }

        for plan_file in os.listdir(path):
            # newplans 에 있는 plan.json 을 차례로 가져옴
            with open(path + plan_file, 'r', encoding='utf-8') as plan_json:
                plan = json.load(plan_json)

            for date, day_diet in plan.items():  # plan에서 날짜 별로 식단을 가져옴
                month = int(date[4:6]) # 날짜에서 month parsing 함
                # 해당 month 에 정보 추가
                for time in plans[month]: # breakfast, lunch, dinner, etc 순
                    meal = day_diet[time]
                    if not self.check_exception(meal):
                        plans[month][time].append(meal) # 예외 확인 후 메뉴 추가
                    else: #@caution-0
                        pass # TODO: days 보다 짧은 list를 반환하지 않도록 처리
        return plans

    def gen(self, path, month, year):
        """
        7, 8, 9 월에 대한 식단 생성
        @parm
            path: str, newplans 경로
            month: int, 월
            year: int, 년도
        @return
            gen_plan: dict, {날짜:메뉴}
        """
        breakfasts, lunchs, dinners, etcs = self.annual_plans

        days = calendar.monthrange(year, month)[1]
        random.shuffle(breakfasts)
        random.shuffle(lunchs)
        random.shuffle(dinners)
        random.shuffle(etcs)

        # @caution-0 : list out of index error
        # preprocess 에서 days 보다 짧은 메뉴 list 를 반환할 경우.
        plan = (
            breakfasts[:days],
            lunchs[:days],
            dinners[:days],
            etcs[:days]
            ) # 이 달의 날짜 수 만큼 slicing
        gen_plan = dict()
        for day, (breakfast, lunch, dinner, etc) in enumerate(plan):
            gen_plan[day+1] = {
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'etc': etc
            }
        return gen_plan

    def gen_by_month(self, path, month, year):
        if month in [7, 8, 9]:
            return gen(path, month, year)

        breakfasts, lunchs, dinners, etcs = self.plans
        days = calendar.monthrange(year, month)[1]
        breakfasts = breakfasts[month]
        lunchs = lunchs[month]
        dinners = dinners[month]
        etcs = etcs[month]
        random.shuffle(breakfasts)
        random.shuffle(lunchs)
        random.shuffle(dinners)
        random.shuffle(etcs)
        breakfasts = breakfasts[:days]
        lunchs = lunchs[:days]
        dinners = dinners[:days]
        etcs = etcs[:days]
        gen_plan = {}
        for i, plan in enumerate(zip(breakfasts, lunchs, dinners, etcs)):
            breakfast, lunch, dinner, etc = plan
            gen_plan[i+1] = {
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'etc': etc
        }
        return gen_plan

    @staticmethod
    def check_exception(meal):
        if len(meal) > 5:
            return True
        for food in meal:
            try:
                subname = menu_json[food]['subname']
            except:
                return True
            else:
                if subname == '#':
                    return True
                else:
                    return False
