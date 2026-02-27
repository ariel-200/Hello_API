import os
import requests
from datetime import datetime

# Minneapolis
lat = 44.97
lon = -93.26
units = 'imperial'


# Error Handling for KeyError if api key not found
api_key = os.environ['WEATHER_KEY']  # Set this environment variable on your computer

url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={units}&appid={api_key}'

# Error Handling for ConnectionError if server is down, or no internet.
response = requests.get(url)
weather_forecast = response.json()

# Error Handling for KeyError if missing or wrong keys, typos
list_forecast = weather_forecast['list']
for forecast in list_forecast:
    temp = forecast['main']['temp']
    timestamp = forecast['dt']
    weather_description = forecast['weather'][0]['description']
    wind_speed = forecast['wind']['speed']
    date = datetime.fromtimestamp(timestamp).strftime("%m-%d-%Y at %I:%M %p")
    print(f'In Minneapolis, on {date}, the temperature will be {temp:.2f}F.\n'
    f'The weather will be {weather_description}, and the wind speed will be {wind_speed:.2f} mph.\n')

