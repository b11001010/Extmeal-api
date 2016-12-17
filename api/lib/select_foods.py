from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError
from chardet import detect
import xmltodict
import numpy as np
import math
import random
import json

def getNutritionParam():
    paramDict = {}
    try:
        apiUrl = "http://localhost:8000/api/food_list/"

        with urlopen(apiUrl) as response:
            jsonString = response.read()                       # jsonデータの読込
            jsonString = jsonString.decode('utf-8')
            paramDict = json.loads(jsonString)            # jsonデータの辞書型への変換

    except URLError as e:
        if hasattr(e, "reason"):
            print("We failed to reach a server.")
            print("Reason: ", e.reason)
        elif hasattr(e, "code"):
            print("The server couldn\'t fulfill the request.")
            print("Error code: ", e.code)
        else:
            print("none")

    return paramDict


def foodNutr(age, gender, activity_level):
    ntr = {"manganese": 0.0, "molybdenum": 0.0, "sodium": 0.0,
           "copper": 0.0, "selenium": 0.0, "vitaminB2": 0.0,
           "folate": 0.0, "vitaminA": 0.0, "iron": 0.0,
           "fat": 0.0, "vitaminC": 0.0, "vitaminB12": 0.0,
           "niacin": 0.0, "vitaminE": 0.0, "calcium": 0.0,
           "chromium": 0.0, "carbohydrates": 0.0, "zinc": 0.0,
           "vitaminB1": 0.0, "vitaminD": 0.0, "phosphorus": 0.0,
           "protein": 0.0, "potassium": 0.0, "biotin": 0.0,
           "iodine": 0.0, "vitaminB6": 0.0, "pantothenic": 0.0,
           "vitaminK": 0.0
           }

    activity = 0.0
    weight = 0.0
    metabo = 0.0
    dayEnergy = 0.0
    mealEnergy = 0.0  # 一食に必要なエネルギー

    # 活動量の算出
    if activity_level == "1":
        activity = 1.5
    elif activity_level == "2":
        activity = 1.75
    else:
        activity = 2.0

    # 男の場合 20歳を前提に作る
    if gender == "1":
        weight = 63.2
        metabo = 24.0
    else:
        weight = 63.2
        metabo = 24.0

    dayEnergy = weight * metabo * activity
    dayEnergy = round(dayEnergy, 1)
    mealEnergy = dayEnergy / 3
    mealEnergy = round(mealEnergy, 1)

    # 栄養素の計算 目安量の項目はいらないかもしれない
    # fat = 20% 目安 0.1g = 0.9kcal
    ntr["protein"] = 50
    fat = round(mealEnergy / 5)
    fat = round(fat / 9)
    ntr["fat"] = fat

    # 飽和脂肪酸  = 7 目標 n-6系脂肪酸　 11  目安 n-3系脂肪酸	 2 目安
    # 炭水化物　  = 50% 目標  0.1g 0.4kcal
    carbohydrates = round(mealEnergy / 2)
    carbohydrates = round(carbohydrates / 4)
    ntr["carbohydrates"] = carbohydrates
    # 食物繊維    = 20 目標
    ntr["vitaminA"] = 600.0 / 3.0
    ntr["vitaminD"] = 5.5 / 3.0
    ntr["vitaminE"] = 6.5 / 3.0
    ntr["vitaminK"] = 150.0 / 3.0
    ntr["vitaminB1"] = 1.2 / 3.0
    ntr["vitaminB2"] = 1.3 / 3.0
    ntr["niacin"] = 13.0 / 3.0
    ntr["vitaminB6"] = 1.2 / 3.0
    ntr["vitaminB12"] = 2.0 / 3.0
    ntr["folate"] = 50.0 / 3.0
    ntr["pantothenic"] = 5.0 / 3.0  # 目安量
    ntr["biotin"] = 50.0 / 3.0
    ntr["vitaminC"] = 85.0 / 3.0
    ntr["sodium"] = 600.0 / 3.0
    ntr["potassium"] = 2500.0 / 3.0  # 目安
    ntr["calcium"] = 650.0 / 3.0
    ntr["magnesium"] = 280.0 / 3.0
    ntr["phosphorus"] = 1000.0 / 3.0  # 目安
    ntr["iron"] = 6.0 / 3.0
    ntr["zinc"] = 8.0 / 3.0
    ntr["copper"] = 0.7 / 3.0
    ntr["manganese"] = 4.0 / 3.0  # 目安量
    ntr["iodine"] = 95.0 / 3.0
    ntr["selenium"] = 25.0 / 3.0
    ntr["chromium"] = 10.0 / 3.0  # 目安量
    ntr["molybdenum"] = 20.0 / 3.0

    return ntr


def coolingExp(a, T_k):
    return a * T_k


def metropolis(deltaGap, T_k):
    return math.exp(-deltaGap / T_k)


def simulatedAnnealing(foodNutritionList, avgNutritionList):
    # 【変数宣言】
    nutritionNames = [
        "protein",      "fat",          "carbohydrates",    "vitaminA",     "vitaminD",
        "vitaminE",     "vitaminK",     "vitaminB1",        "vitaminB2",    "niacin",
        "vitaminB6",    "vitaminB12",   "folate",           "pantothenic",  "biotin",
        "vitaminC",     "sodium",       "potassium",        "calcium",       "magnesium",
        "phosphorus",   "iron",         "zinc",             "copper",         "manganese",
        "iodine",       "selenium",     "chromium",         "molybdenum"
    ]
    sumNutritionList = {}

    # 【定数宣言】
    FOOD_NUM = 20                       # 食品数
    NUTRITION_NUM = len(nutritionNames) #栄養素種数
    INIT_TEMPERATURE = 1.0              # 初期温度
    CONV_TEMPERATURE = 0.1              # 収束温度
    SEARCH_TIME = FOOD_NUM              # 探索回数

    # 【メインルーチン】
    # 初期化
    T_k = INIT_TEMPERATURE
    keepErrorVal = 9999999
    goodErrorVal = keepErrorVal
    for i in range(0, NUTRITION_NUM):
        sumNutritionList[nutritionNames[i]] = 0.0

    # 計算対象とする食品の選択
    calcFoodsFlg = {}
    for i in range(0, NUTRITION_NUM):
        nutritionName = nutritionNames[i]
        calcFoodsFlg[nutritionName] = False

        for j in range(0, FOOD_NUM):
            if foodNutritionList[j][nutritionName] > 0.0:
                calcFoodsFlg[nutritionName] = True
                break

    # 基準化
    normalizeNutrition = {}
    for i in range(0, FOOD_NUM):
        normalizeNutrition[i] = {}
        for j in range(0, NUTRITION_NUM):
            nutritionName = nutritionNames[j]
            hoge = foodNutritionList[i][nutritionName]
            fuga = avgNutritionList[nutritionName]
            normalizeNutrition[i][nutritionName] = hoge / fuga
            # normalizeNutrition[i][nutritionName] = foodNutritionList[i][nutritionName] / avgNutritionList[nutritionName]

    # 〇収束温度まで繰り返し
    fixFoodIdx = random.randint(1, FOOD_NUM) - 1

    selectedFoods = np.array([0] * FOOD_NUM)
    goodSelectedFoods = np.array([0] * FOOD_NUM)
    while T_k > CONV_TEMPERATURE:
        # 〇一定回数まで同一温度で探索を繰り返し
        for searchTime in range(1, SEARCH_TIME):
            # 購入する品物の数を変更
            while True:
                changeIdx = random.randint(1, FOOD_NUM) - 1
                if fixFoodIdx != changeIdx:
                    break
            selectedFoods[changeIdx] = (selectedFoods[changeIdx] + 1) % 2

            # 生成した解の評価
            newErrorVal = 0.0
            for i in range(0, NUTRITION_NUM):
                if calcFoodsFlg[nutritionNames[i]] == True:
                    newErrorVal += 1.0
            for i in range(0, FOOD_NUM):
                if selectedFoods[i] == 1:
                    for j in range(0, NUTRITION_NUM):
                        newErrorVal -= normalizeNutrition[i][nutritionNames[j]]
            newErrorVal = abs(newErrorVal)

            # 最適解の場合
            if goodErrorVal > newErrorVal:
                goodErrorVal = newErrorVal
                for i in range(0, FOOD_NUM):
                    goodSelectedFoods[i] = selectedFoods[i]

            # 解の遷移の取消判定
            if keepErrorVal > newErrorVal:
                # ＜改善している場合＞
                keepErrorVal = newErrorVal
            else:
                # ＜改悪している場合＞
                if random.uniform(0.0, 1.0) <= metropolis(newErrorVal - keepErrorVal, T_k):
                    # 改悪を許可
                    keepErrorVal = newErrorVal
                else:
                    # 前回の状態を維持
                    selectedFoods[changeIdx] = (selectedFoods[changeIdx] + 1) % 2
        # 温度を下げる
        T_k = coolingExp(0.97, T_k)

    # jsonデータの作成
    outputJsonList = []
    for i in range(0, FOOD_NUM):
        if goodSelectedFoods[i] == 1:
            selectedItemsName = {}
            selectedItemsName["food"] = foodNutritionList[i]["name"]
            selectedItemsName["item_id"] = foodNutritionList[i]["item_id"]
            outputJsonList.append(selectedItemsName)

            for j in range(0, NUTRITION_NUM):
                nutritionName = nutritionNames[j]
                sumNutritionList[nutritionName] += foodNutritionList[i][nutritionName]
    outputJsonList.append(sumNutritionList)  # 算出した食品組合せの栄養素合計を登録

    # print(avgNutritionList)
    # print(sumNutritionList)
    # print(goodSelectedFoods)

    return json.dumps(outputJsonList, ensure_ascii=False)
