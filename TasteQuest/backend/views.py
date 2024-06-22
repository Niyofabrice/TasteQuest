from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import get_places_nearby
import requests
import json

# Create your views here.

api_key = "FBfcGVZBIxMBGzTztAhR0VmEdrIcCxdn"
api_key2 = "33392eacd2msha34644b78dc6760p185cecjsn3c8e231a16cf"
rapidapi_host = "map-places.p.rapidapi.com"

categories = ["10000","13000","14000"]

fields = ["fsq_id","name","geocodes","location","categories","closed_bucket","description","tel","email","website",
        "social_media","hours","hours_popular","rating","popularity","price","menu","date_closed","photos","tastes"]

api_url = "https://api.tomtom.com/search/"
version = "2"
language = "en-US"
location_data = {}
headers = {
            "X-RapidAPI-Key": api_key2,
            'X-RapidAPI-Host': rapidapi_host,
       }

# https://api.tomtom.com/search/2/poiCategories.json?language=en-US&key=*****


def home(request):

    return render(request, 'base.html')


def save_location(request):
    if request.method == 'POST':
        data = request.POST
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Process location data (e.g., save to database)
        location_data['latitude'] = latitude
        location_data['longitude'] = longitude
        print(location_data)

        # Optionally, send a response back to the client

        return JsonResponse({'Success': 'location saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_place_details(place_id):
    # Construct API request URL with parameters
    place_detail_api_url = "https://map-places.p.rapidapi.com/details/json"
    details_params = {
        "place_id": place_id,
    }

    # Make Place Detail API request
    details_response = requests.get(place_detail_api_url, headers=headers, params=details_params)
    if details_response.status_code == 200:
        data_str = details_response.content.decode('utf-8')  # Decode byte data to string
        data_dict = json.loads(data_str)  # Parse JSON string to dictionary

        return data_dict   # Return place details
    else:
        # Return error message
        return None


def get_place_photos(photo_reference, maxheight, maxwidth):
    # Construct API request URL with parameters
    place_photo_api_url = "https://map-places.p.rapidapi.com/photo"
    photo_params = {
        "photo_reference": photo_reference,
        "maxheight": maxheight,
        "maxwidth": maxwidth
    }

    # Make Place Photo API request
    photo_response = requests.get(place_photo_api_url, headers=headers, params=photo_params)

    if photo_response.status_code == 200:
        # Return the raw image data
        return photo_response.content
    else:
        # Return an error message
        return {'error': f"Error fetching place photo, status code: {photo_response.status_code}"}


def recommend_places(request):
    latitude = location_data["latitude"]
    longitude = location_data["longitude"]
    if latitude and longitude:
        places = get_places_nearby(latitude, longitude)
        print(places)
        # Process and filter results as needed
        return render(request, 'card.html', {'places': places})
    return render(request, 'base.html')


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

