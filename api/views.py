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
def item_list(request):
    """年齢，性別，活動レベルを受け取り最適な食品お組み合わせを返す"""
    try:
        age = request.POST['age']
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    # TODO: 最適な食品の組み合わせを求める

    return HttpResponse('hoge', content_type='application/json')


@csrf_exempt
def login(request):
    """ログインの可否を返す"""
    try:
        login_id = request.POST['login_id']
        password = request.POST['password']
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    url = 'https://netsuper.daiei.co.jp/index.php?secure=1'
    data = ('submit_member_login%%5B%%5D=member_login&loginCookie=1&login_id=%s&password=%s' % (login_id, password)).encode('utf-8')
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