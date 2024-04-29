from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json

# Create your views here.

api_key = "FBfcGVZBIxMBGzTztAhR0VmEdrIcCxdn"
api_key2 = "33392eacd2msha34644b78dc6760p185cecjsn3c8e231a16cf"
rapidapi_host = "map-places.p.rapidapi.com"

# api_url = "https://api.tomtom.com/search/"
version = "2"
language = "en-US"
location_data = {}
headers = {
            "X-RapidAPI-Key": api_key2,
            'X-RapidAPI-Host': rapidapi_host,
        }

# https://api.tomtom.com/search/2/poiCategories.json?language=en-US&key=*****


def home(request):
    return render(request, 'index.html')


def save_location(request):
    if request.method == 'POST':
        data = request.POST
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Process location data (e.g., save to database)
        location_data['latitude'] = latitude
        location_data['longitude'] = longitude

        # Optionally, send a response back to the client
        return JsonResponse({'Success': 'location saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_place(request):
    if request.method == 'GET':
        # Construct API request URL with parameters
        nearby_search_api_url = "https://map-places.p.rapidapi.com/nearbysearch/json"
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

                # Define fields to extract
                fields = [
                    'current_opening_hours',
                    'formatted_address',
                    'formatted_phone_number',
                    'photos',
                    'rating',
                    'reviews',
                    'user_ratings_total',
                    'wheelchair_accessible_entrance'
                ]

                # Get details of the place
                place_details = get_place_details(place_id, fields='photos, rating, reviews')

                # Get photos of the place
                # for photo in place_details["photos"]:
                #     photo_reference = photo["photo_reference"]
                #     maxheight = 400
                #     maxwidth = 400
                #
                #     place_photos = get_place_photos(photo_reference, maxheight, maxwidth)

                # print(place_details)

                return HttpResponse(place_details)  # To be worked on
        else:
            return HttpResponse(f"Error fetching Places, status code: {response.status_code}")

    return HttpResponse("Invalid request method")


def get_place_details(place_id, fields):
    # Construct API request URL with parameters
    place_detail_api_url = "https://map-places.p.rapidapi.com/details/json"
    details_params = {
        "place_id": place_id,
        "fields": fields
    }

    # Make Place Detail API request
    details_response = requests.get(place_detail_api_url, headers=headers, params=details_params)
    if details_response.status_code == 200:
        data_str = details_response.content.decode('utf-8')  # Decode byte data to string
        data_dict = json.loads(data_str)  # Parse JSON string to dictionary

        return data_dict   # Return place details
    else:
        # Return error message
        return {'error': f"Error fetching Place details, status code: {details_response.status_code}"}


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
