"""
연간 식단 계획을 생성함

annual_plan: list[month_info], month_info 의 리스트
    month_info: dict, {year: int, month: int, meals: list[day_info]}
        day_info: dict, {day: int, time: list[food_info]}
            (time:= breakfast, lunch, dinner, etc)
            food_info: dict, {subname: str, nutrient: float, category: str, allergy: list[int], 
                title: str, } # 추가 정보
                (nutrient:= cal, fat, protein, carbohydrate, sugar, sodium, cholesterol)
"""
import os
import json
import random
import calendar
from dietGenerator.menuCurator import MenuCurator

class PlanGenerator:
    """
    food_infos: dict, 음식 영양 정보 {food:food_info} # from menu.json
        food: str, 음식 이름
        food_info: dict, 음식 영양 정보

    raw_plan_data: dict, 1년 식단 {month:plan} # from newplans
      month: int, (1 ~ 12)
      plan: dict, 1달 식단 {time:menu_list}
            time: str, (breakfast, lunch, dinner, etc)
            menu_list: list[menu], 그 때의 식단 (아침, 점심, 저녁)
                menu: list[str], food 의 리스트
                    food: str, 음식 이름

    curator: MenuCurator,
        food_info 를 기반으로 menu를 추천해주는 모듈
    """
    def __init__(self, rsc_path='../rsc/'):
        # 영양 정보 가져오기
        with open(rsc_path + 'menu.json', 'r', encoding='utf-8') as menu_json:
            # {food:food_info} <- food_info : dict (영양 정보)
            self.food_infos = json.load(menu_json)

        plan_src_path = rsc_path + 'newplans/'
        self.raw_plan_data = self.load_plan_data(plan_src_path)
        self.curator = MenuCurator(self.food_infos)

    def load_plan_data(self, plan_src_path):
        """
        연간 식단을 반환함
        {월별 {각 시간대 별 [메뉴 리스트]}} 딕셔너리를 반환함
        @parm:
            path: str, newplans path
        @return
            raw_plan_data: dict, {month:plan}
            -> plan: dict, {time:menu list}
        """
        raw_plan_data = dict() # month:plan
        for month in range(13):
            # plans를 월 별로 initialize
            # month = 0 에는 모든 달의 menu 를 다 담음
            raw_plan_data[month] = {
                # 각 시간대 별로 menu list 가지고 있음
                'breakfast': list(),
                'lunch': list(),
                'dinner': list(),
                'etc': list()}

        for plan_src_file in os.listdir(plan_src_path):
            # newplans 에 있는 plan.json 을 차례로 가져옴
            with open(plan_src_path + plan_src_file, 'r', encoding='utf-8') as plan_json:
                raw_plan = json.load(plan_json)

            for date, day_diet in raw_plan.items():  # raw_plan 에서 날짜 별로 식단을 가져옴
                month = int(date[4:6]) # 날짜에서 month parsing 함
                # 해당 month 에 정보 추가
                for time in raw_plan_data[month]: # time := breakfast, lunch, dinner, etc
                    menu = day_diet[time]
                    if self.is_validate(menu):
                        raw_plan_data[0][time].append(menu) # 모든 month 통합
                        raw_plan_data[month][time].append(menu) # 예외 확인 후 메뉴 추가
                    else: #@caution-0
                        pass # TODO: days 보다 짧은 list를 반환하지 않도록 처리
        return raw_plan_data

    def generate_annual_plan(self, year):
        """
        최종적인 json 파일의 형태로 annual plan 만듦
        @parm:
            year: int, 년
        @return:
            annual_plan: list[monthly_plan], monthly_plan 의 리스트
                monthly_plan: dict, 해당 월의 정보
                {
                    year: int, 년
                    month: int, 월
                    meals: list[day_info], day_info 의 리스트
                        day_info: dict, 해당 일의 정보
                        {
                            day: int, 일
                            time: list[food_info], 해당 시간에 나오는 음식의 정보 (food_info) 리스트
                                time:= breakfast, lunch, dinner, etc
                                food_info: dict, 해당 음식의 정보
                                {
                                    subname: str,
                                    nutrient: float,
                                    -> (cal, fat, protein, carbohydrate, sugar, sodium, cholesterol)
                                    category: str,
                                    allergy: list[int],
                                    
                                    + 추가 정보
                                    title: str,
                                }
                        }
                }
        """
        annual_plan = list()
        for month in range(1, 13):
            # 1월 부터 12월까지 정보를 차례로 생성함
            monthly_plan = self.generate_monthly_plan(month, year)
            annual_plan.append(monthly_plan) # 월 별 계획
        return annual_plan

    def generate_monthly_plan(self, month, year):
        """
        year 년 month 월의 메뉴를 generate 함
        @parm:
            month: int, 월
            year: int, 년
        @return:
            monthly_plan: dict, {year:int, month:int, meals:monthly_diet}
                년도, 월, 그 달의 식단 계획
                monthly_diet: list[daily_plan], 날짜 별 그날의 식단 리스트
                    daily_plan: dict, {day:int, time:menu_info} 
                        날짜와 그날의 시간별 메뉴 정보
                        time:= breakfast, lunch, dinner, etc
                        menu_info: list[food_info], 해당 시간의 음식 정보들의 리스트
                            food_info: dict, 음식 정보
            -> meals의 길이 = year 년 month 의 날짜 수
        """
        # 해당 월의 날짜 수 계산 후, initialize
        days = calendar.monthrange(year, month)[1]
        monthly_plan = dict()
        monthly_plan['year'] = year
        monthly_plan['month'] = month
        monthly_diet = list()

        raw_plan = self.raw_plan_data[month] # dict {time:menu list}
        for time, menu_list in raw_plan.items():
            # time:= breakfast, lunch, dinner, etc 순서
            if len(menu_list) < days: # 날짜 수가 모자라면, 통합 plan 까지 더해줌
                plan = menu_list + self.raw_plan_data[0][time]
            else: # 날짜 수를 충족할 경우, 원래 raw_menu_list 만 반환
                plan = menu_list + list()
            
            # 가져온 data 를 섞고, slice 후, monthly plan 에 넣어줌
            random.shuffle(plan) # 순서를 무작위로 섞어줌
            for day, menu in enumerate(plan[:days]): # days 만큼 slice
                daily_plan = dict() # 해당 날의 계획
                daily_plan['day'] = day
                daily_plan[time] = self.convert_menu2info(menu) # menu_info
                monthly_diet.append(daily_plan) # 생성한 하루 식단 계획을 저장

        # 생성된 한달의 계획을 반환
        monthly_plan['meals'] = monthly_diet
        return monthly_plan

    def convert_menu2info(self, menu):
        """
        @parm
            menu: list[food], food 의 리스트
                food: str, 음식 이름
        @return
            menu_info: list[food_info], food_info 의 리스트
                food_info: dict, 영양 정보
        """
        menu_info = list()
        for food in menu:
            food_info = self.food_infos[food]
            # 추가 정보가 필요하다면, 여기서 추가 가능
            food_info['title'] = food # 이름을 추가해줌
            # rate 추가 가능 !
            menu_info.append(food_info)
        return menu_info

    def is_validate(self, menu):
        """
        @parm:
            menu: list[str], 음식 이름의 리스트
        @return:
            validate: bool, 유효할 경우 True
        """
        if len(menu) > 5:
            return False # 5 개 넘음
        for food in menu:
            try:
                subname = self.food_infos[food]['subname']
            except: # subname 없음
                return False
            else:
                if subname == '#':
                    return False
                else: # validate 함
                    return True
