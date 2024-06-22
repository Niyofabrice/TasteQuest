import requests
from django.conf import settings
from django.core.cache import cache

def get_places_nearby(latitude, longitude, query='', radius=1000):
    cache_key = f"places_{latitude}_{longitude}_{query}_{radius}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    endpoint_url = 'https://api.foursquare.com/v3/places/nearby'
    params = {
        'll': f'{latitude},{longitude}',
        'query': query,
        'radius': radius,
        'client_id': settings.FOURSQUARE_CLIENT_ID,
        'client_secret': settings.FOURSQUARE_CLIENT_SECRET,
        'v': '20210101'  # API version
    }
    response = requests.get(endpoint_url, params=params)
    places = response.json().get('response', {}).get('places', [])
    print(places)

    # Enhance place data with photos
    for place in places:
        place['photos'] = get_place_photos(place['id'])

    cache.set(cache_key, response.json(), timeout=3600)  # Cache for 1 hour
    print(response.json)
    return response.json()

def get_place_photos(place_id, max_photos=5):
    cache_key = f"place_photos_{place_id}"
    cached_photos = cache.get(cache_key)
    if cached_photos:
        return cached_photos
    endpoint_url = f"https://api.foursquare.com/v2/places/{place_id}/photos"
    params = {
        "client_id": settings.FOURSQUARE_CLIENT_ID,
        "client_secret": settings.FOURSQUARE_CLIENT_SECRET,
        "v": "20210101"  # API version
    }
    response = requests.get(endpoint_url, params=params)
    data = response.json()
    
    photos = []
    if "response" in data and "photos" in data["response"]:
        items = data["response"]["photos"]["items"]
        for item in items[:max_photos]:
            photo_url = f"{item['prefix']}300x300{item['suffix']}"  # Adjust size as needed
            photos.append(photo_url)
    cache.set(cache_key, photos, timeout=3600) # Cashe for 1 hour
    return photos