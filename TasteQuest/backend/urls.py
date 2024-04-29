from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get_place/', get_place, name="get_place"),
    path('save_location/', save_location, name="save_location"),
]
