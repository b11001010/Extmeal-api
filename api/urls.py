from django.conf.urls import url
from api import views

urlpatterns = [
    # 食品
    url(r'^food_list/$', views.food_list, name='food_list'),
    # Echo
    url(r'^echo/$', views.echo, name='echo'),
    # Login
    url(r'^login/$', views.login, name='login'),
    # item_list
    url(r'^item_list/$', views.item_list, name='item_list'),
    # submit
    url(r'^submit/$', views.submit, name='submit'),
]
