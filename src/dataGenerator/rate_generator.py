import json
import random

class RateGenerator:
    """
    기존의 food_info 에 별점 정보를 더함
    더해지는 별점은 dumy data로 그 기준은
    self.check_delicious() 함수를 따름.
    """
    def __init__(self, rsc_path):
        self.food_infos = dict()
        with open(rsc_path + 'menulist.json', 'r', encoding='utf-8') as menu_json:
            # {food:food_info} <- food_info : dict (영양 정보)
            raw_food_infos = json.load(menu_json)
            for food_info in raw_food_infos:
                food = food_info['title']
                self.food_infos[food] = food_info

    def add_rate(self):
        dumy_rate = dict()
        for food, food_info in self.food_infos.items():
            food_info['rates'] = [{
                'userId': 'soldier76',
                'score': round(self.check_delicious(food), 2)}] # 2자리수 반올림
            dumy_rate[food] = food_info['rates'][0]['score']
        # self.save_as_json('../')
        with open('../rate_infos.json', 'w', encoding='utf-8') as rate_json:
            json.dump(dumy_rate, rate_json, ensure_ascii=False, indent=2)
    
    def check_delicious(self, food):
        has_famous = False
        for famous in ["고기", "미트", "소", "돼지", "닭", "삼겹", "까스", "새우", "갈비", "치킨", "햄", "스테이크"]:
            if food.find(famous) > -1:
                has_famous = True
                break
        important = True if self.food_infos[food]['category'] in ["메인", "서브"] else False

        if has_famous and important:
            return random.uniform(4, 5)
        elif has_famous or important:
            return random.uniform(3, 4)
        else:
            return random.uniform(0.1, 3)

    def save_as_json(self, result_path):
        with open(result_path + 'menulist_rate.json', 'w', encoding='utf-8') as json_file:
            food_infos_list = list(self.food_infos.values())
            json.dump(food_infos_list, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    rategenerator = RateGenerator('../')
    rategenerator.add_rate()
