import requests
from datetime import datetime

def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9/5 + 32, 1)

API_key = 'b9d1b739b6f7ca724d497b532df3a988'
lat = '39.8662'
lon = '-74.8390'

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

        # Print the information for each element in the "list"
        print(time)
        print(f'city: {city} min: {temp_min}°F max: {temp_max}°F | {condition}')
        print('-' * 30)

    # Print the daily temperature information
    print('\nDaily Temperature Information:')
    for date, info in daily_info.items():
         print(f'{date}: Min: {info["min"]}°F, Max: {info["max"]}°F, Conditions: {", ".join(info["conditions"])}')

else:
    print(f'Error: {r.status_code}')



