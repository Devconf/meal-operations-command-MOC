"""
data 의 유효성 검증하고,
요효하게 수정함.
"""
import os
import json
from correct import black_lists

class Checker:
    """
    menulist.json
    newplans/new_plan_*.json
    두 data 의 유효성을 검증하고, 수정함
    """
    def __init__(self):
        self.rsc_path = '../'

        self.food_infos = dict()
        self.food_hits = dict()
        menulist_path = self.rsc_path + 'menulist.json'
        with open(menulist_path, 'r', encoding='utf-8') as menulist_json:
            # {food:food_info} <- food_info : dict (영양 정보)
            raw_food_infos = json.load(menulist_json)
            for food_info in raw_food_infos:
                food = food_info['title'] # 음식 이름
                self.food_infos[food] = food_info
                self.food_hits[food] = 0

    def check_start(self):
        """
        함수 호출 여부를 수정하여, (주석 처리)
        어떤 유효성을 검증할 지 선택할 수 있음
        """
        # 가장 먼저, black list 에 있는 이름을 가진
        # 음식 정보가 menulist에 등록되어 있는 확인
        self.food_name_check()

        # menulist 안에 있는 정보들이 올바른지 확인
        self.food_info_type_check() # type 먼저 체크
        self.food_info_numeric_check()

        # newplans 안에 있는 음식 이름들을 확인
        self.newplan_menu_check()
        self.newplan_food_name_match()

    def food_name_check(self):
        """
        menulist 안에 있는 음식들의 이름이
        black list (remove, refine) 안에 있지 않은지 확인 후, 수정
        """
        removes = black_lists.removes
        refines = black_lists.refines

        for food in removes:
            if food in self.food_infos:
                self.food_infos.pop(food)

        for food in refines:
            if food in self.food_infos:
                food_info = self.food_infos.pop(food)
                rename = refines[food]
                food_info['title'] = rename
                self.food_infos[rename] = food_info

        fails = list()
        for food in self.food_infos:
            if food in removes or food in refines:
                fails.append(food)

        if fails:
            print('E: Food name check\n', fails)
        else:
            print("menulist food name check SUCCESS")
        self.save_json('../menulist.json', list(self.food_infos.values()))
        return self.find_black_list()

    def find_black_list(self):
        """
        black list에 올라갈 가능성이 있는 음식 이름들을 찾아줌
        Error 가 아닌 Warning
        """
        black_list = ['임시', ',', 'g', '/', '?'] + list(map(str, range(0,10)))
        warning_names = list()
        for food in self.food_infos:
            for black_word in black_list:
                if food.find(black_word) > -1:
                    # black list 내의 word를 포함한다면
                    print("W: Food Name", food, "|", black_word)
                    warning_names.append(food)
                    break        
        return warning_names

    def food_info_type_check(self):
        """
        food info 의 type scheme 에 따라
        type에 맞게 정보가 들어있는지 확인
        """
        wrong_types = list()
        type_scheme = black_lists.type_scheme
        rate_type_scheme = black_lists.rate_type_scheme

        num_keys = len(type_scheme)
        for food, food_info in self.food_infos.items():
            validate = True
            if len(food_info) != num_keys:
                validate = False
                print("E: Keynum", food)
            else:
                for info in food_info:
                    if not isinstance(food_info[info], type_scheme[info]):
                        if type_scheme[info] == float and isinstance(food_info[info], int):
                            if food_info[info]: # 0이 아님
                                food_info[info] = float(food_info[info])
                                print('E: Not float', info, food, food_info[info])
                        else:
                            validate = False
                            print("E: Keytype", info, food)
                for rate_infos in food_info['rates']:
                    for rate_info in rate_infos:
                        if not isinstance(rate_infos[rate_info], rate_type_scheme[rate_info]):
                            validate = False
                            print("E: Rate Keytype", info, food)

            if not validate:
                wrong_types.append(food)

        if wrong_types:
            self.save_json('correct/menulist.json', list(self.food_infos.values()))
        if wrong_types:
            print(wrong_types)
        else:
            print("Wrong Type SUCCESS")
        return wrong_types

    def food_info_numeric_check(self):
        """
        음식 정보 중, 숫자 정보를 가지는 속성들에 대해,
        - float 인 경우, 소수점 둘째 자리 까지 반올림
        - 0 인 경우, float 0.0 이 아닌 int 0 으로
        """
        numerics = ["cal", "fat", "protein", "carbohydrate", "sugar", "sodium", "cholesterol"]
        for food, food_info in self.food_infos.items():
            for info in numerics:
                food_info[info] = round(food_info[info], 2)
                if not food_info[info]:
                    # 0.0 인 경우, 0 으로 넣어줌
                    food_info[info] = 0
            
            for rate in food_info['rates']:
                rate['score'] = round(rate['score'], 2)
                if not rate['score']:
                    # 0.0 인 경우, 0 으로 넣어줌
                    rate['score'] = 0

        self.save_json('../menulist.json', list(self.food_infos.values()))

    def newplan_menu_check(self):
        """
        newplan 에 있는 음식 이름들이 올바른지 확인 후, 수정
        """
        newplans_path = self.rsc_path + 'newplans/'
        newplans_list = os.listdir(newplans_path)

        removes = black_lists.removes
        refines = black_lists.refines

        for newplan_file in newplans_list:
            with open(newplans_path + newplan_file, 'r', encoding='utf-8') as newplan_json:
                # newplan: dict, {date, diet}
                #   diet: dict, {time, menu}
                #       menu: list[food], 그 시간대 메뉴
                #           food: str, 음식 이름
                newplan = json.load(newplan_json)
            
            for daily_diet in newplan.values():
                for time, menu in daily_diet.items():
                    clean_menu = list()
                    for food in menu:
                        if food in removes:
                            continue
                        elif food in refines:
                            clean_menu.append(refines[food])
                        else: # No ERROR
                            clean_menu.append(food)
                    daily_diet[time] = clean_menu

            for food in menu:
                if food in removes or food in refines:
                    print(newplan_file, food)

            self.save_json(newplans_path + newplan_file, newplan)

    def newplan_food_name_match(self):
        """
        newplans 에 있는 menu의 food 들이 모두
        menulist 에 등록 되어 있는지 확인
        """
        no_match = list()
        newplans_path = self.rsc_path + 'newplans/'
        newplans_list = os.listdir(newplans_path)

        for newplan_file in newplans_list:
            with open(newplans_path + newplan_file, 'r', encoding='utf-8') as newplan_json:
                # newplan: dict, {date, diet}
                #   diet: dict, {time, menu}
                #       menu: list[food], 그 시간대 메뉴
                #           food: str, 음식 이름
                newplan = json.load(newplan_json)
            
            for daily_diet in newplan.values():
                for menu in daily_diet.values():
                    for food in menu:
                        if food not in no_match and food not in self.food_infos:
                            no_match.append(food) # menulist 에 등록되어 있지 않은 경우
                            print('E: No Match', food)
                        else:
                            self.food_hits[food] += 1
        # 매칭 되지 않는 음식 이름 출력
        if no_match:
            print(no_match)
        else:
            print("No Match SUCCESS")

        # 한 번도 hit 하지 않은 음식 이름 출력
        for food in self.food_hits:
            if not self.food_hits[food]:
                print("W: No Hit", food)
        return no_match

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    checker = Checker()
    checker.check_start()
