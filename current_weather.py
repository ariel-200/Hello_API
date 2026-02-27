import requests
import os

geocoder_url = 'https://api.openweathermap.org/geo/1.0/direct'
weather_url = 'https://api.openweathermap.org/data/2.5/weather'
api_key = os.getenv('WEATHER_KEY')


def main():
    location = get_location()
    coordinates, error = get_geocode_data(location)
    if error:
        print('Sorry, could not get geocode')
        return
    lat, lon = get_lat_lon(coordinates)
    if None in (lat, lon):
        print('Sorry, could not get coordinates')
        return
    weather_data, error = get_current_weather(lat, lon, api_key)
    if error:
        print('Sorry, could not get weather')
        return
    current_temp = get_temp(weather_data)
    print(f'The current temperature is {round(current_temp, 2)}F.')


def get_location():
    city, state, country = '', '', ''

    while len(city) == 0:
        city = input('Enter the city name: ').strip()
    while len(state) != 2 or not state.isalpha():
        state = input('Enter the 2-letter state code: ').strip().upper()
    while len(country) != 2 or not country.isalpha():
        country = input('Enter the 2-letter country code: ').strip().upper()

    location = f'{city},{state},{country}'
    return location


def get_geocode_data(location):
    try:
        params = {'q': location, 'limit': 1, 'appid': api_key}
        response = requests.get(geocoder_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            print('Sorry, location could not be found')
            return None, ValueError('No geocode results found')
        return data[0], None
    except Exception as ex:
        print(ex)
        return None, ex


def get_lat_lon(geocoder_data):
    try:
        return geocoder_data['lat'], geocoder_data['lon']
    except (TypeError, KeyError):
        print('This data is not in the format expected')
        return None, None


def get_current_weather(lat, lon, key):
    try:
        weather_query = {'lat': lat, 'lon': lon, 'units': 'imperial', 'appid': key}
        response = requests.get(weather_url, params=weather_query, timeout=10)
        response.raise_for_status() # Raise exception for 400 or 500 errors
        data = response.json()
        return data, None
    except Exception as ex:
        print(ex)
        return None, ex


def get_temp(weather_data):
    try:
        temp = weather_data['main']['temp']
        return temp
    except KeyError:
        print('This data is not in the format expected')
    return None


if __name__ == '__main__':
    main()
