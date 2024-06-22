from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import get_places_nearby
import requests
import json

# Create your views here.

#api_key = "FBfcGVZBIxMBGzTztAhR0VmEdrIcCxdn"
#api_key2 = "33392eacd2msha34644b78dc6760p185cecjsn3c8e231a16cf"
#rapidapi_host = "map-places.p.rapidapi.com"

# api_url = "https://api.tomtom.com/search/"
#version = "2"
#language = "en-US"
location_data = {}
#headers = {
#            "X-RapidAPI-Key": api_key2,
#            'X-RapidAPI-Host': rapidapi_host,
#       }

# https://api.tomtom.com/search/2/poiCategories.json?language=en-US&key=*****


def home(request):
    places = [
        {"name": "The Rustic Grill", "description": "Nestled in the heart of a charming neighborhood, The Rustic Grill offers a cozy and inviting atmosphere where the flavors of farm-fresh ingredients shine. With a focus on locally sourced produce and meats, their menu features mouthwatering grilled dishes and hearty comfort foods, all expertly prepared with a rustic touch.", "image": "images/pexels-vedanti-66315-239975.jpg", "cuisine": "American, Grill", "price_range": 15},
        {"name": "Pasta Amore", "description": "Indulge in the authentic flavors of Italy at Pasta Amore, where every dish is a labor of love. With recipes passed down through generations, their chefs masterfully prepare homemade pasta and sauces using only the finest ingredients. From classic favorites like spaghetti carbonara to innovative creations, each bite promises a delightful journey through the rustic and rich flavors of the Italian countryside.", "image": "images/pexels-thomas-balabaud-735585-1579739.jpg", "cuisine": "Italian", "price_range": 35},
        {"name": "Sushi Sakura", "description": "Step into the elegantly minimalist ambiance of Sushi Sakura and embark on a culinary journey through the finest in Japanese cuisine. Their skilled sushi chefs meticulously craft each roll and nigiri, showcasing the freshest seafood and a dedication to authentic flavors. Complemented by a selection of warm and cold small plates, Sushi Sakura offers a true taste of Japan.", "image": "images/pexels-reneasmussen-1581384.jpg", "cuisine": "Japanese", "price_range": 25},
        {"name": "Spice Bazaar", "description": "Embark on a flavorful adventure at Spice Bazaar, where the vibrant aromas and bold spices of Middle Eastern and Mediterranean cuisines come together in a tantalizing fusion. From succulent kebabs to fragrant tagines and creamy hummus, each dish is a celebration of exotic ingredients and time-honored cooking techniques, transporting you to the bustling markets of faraway lands.", "image": "images/pexels-pixabay-262047.jpg", "cuisine": "Indian", "price_range": 20},
        # Add more card data as needed
    ]

    context = {
        "places": places,
    }

    return render(request, 'base.html', context)


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


def get_place(request):
    if request.method == 'GET':
        # Construct API request URL with parameters
        nearby_search_api_url = "https://map-places.p.rapidapi.com/nearbysearch/json"
        print(location_data)
        params = {
            "location": location_data["latitude"] + ', ' + location_data["longitude"],
            "radius": "5000",
            # "keyword": 'cruise',
            "type": 'restaurant'
        }

        # Make Nearby Search API request
        response = requests.get(nearby_search_api_url, headers=headers, params=params)

        if response.status_code == 200:
            data_str = response.content.decode('utf-8')  # Decode byte data to string
            data_dict = json.loads(data_str)  # Parse JSON string to dictionary

            # Extract place information
            for place in data_dict.get('results', []):
                # Get the place id
                place_id = place.get("place_id")
                print(place_id)

                # Define fields to extract
                fields = ['current_opening_hours, formatted_address, formatted_phone_number, photos, rating, reviews, user_ratings_total, wheelchair_accessible_entrance']

                # Get details of the place
                place_details = get_place_details(place_id)
                print(place_details.get("result"))

                # if place_details is not None:
                #     # Get photos of the place
                #     photos = place_details.get("photos")
                #     if photos is not None:
                #         for photo in photos:
                #             photo_reference = photo.get("photo_reference")
                #             maxheight = 400
                #             maxwidth = 400
                #
                #             # Get place photos
                #             place_photos = get_place_photos(photo_reference, maxheight, maxwidth)

            return JsonResponse(place_details.get("result"))  # To be worked on
        else:
            return HttpResponse(f"Error fetching Places, status code: {response.status_code}")

    return HttpResponse("Invalid request method")


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
        # Process and filter results as needed
        return render(request, 'recommendations.html', {'places': places})
    return render(request, 'location_form.html')


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

