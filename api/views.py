import json

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, HttpResponseNotFound
from api.models import Food

from api.lib import select_foods
from api.lib import daiei_client

# Create your views here.


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

    login_result = daiei_client.login(json_data["login_id"], json_data["password"])

    if login_result:
        """ログイン成功"""
        return JsonResponse({"result": True})
    else:
        """ログイン失敗"""
        return JsonResponse({"result": False})


@csrf_exempt
def item_list(request):
    """年齢，性別，活動レベルを受け取り最適な食品お組み合わせを返す"""
    try:
        data = request.POST['userInfo']
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    json_data = json.loads(data)

    nutritionParam = select_foods.getNutritionParam()

    age = json_data['age']  # 年齢
    gender = json_data['gender']  # 性別 1は男2は女
    activity_level = json_data['activity_level']  # 活動レベル ３段階，大きい方が運動量が多い

    res = select_foods.foodNutr(age, gender, activity_level)

    jsonString = select_foods.simulatedAnnealing(nutritionParam, res)


    return HttpResponse(jsonString, content_type='application/json')


@csrf_exempt
def submit(request):
    """購入処理"""
