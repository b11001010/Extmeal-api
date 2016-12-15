import json
from collections import OrderedDict
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from api.models import Food
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
        """三大栄養素"""
            'energy': food.energy,
            'protein': food.protein,
            'fat': food.fat,
            'carbohydrates': food.carbohydrates,
        """ビタミン"""
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
        """ミネラル"""
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

    return HttpResponse('hoge', content_type='application/json')