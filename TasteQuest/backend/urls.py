from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get_place/', get_place, name="get_place"),
    path('save_location/', save_location, name="save_location"),
    path('signup/', user_signup, name="signup"),
    path('login/', user_login, name="login"),
    path('forgot_password', user_forgot_password, name="forgot-password"),
    path('logout/', user_logout, name="logout")
]
