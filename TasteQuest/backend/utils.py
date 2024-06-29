import requests


headers = {
    "accept": "application/json",
    "Authorization": "fsq3DpPCdy4UqMmMs9u+pdWD9xUr8NpdjTOwFqdF/ru7b18="
}

categories = "4bf58dd8d48988d1e2931735,4bf58dd8d48988d1fa931735,5bae9231bedf3950379f89cb,63be6904847c3692a84b9c27,63be6904847c3692a84b9c22,58daa1558bbb0b01f18ec1ae,63be6904847c3692a84b9c13,4d4b7105d754a06374d81259,4bf58dd8d48988d128941735,4bf58dd8d48988d1e0931735,4bf58dd8d48988d16d941735,52e81612bcbc57f1066b7a0c,4bf58dd8d48988d143941735,4bf58dd8d48988d121941735,4bf58dd8d48988d16e941735"

def get_places_nearby(query='', radius=5000):
    endpoint_url = 'https://api.foursquare.com/v3/places/nearby'
    #endpoint_url = 'https://api.foursquare.com/v3/places/search'
    params = {
        'query': query,
        'radius': radius,
        'categories': categories,
        'fields': "fsq_id,name,geocodes,location,categories,closed_bucket,description,tel,email,website,social_media,hours,hours_popular,rating,popularity,price,menu,date_closed,photos,tastes"
    }
    response = requests.get(endpoint_url, headers=headers, params=params)
    return response.json()
