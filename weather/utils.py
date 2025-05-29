import requests
from django.conf import settings

def get_weather_data(latitude, longitude):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': True,
            'hourly': 'temperature_2m,relativehumidity_2m,windspeed_10m',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'auto'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_cities_autocomplete(query):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 5,
            'featuretype': 'city'
        }
        headers = {'User-Agent': 'WeatherApp/1.0'}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        cities = []
        for result in response.json():
            cities.append({
                'name': f"{result['display_name'].split(',')[0]}, {result['display_name'].split(',')[-1]}",
                'latitude': result['lat'],
                'longitude': result['lon']
            })
        return cities
    except requests.RequestException as e:
        print(f"Error fetching city autocomplete: {e}")
        return []