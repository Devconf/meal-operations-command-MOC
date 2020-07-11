"""
new_plan 을 생성
"""
import os
import json

class NewPlanGenerator:
    """
    meal_plan 으로 new_plan 만듦
    """
    def __init__(self, rsc_path='../../rsc/'):
        self.times = { # convert raw data 의 이름 -> new data 이름
            "brst":"breakfast",
            "lunc":"lunch",
            "dinr":"dinner",
            "adspcfd":"etc"}
        meal_plan_path = rsc_path + 'rawdata/'
        self.new_plan_path = rsc_path + 'newplans/'
        self.raw_plans = self.load_raw_plans(meal_plan_path)

    def load_raw_plans(self, meal_plan_path):
        """
        @parm:
            meal_plan_path: str, 공공데이터인 meal_plan 의 path
        @return
            raw_plans: dict, {identifier,raw_plan}
                raw_plan: dict, {date:infos}
                    date: str, YYYYMMDD 형식의 날짜 문자열
                    infos: list[info], info 들의 list
                        info: dict, meal_plan 에 들어있는 개별 정보 단위
        """
        raw_plans = dict()
        for meal_plan_file in os.listdir(meal_plan_path):
            with open(meal_plan_path + meal_plan_file, 'r', encoding='utf-8') as meal_plan_json:
                raw_data = json.loads(meal_plan_json.read().replace('\n', ''))
                """
                raw_data: dict, {DESCRIPTION: info_scheme, DATA: list[info]}
                    info_scheme: dict, {
                                    "dates": "날짜",
                                    "brst": "조식",
                                    "brst_cal": "조식열량",
                                    "lunc": "중식",
                                    "lunc_cal": "중식열량",
                                    "dinr": "석식",
                                    "dinr_cal": "석식열량",
                                    "adspcfd": "증특식",
                                    "adspcfd_cal": "증특식열량",
                                    "sum_cal": "열량합계"
                                }
                    info: dict, info_scheme 를 따름
                        단, 하루의 식단이 여러개의 info 로 쪼개져 있음.
                        하루의 식단 <- info 의 누적 
                            from (dates에 값 존재하는 info 등장) 
                            until (dates에 값 존재하는 info 새로 등장)
                        parsing 필요 => self.filter_validate
                """
                meal_plan = raw_data["DATA"]

            identifier = meal_plan_file.split('_')[-1] # identifier 만 가져옴
            raw_plans[identifier] = self.filter_validate(meal_plan)
        return raw_plans

    def generate_new_plan(self):
        """
        @parm:
            self.
            raw_plans: dict, {identifier,raw_plan}
                raw_plan: dict, {date:infos}
                    date: str, YYYYMMDD 형식의 날짜 문자열
                    infos: list[info], info 들의 list
                        info: dict, {time:food} meal_plan 에 들어있는 개별 정보 단위
                            food: str, 음식 이름
                            *각각의 info의 각 time 에는 최대 1개의 food 가 있음
        """
        for identifier, raw_plan in self.raw_plans.items():
            # meal_plan_<identifier> 에서 <identifier> 를
            # new_plan_<identifier> 에 사용
            new_plans = dict()
            for date, infos in raw_plan.items():
                new_plan = {
                    "breakfast": list(),
                    "lunch": list(),
                    "dinner": list(),
                    "etc": list()}
                for info in infos:
                    for time in self.times: # brst, lunc, dinr, adspcfd
                        food_name = self.clean_food_name(info[time])
                        if food_name: # 음식이름 존재, 추출 성공
                            new_plan[date][self.times[time]].append(food_name)
                            # info 별로 최대 음식 1개의 이름을 가지고 있으므로, 계속 누적
                
                # 누적된 식단을 날짜에 맞춰 저장
                new_plans[date] = new_plan

            # 최종 결과를 json file 로 저장
            with open(self.new_plan_path + f"new_plan_{identifier}.json",
                'w', encoding='utf-8') as new_plan_file:
                json.dump(new_plans, new_plan_file, ensure_ascii=False, indent=2)

    def filter_validate(self, plan):
        """
        @parm:
            plan: list[info]
        @return:
            raw_plan: dict, {date:infos}
                date: str, YYYYMMDD 형식의 날짜 문자열
                infos: list[info], info 들의 list
                    info: dict, meal_plan 에 들어있는 개별 정보 단위
                    각 info 의 각 time 에는 최대 1개의 음식 이름 존재
                    dates 는 head_info 만 가지고 있고, 같은 날의 다른 info 는 갖고 있지 않음
                    따라서 
                        dates 에 값이 처음 등장하고, 
                        다음으로 dates 가 등장할 때 까지
                    하루의 식단으로 취급
        """
        time_list = ["brst", "lunc", "dinr", "adspcfd"]
        raw_plan = dict()

        is_date = False
        temp_infos = list() # 임시 누적용 list
        for info in plan:
            try:
                date = int(info["dates"])
                # 성공시 else 로 이동
            except:
                # info["dates"] 를 int 로 변환 실패
                is_food = any([info[time] != "" for time in time_list])
                if is_date == True and is_food and not info["dates"]:
                    # date를 가지고 있는 head_info 없이는 누적하지 않음,
                    # 아침, 점심, 저녁, 부식 중 하나라도 정보를 가지고 있어야 함,
                    # dates 에 아무런 내용도 없어야 함
                    temp_infos.append(info) # 임시 list 에 넣어둠
            else:
                # date 가 있고,
                is_date = True
                if len(temp_infos) > 0: # temp_infos 가 비어 있지 않다면
                    raw_plan[temp_infos[0]["dates"]] = temp_infos # 첫 번째로 들어간 info 의 날짜로 temp_infos 넣어줌
                    temp_infos = [] # temp_infos 를 비움
                temp_infos.append(info) # dates를 가지고 있는 info 가 항상 첫 번째로 들어감
                                        # case 1. len(temp_infos) == 0 -> 처음으로 날짜를 가진 info 들어감, (head_info)
                                        # case 2. len(temp_infos) > 0 누적 된 info 를 넣어주고, temp_infos를 다시 비움
        return raw_plan

    @staticmethod
    def clean_food_name(food_name):
        """
        meal_plan 안의 음식 이름이 옴,
        음식 이름 뿐 아니라, 다른 정보가 있음
        parsing 필요함
        -> 이후 checker 를 통해 다시 작업할 필요 있음
        """
        if not food_name:
            return None
        food_name = food_name.replace(' ', '')
        idx = food_name.find('(')
        if idx != -1: # 알레르기 정보 이전까지만 가져옴
            food_name = food_name[:idx]
        return food_name

if __name__ == "__main__":
    newplan_generator = NewPlanGenerator()
    newplan_generator.generate_new_plan()
