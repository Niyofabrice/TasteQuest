import requests

def get_location():
    try:
        # Send a GET request to the IP Geolocation API
        response = requests.get("http://ip-api.com/json/")
        data = response.json()

        # Extract latitude and longitude
        latitude = data['lat']
        longitude = data['lon']

        return latitude, longitude
    except Exception as e:
        print("Error:", e)


# Get and print location
latitude, longitude = get_location()
print("Latitude:", latitude)
print("Longitude:", longitude)