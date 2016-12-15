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
            'price': food.price,
            'energy': food.energy,
            'carbohydrates': food.carbohydrates,
            'protein': food.protein,
            'fat': food.fat,
            'calcium': food.calcium,
            'iron': food.iron,
            'vitaminA': food.vitaminA,
            'vitaminB1': food.vitaminB1,
            'vitaminB2': food.vitaminB2,
            'vitaminC': food.vitaminC,
        }

        foods.append(food_dict)
        problems_json = json.dumps(foods, ensure_ascii=False)
    return HttpResponse(problems_json, content_type='application/json')


@csrf_exempt
def echo(request):
    try:
        data = request.POST['userAuth']
    except MultiValueDictKeyError or ValueError:
        return HttpResponseNotFound(content_type='application/json')

    return HttpResponse(data, content_type='application/json')



