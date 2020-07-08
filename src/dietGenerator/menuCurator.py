"""
메뉴 추천기
food_info 를 기반으로 menu 를 추천
"""
from math import sqrt

class MenuCurator:
    """
    @parm:
        food_infos: dict, {food:food_info}
            food: str, 음식 이름
            food_info: dict, 음식 정보
            {
                subname: str,
                nutrient: float,
                category: str,
                allergy: list[int],
                title: str,
            }
            (nutrient:= cal, fat, protein, carbohydrate, sugar, sodium, cholesterol)
    """
    def __init__(self, food_infos):
        # 영양 정보 가져오기
        self.food_infos = food_infos
        self.food_vectors = self.info2vector()

    def info2vector(self):
        """
        @return:
            food_vectors: dict, {food:food_vector}
                food_vector: tuple(float), nutirents
                    nutrients:= cal, fat, protein, carbohydrate, sugar, sodium, cholesterol
        """
        food_vectors = dict()
        for food, food_info in self.food_infos.items():
            temp_food_vector = list(food_info.values())[3:8] # nutrients
            """
            추가하고 싶은 벡터 요소를
            temp_food_vector.append( 요소 ) 로 추가
            """
            # tuple 로 변경 불가능하게
            food_vectors[food] = tuple(temp_food_vector)
        return food_vectors

    def find_similar_foods(self, target_food, baseline=0.999):
        """
        @parm:
            target_food: str, 음식 이름
        @return:
            baseline 이상의 similarity 를 가진 음식들
            found: list(str), 음식 이름 리스트
        """
        similar_foods = list()
        for food in self.food_vectors:
            if not food == target_food:
                similarity = self.food_similarity(food, target_food)
                if similarity >= baseline:
                    similar_foods.append(food)
        return similar_foods

    def food_similarity(self, food_a, food_b):
        """
        @parm:
            food_a: str, 첫 번째 음식 이름
            food_b: str, 두 번째 음식 이름
        @return:
            similarity: float, 코사인 유사도 (0~1)
            1에 가까울 수록 유사함
        """
        vector_a = self.food_vectors[food_a]
        vector_b = self.food_vectors[food_b]
        return self.cos_similarity(vector_a, vector_b)
    
    def cos_similarity(self, vector_a, vector_b):
        """
        @parm:
            vector: tuple(float)
            vector: tuple(float)
        @return:
            cos(theta) 0 to 1
            theta:= 두 벡터가 이루는 각
        """
        size_product = self.norm_of(vector_a)*self.norm_of(vector_b)
        if not size_product:
            return 0 # 둘 중 하나라도 벡터 크기가 0인 경우
        dot_result = self.dot_product(vector_a, vector_b)
        return dot_result/size_product

    @staticmethod
    def dot_product(vector_a, vector_b):
        """
        @parm:
            vector: tuple(float)
            vector: tuple(float)
        @return:
            dot: float, 두 벡터의 내적값
        """
        return sum(map(lambda elm_a, elm_b: elm_a*elm_b, vector_a, vector_b))

    @staticmethod
    def norm_of(vector):
        """
        @parm:
            vector: tuple(float)
        @return:
            norm: float, 벡터의 절댓값 (크기)
        """
        return sqrt(sum(map(lambda elm: elm*elm, vector)))
