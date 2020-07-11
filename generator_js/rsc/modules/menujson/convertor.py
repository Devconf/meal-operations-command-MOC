import json


def load_refine():
    # load refine
    refine = dict()
    with open('menu_refine.txt', 'r') as refine_file:
        for line in refine_file:
            line = line.strip()
            target, convert = line.split(', ')
            refine[target] = convert
    return refine

def load_food_infos():
    # load menu_json
    with open('menu.json', 'r', encoding='utf-8') as menu_json:
        # {food:food_info} <- food_info : dict (영양 정보)
        food_infos = json.load(menu_json)
        return food_infos

def save_json(result_file, list_data):
    with open(result_file, 'w', encoding='utf-8') as result_json:
        json.dump(list_data, result_json, ensure_ascii=False, indent=2)

def convert():
    refine = load_refine()
    food_infos = load_food_infos()
    errors = list()

    # target 이 모두 menu.json 에 있는 이름인지 체크
    for target in refine:
        if not target in food_infos:
            errors.append(target)


    if not errors:
        # 최종 저장할 데이터 형태에 맞게 수정
        converted = list()
        converted_with_mg = list()
        for food, food_info in food_infos.items():
            # refine 해야하는 대상인 경우,
            # 바뀐 이름을 넣어줌
            if food in refine:
                food_info['title'] = refine[food]
            else:
                food_info['title'] = food

            # subname 지워줌
            food_info.pop('subname')
            converted.append(food_info)

            # mg 수정한 형태
            for nutrient in ['sodium', 'cholesterol']:
                food_info[nutrient] /= 1000
            converted_with_mg.append(food_info)
        
        # 최종 결과 json으로 저장
        save_json('new_menu.json', converted)
        save_json('new_menu_with_mg.json', converted_with_mg)
        print('SUCCESS')
    else:
        print('ERROR', errors)

if __name__ == '__main__':
    convert()
