import requests
from datetime import datetime

# Read API key from config.txt file
with open('config.txt', 'r') as file:
    # Read the entire file
    content = file.read()

    # Use regular expressions to extract the API key
    import re
    match = re.search(r"API_Key='(.+)'", content)
    
    if match:
        API_key = match.group(1)
        print("API Key:", API_key)
    else:
        print("API key not found in the config.txt file.")


def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9/5 + 32, 1)

#convert zip code to longitude and latitude cordinates for API call
def convert_zip(zip_code):
    country_code = 'US'

    #URL for API call to convert zip
    url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={API_key}'

    r = requests.get(url)

    if r.status_code != 200:
        print(f'Error: {r.status_code}')
    else:
        data = r.json()
        #return lon and lat cordinates for use in next API call
        return (data.get('lon'), data.get('lat'))

#Get daily min temp, max temp, and conditions for given zip code (Must be US zipcode)
def get_weather_info(zip_code):
    
    #convert zip to cordinates for API Call
    lon, lat = convert_zip(zip_code)

    #URL for weather data API call
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}'

    r = requests.get(url)

    if r.status_code != 200:
        print(f'Error: {r.status_code}')
    else:
        data = r.json()
        # Dictionary to store daily temperature information
        daily_info = {}

        # Extract data from json
        # Data format is a series of weather information taken every three hours
        for list_data in data.get("list"):
            time = datetime.utcfromtimestamp(list_data.get('dt'))
            date_str = time.strftime("%Y-%m-%d")  # Extracting the date as a string

            temp_min = kelvin_to_fahrenheit(list_data.get("main").get("temp_min"))
            temp_max = kelvin_to_fahrenheit(list_data.get("main").get("temp_max"))
            condition = list_data.get('weather')[0]['main']

            # Update daily temperature information, Each day is own entry in the dictonary, lowest min and highest max taken for each day, all the condition words are made into a list
            if date_str not in daily_info:
                daily_info[date_str] = {'min': temp_min, 'max': temp_max, 'conditions': {condition}}  # Create new day entry
            else:
                daily_info[date_str]['min'] = min(daily_info[date_str]['min'], temp_min)  # Update daily min temp
                daily_info[date_str]['max'] = max(daily_info[date_str]['max'], temp_max)  # Update daily max temp 
                daily_info[date_str]['conditions'].add(condition)  # Add Condition to daily conditions list
        

        return daily_info, lon, lat