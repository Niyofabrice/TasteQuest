from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import get_places_nearby
import requests
import json

# Create your views here.

categories = "4d4b7104d754a06370d81259,4bf58dd8d48988d1e2931735,4bf58dd8d48988d18d941735,\
    4bf58dd8d48988d11f941735,4bf58dd8d48988d18b941735,4bf58dd8d48988d189941735,56aa371be4b08b9a8d573550,\
    63be6904847c3692a84b9bb5,4bf58dd8d48988d16a941735,4bf58dd8d48988d116941735,4bf58dd8d48988d179941735,\
    4bf58dd8d48988d11e941735,4bf58dd8d48988d1d8941735,4bf58dd8d48988d1d5941735,4bf58dd8d48988d121941735,4bf58dd8d48988d11b941735,\
    4bf58dd8d48988d143941735,50327c8591d4c4b30a586d5d,63be6904847c3692a84b9bb6,52e81612bcbc57f1066b7a0c,4bf58dd8d48988d16d941735,\
    4bf58dd8d48988d1e0931735,4bf58dd8d48988d128941735,4d4b7105d754a06374d81259,503288ae91d4c4b30a586d67,4bf58dd8d48988d1c8941735,\
    4bf58dd8d48988d10a941735,5f2c344a5b4c177b9a6dc011,4bf58dd8d48988d14e941735,4bf58dd8d48988d157941735,5f2c2b7db6d05514c7044837,\
    4bf58dd8d48988d142941735,52e81612bcbc57f1066b7a03,4bf58dd8d48988d145941735,52af3aaa3cf9994f4e043bf0,52af3b813cf9994f4e043c04,\
    4eb1bd1c3b7b55596b4a748f,4deefc054765f83613cdba6f,4bf58dd8d48988d111941735,4bf58dd8d48988d113941735,4bf58dd8d48988d149941735,\
    4bf58dd8d48988d14a941735,4bf58dd8d48988d169941735,52e81612bcbc57f1066b7a01,5e179ee74ae8e90006e9a746,52e81612bcbc57f1066b7a02,\
    52e81612bcbc57f1066b79f1,52e81612bcbc57f1066b79f4,4bf58dd8d48988d16c941735,4bf58dd8d48988d144941735,4bf58dd8d48988d154941735,\
    4bf58dd8d48988d16e941735,4bf58dd8d48988d10f941735,5bae9231bedf3950379f89e1,4bf58dd8d48988d1c1941735,4bf58dd8d48988d1c0941735,\
    4bf58dd8d48988d1ca941735,4bf58dd8d48988d1c5941735,4bf58dd8d48988d150941735,4bf58dd8d48988d1cc941735,4f04af1f2fb6e1c99f3db0bb,\
    52f2ab2ebcbc57f1066b8b41,63be6904847c3692a84b9bb7,5267e4d9e4b0ec79466e48d1,5bae9231bedf3950379f89c5,63be6904847c3692a84b9bb8,\
    4bf58dd8d48988d163941735,5fabfe3599ce226e27fe709a,4bf58dd8d48988d1fa931735,4bf58dd8d48988d1ee931735"



def home(request):
    results = get_places_nearby().get("results")

    context = {
        "places": results,
    }

    return render(request, "base.html", context)
    


def user_signup(request):
    """Handle user signup"""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('home')
            except:
                print("username taken")
        else:
            context = {
                "message": "Passwords do not match",
                "username": username,
                "email": email
            }
            return render(request, "signup.html", context)

    return render(request, "signup.html")

def user_login(request):
    """Handle user login"""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.all().filter(email=email).first()
            if user is not None:
                authenticated_user = authenticate(username=user.username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('home')
                else:
                    return render(request, 'login.html', {"error": "Incorrect Password", "email": email})
            else:
                return render(request, 'login.html', {"error": "Email Not Found", "email": email})
        except Exception as e:
            return render(request, 'login.html', {"error": "An Error Occured"})
    return render(request, 'login.html')
    

def user_forgot_password(request):
    return render(request, "forgot_password.html")

def user_logout(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')



def get_place_details(request, place_id):
    details_url = f'https://api.foursquare.com/v3/places/{place_id}'
    headers = {
        'Authorization': "fsq3DpPCdy4UqMmMs9u+pdWD9xUr8NpdjTOwFqdF/ru7b18=",
        'Accept': 'application/json'
    }
    params = {
        'query': '',
        'radius': 5000,
        'categories': categories,
        'fields': "fsq_id,name,geocodes,location,categories,closed_bucket,description,tel,email,website,social_media,hours,hours_popular,rating,popularity,price,menu,date_closed,photos,tastes"
    }
    
    details_response = requests.get(details_url, headers=headers, params=params)
    
    if details_response.status_code != 200:
        return JsonResponse({"Error": "Place details not found"}, status=404)

    place_details = details_response.json()

    # Fetch place photos
    photos_url = f'https://api.foursquare.com/v3/places/{place_id}/photos'
    photos_response = requests.get(photos_url, headers=headers)
    
    photos = []
    if photos_response.status_code == 200:
        photos_data = photos_response.json()
        photos = [photo['prefix'] + 'original' + photo['suffix'] for photo in photos_data]

    context = {
        'place_details': place_details,
        'photos': photos,
    }

    return render(request, 'place_details.html', context)