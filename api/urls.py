from django.conf.urls import url
from api import views

urlpatterns = [
    # 食品
    url(r'^food_list/$', views.food_list, name='food_list'),
    # Echo
    url(r'^echo/$', views.echo, name='echo'),
    # Login
    url(r'^login/$', views.login, name='login'),
]
