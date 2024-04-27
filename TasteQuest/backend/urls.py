from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get_place/', search_restaurants, name="search_restaurants"),
    path('save_location/', save_location, name="save_location"),
]
