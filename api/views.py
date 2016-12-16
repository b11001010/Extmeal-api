import json

import urllib.request
from http import cookiejar

from collections import OrderedDict
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from api.models import Food

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError
from chardet import detect
import xmltodict
import numpy as np
import math
import random
# Create your views here.


# cookie管理
COOKIE = cookiejar.CookieJar()

def food_list(request):
    """食品のリストのJSONを返す"""
    foods = []
    for food in Food.objects.all():

        food_dict = {
            'id': food.id,
            'name': food.name,
            'item_id': food.item_id,
            'price': food.price,
            'gram': food.gram,

            'energy': food.energy,
            'protein': food.protein,
            'fat': food.fat,
            'carbohydrates': food.carbohydrates,

            'vitaminA': food.vitaminA,
            'vitaminD': food.vitaminD,
            'vitaminE': food.vitaminE,
            'vitaminK': food.vitaminK,
            'vitaminB1': food.vitaminB1,
            'vitaminB2': food.vitaminB2,
            'niacin': food.niacin,
            'vitaminB6': food.vitaminB6,
            'vitaminB12': food.vitaminB12,
            'folate': food.folate,
            'pantothenic': food.pantothenic,
            'biotin': food.biotin,
            'vitaminC': food.vitaminC,

            'sodium': food.sodium,
            'potassium': food.potassium,
            'calcium': food.calcium,
            'magnesium': food.magnesium,
            'phosphorus': food.phosphorus,
            'iron': food.iron,
            'zinc': food.zinc,
            'copper': food.copper,
            'manganese': food.manganese,
            'iodine': food.iodine,
            'selenium': food.selenium,
            'chromium': food.chromium,
            'molybdenum': food.molybdenum,
        }

        foods.append(food_dict)
        problems_json = json.dumps(foods, ensure_ascii=False)
    return HttpResponse(problems_json, content_type='application/json')


@csrf_exempt
def echo(request):
    """ただのEcho"""
    try:
        data = request.POST['userAuth']
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def login(request):
    """ログインの可否を返す"""
    try:
        auth = request.POST['auth']
        json_data = json.loads(auth)
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    url = 'https://netsuper.daiei.co.jp/index.php?secure=1'
    data = ('submit_member_login%%5B%%5D=member_login&loginCookie=1&login_id=%s&password=%s' % (json_data["login_id"], json_data["password"])).encode('utf-8')
    req = urllib.request.Request(url, data)

    opener = urllib.request.build_opener()
    opener.add_handler(urllib.request.HTTPCookieProcessor(COOKIE))

    response = opener.open(req).read().decode('utf-8')
    if '配達便の選択' in response:
        """ログイン成功"""
        return JsonResponse({"result": True})
    else:
        """ログイン失敗"""
        return JsonResponse({"result": False})



def getNutritionParam():
    paramDict = {}
    try:
        apiUrl = "http://localhost/api/food_list/"

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
    ntr["vitaminA"] = 600
    ntr["vitaminD"] = 5.5
    ntr["vitaminE"] = 6.5
    ntr["vitaminK"] = 150
    ntr["vitaminB1"] = 1.2
    ntr["vitaminB2"] = 1.3
    ntr["niacin"] = 13
    ntr["vitaminB6"] = 1.2
    ntr["vitaminB12"] = 2.0
    ntr["folate"] = 50
    ntr["pantothenic"] = 5  # 目安量
    ntr["biotin"] = 50
    ntr["vitaminC"] = 85
    ntr["sodium"] = 600
    ntr["potassium"] = 2500  # 目安
    ntr["calcium"] = 650
    ntr["magnesium"] = 280
    ntr["phosphorus"] = 1000  # 目安
    ntr["iron"] = 6.0
    ntr["zinc"] = 8.0
    ntr["copper"] = 0.7
    ntr["manganese"] = 4.0  # 目安量
    ntr["iodine"] = 95
    ntr["selenium"] = 25
    ntr["chromium"] = 10  # 目安量
    ntr["molybdenum"] = 20

    return ntr


def coolingExp(a, T_k):
    return a * T_k


def metropolis(deltaGap, T_k):
    return math.exp(-deltaGap / T_k)


def simulatedAnnealing(nutritionList, avgNutritionList):
    # 【定数宣言】
    INIT_TEMPERATURE = 1.0  # 初期温度
    CONV_TEMPERATURE = 0.1  # 収束温度
    SEARCH_TIME = 4         # 探索回数
    FOOD_NUM = 20            # 食品数

    # 【変数宣言】
    # ＜ナップザック関連＞
    selectedItems = np.array([0] * FOOD_NUM)
    goodSelectedItems = np.array([0] * FOOD_NUM)
    selectedItemsName = {}

    # 【メインルーチン】
    # 初期化
    T_k = INIT_TEMPERATURE
    keepErrorVal = 9999999

    # 〇収束温度まで繰り返し
    while T_k > CONV_TEMPERATURE:
        # 〇一定回数まで同一温度で探索を繰り返し
        for searchTime in range(1, SEARCH_TIME):
            # 購入する品物の数を変更
            changeIdx = random.randint(1, FOOD_NUM) - 1
            selectedItems[changeIdx] = (selectedItems[changeIdx] + 1) % 2

            # 生成した解の評価
            newErrorVal = 0.0
            newErrorVal += (
                avgNutritionList["protein"]
                + avgNutritionList["fat"]
                + avgNutritionList["carbohydrates"]
                + avgNutritionList["vitaminA"]
                + avgNutritionList["vitaminD"]
                + avgNutritionList["vitaminE"]
                + avgNutritionList["vitaminK"]
                + avgNutritionList["vitaminB1"]
                + avgNutritionList["vitaminB2"]
                + avgNutritionList["niacin"]
                + avgNutritionList["vitaminB6"]
                + avgNutritionList["vitaminB12"]
                + avgNutritionList["folate"]
                + avgNutritionList["pantothenic"]
                + avgNutritionList["biotin"]
                + avgNutritionList["vitaminC"]
                + avgNutritionList["sodium"]
                + avgNutritionList["potassium"]
                + avgNutritionList["calcium"]
                + avgNutritionList["magnesium"]
                + avgNutritionList["phosphorus"]
                + avgNutritionList["iron"]
                + avgNutritionList["zinc"]
                + avgNutritionList["copper"]
                + avgNutritionList["manganese"]
                + avgNutritionList["iodine"]
                + avgNutritionList["selenium"]
                + avgNutritionList["chromium"]
                + avgNutritionList["molybdenum"]
            )
            for i in range(0, FOOD_NUM):
                selectedItem = selectedItems[i]
                if selectedItem == 1:
                    newErrorVal -= (
                        nutritionList[i]["protein"]
                        + nutritionList[i]["fat"]
                        + nutritionList[i]["carbohydrates"]
                        + nutritionList[i]["vitaminA"]
                        + nutritionList[i]["vitaminD"]
                        + nutritionList[i]["vitaminE"]
                        + nutritionList[i]["vitaminK"]
                        + nutritionList[i]["vitaminB1"]
                        + nutritionList[i]["vitaminB2"]
                        + nutritionList[i]["niacin"]
                        + nutritionList[i]["vitaminB6"]
                        + nutritionList[i]["vitaminB12"]
                        + nutritionList[i]["folate"]
                        + nutritionList[i]["pantothenic"]
                        + nutritionList[i]["biotin"]
                        + nutritionList[i]["vitaminC"]
                        + nutritionList[i]["sodium"]
                        + nutritionList[i]["potassium"]
                        + nutritionList[i]["calcium"]
                        + nutritionList[i]["magnesium"]
                        + nutritionList[i]["phosphorus"]
                        + nutritionList[i]["iron"]
                        + nutritionList[i]["zinc"]
                        + nutritionList[i]["copper"]
                        + nutritionList[i]["manganese"]
                        + nutritionList[i]["iodine"]
                        + nutritionList[i]["selenium"]
                        + nutritionList[i]["chromium"]
                        + nutritionList[i]["molybdenum"]
                    )
            newErrorVal = abs(newErrorVal)

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
                    selectedItems[changeIdx] = (selectedItems[changeIdx] + 1) % 2
        # 温度を下げる
        T_k = coolingExp(0.97, T_k)

    item_list = []
    for i in range(0, FOOD_NUM):
        if selectedItems[i] == 1:
            selectedItemsName[i] = {}
            selectedItemsName[i]["food"] = nutritionList[i]["name"]
            selectedItemsName[i]["item_id"] = nutritionList[i]["item_id"]
            item_list.append(selectedItemsName[i])

    return json.dumps(item_list, ensure_ascii=False)


@csrf_exempt
def item_list(request):
    """年齢，性別，活動レベルを受け取り最適な食品お組み合わせを返す"""
    try:
        data = request.POST['userInfo']
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    json_data = json.loads(data)

    nutritionParam = getNutritionParam()

    age = json_data['age']  # 年齢
    gender = json_data['gender']  # 性別 1は男2は女
    activity_level = json_data['activity_level']  # 活動レベル ３段階，大きい方が運動量が多い

    res = foodNutr(age, gender, activity_level)

    jsonString = simulatedAnnealing(nutritionParam, res)

    print(jsonString)

    return HttpResponse(jsonString, content_type='application/json')


@csrf_exempt
def submit(request):
    """購入処理"""