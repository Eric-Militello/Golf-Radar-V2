import requests
from datetime import datetime

API_key = 'b9d1b739b6f7ca724d497b532df3a988'

def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9/5 + 32, 1)

def convert_zip(zip_code):
    country_code = 'US'
    url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={API_key}'
    r = requests.get(url)

    if r.status_code != 200:
        print(f'Error: {r.status_code}')
    else:
        data = r.json()
        return (data.get('lon'), data.get('lat'))


def get_weather_info(zip_code):
    
    lon, lat = convert_zip(zip_code)

    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}'

    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        city = data.get("city").get('name')

        # Dictionary to store daily temperature information
        daily_info = {}

        for list_data in data.get("list"):
            time = datetime.utcfromtimestamp(list_data.get('dt'))
            date_str = time.strftime("%Y-%m-%d")  # Extracting the date as a string

            temp_min = kelvin_to_fahrenheit(list_data.get("main").get("temp_min"))
            temp_max = kelvin_to_fahrenheit(list_data.get("main").get("temp_max"))
            condition = list_data.get('weather')[0]['main']

            # Update daily temperature information
            if date_str not in daily_info:
                daily_info[date_str] = {'min': temp_min, 'max': temp_max, 'conditions': {condition}}
            else:
                daily_info[date_str]['min'] = min(daily_info[date_str]['min'], temp_min)
                daily_info[date_str]['max'] = max(daily_info[date_str]['max'], temp_max)
                daily_info[date_str]['conditions'].add(condition)
        print(city)
        #print(daily_info)
        return daily_info
    else:
        print(f'Error: {r.status_code}')

