import requests
import json
opentopokey = '215aefe5ec11696b8fd31cf5ecbc10a9'
def get_elevation(lat, lng, api_key):
    """Get the elevation of a specific latitude and longitude using Google Elevation API."""
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={api_key}"
    
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        return data["results"][0]["elevation"]
    else:
        print("Error:", data["status"])
        return None

# Example Usage
api_key = 'XEUZuUPwMR1@X9X!rle6_OBF2wOAbyARZ_rfmRkHIvDBoQJBQZOJncfQ9Sm4M87I'
latitude = 40.714728
longitude = -73.998672

elevation = get_elevation(latitude, longitude, api_key)
print(f"The elevation at latitude {latitude}, longitude {longitude} is {elevation} meters.")
