from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('signup/', user_signup, name="signup"),
    path('login/', user_login, name="login"),
    path('forgot_password/', user_forgot_password, name="forgot-password"),
    path('logout/', user_logout, name="logout"),
    path('place_details/<str:place_id>/', get_place_details, name='place_details'),
]
