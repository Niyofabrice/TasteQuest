from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

# Create your views here.

api_key = "FBfcGVZBIxMBGzTztAhR0VmEdrIcCxdn"
api_key2 = "33392eacd2msha34644b78dc6760p185cecjsn3c8e231a16cf"
rapidapi_host = "map-places.p.rapidapi.com"

# api_url = "https://api.tomtom.com/search/"
version = "2"
language = "en-US"
location_data = {}

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


# def get_places(request):
#     if request.method == "GET":
#         url = f"{api_url}{version}/poiCategories.json?language={language}&key={api_key}"
#         try:
#             response = requests.get(url)
#             poi_categories = response.json()["poiCategories"]
#
#             # Filter out only restaurant-related categories
#             restaurant_categories = [category for category in poi_categories if "Food" in category["name"] or "Restaurant" in category["name"]]
#
#             # return JSON3
#             return HttpResponse({"restaurant category": restaurant_categories}, content_type="application/json")
#         except requests.RequestException as e:
#             return HttpResponse(f"Error: {e}", status=500)


def search_restaurants(request):
    if request.method == 'GET':
        # Construct the API request URL with parameters
        api_url = "https://map-places.p.rapidapi.com/nearbysearch/json"
        headers = {
            "X-RapidAPI-Key": api_key2,
            'X-RapidAPI-Host': rapidapi_host,
        }
        params = {
            "location": location_data["latitude"] + ', ' + location_data["longitude"],
            "radius": "5000",
            # "keyword": 'cruise',
            "type": 'restaurant'
            # Add any other parameters as needed
        }

        print(params)

        # Make the API request
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            # Extract relevant data from the response
            restaurants = data.get('results', [])
            # Pass the data to the template
            # print(restaurants)
            result = [print(restaurant["photos"])for restaurant in restaurants]
            return render(request, 'index.html', {'restaurants': restaurants})
        else:
            return HttpResponse(response.status_code)

