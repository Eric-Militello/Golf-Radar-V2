from location import *
from datetime import datetime
from golf import scrape_tee_times
from datetime import datetime

# URLs
golf_base_url = "https://www.golfnow.com/tee-times/search#qc=GeoLocation&q={}&sortby=Facilities.Distance.0&view=Course&date={}&holes={}&radius={}&timemax={}&timemin={}&players={}&pricemax=10000&pricemin=0&promotedcampaignsonly=false&hotdealsonly=false&longitude={}&latitude={}"

# Called when user submits their inputs,
def main(zip_code, range_value, early_time, late_time,min_temp, max_temp, conditions_blacklist, selected_players, selected_holes):
     
     daily_weather_info, lon, lat = get_weather_info(zip_code)  # Call weather API to get weather info for given zip code

     # Create 2 empty lists, 
     # valid_days store which days fit the weather criteria, 
     # valid_days_data store the weather data, tee time data, and search url that will be used to scrape for tee time info
     valid_days = []
     valid_days_data = []

     for day in daily_weather_info:
        # Check if day fits criteria, 'None' returned if it does not, day i
        day_result = valid_day(min_temp, max_temp, conditions_blacklist, day, daily_weather_info) 
        if day_result:
          valid_days.append(day_result)
     #print(valid_days)

     #day will be a list in format ['date', min, max, {'condition1', 'consdition2', etc.. }]
     for day in valid_days:
          search_url = build_search_url(zip_code, convert_day_format(day, '2024'), convert_hole_format(selected_holes), 
                                            convert_range_format(range_value), convert_late_time_format(late_time), 
                                            convert_early_time_format(early_time), convert_selected_players(selected_players), lon, lat)
          tee_time_info = scrape_tee_times(search_url)

          valid_days_data.append({
               'day': format_date_for_gui(day[0]),
               'low_temp': day[1],
               'high_temp' : day[2],
               'condition' : day[3],
               'tee_time_info': tee_time_info,
               'url' : search_url
        })

     return valid_days_data

# Check if day meets given weather criteria return day info it passes and 'None' if it does not    
def valid_day(min_temp, max_temp, conditions_blacklist, day, daily_weather_info):
    day_info = daily_weather_info.get(day, {})  # Get the info for the specified day or an empty dictionary if not found

    # change all conditions to lower to avoid any case sensitivity issues
    conditions = {condition.lower() for condition in day_info.get('conditions', set())}
    blacklist = {condition.lower() for condition in conditions_blacklist}

    #print(f'Day: {day}, Conditions: {conditions}, Blacklist: {blacklist}')

    if (
        day_info
        and float(day_info['min']) >= float(min_temp) # Check daily min is greater than or equal to min temp passed in
        and float(day_info['max']) <= float(max_temp) # Check daily max is less than or equal to max temp passed in
        and not any(condition in blacklist for condition in conditions) # Check that any daily conditions are not in the passed in black list
    ):
        return (day, day_info['min'], day_info['max'], day_info['conditions'])
    else:
        return None

# Convert user input to proper format to build search URL
def convert_hole_format(selected_holes):
    if selected_holes[0] == '08':
        return 2
    elif selected_holes[0] == '9':
        return 1
    else:
         return 3

# Convert user input to proper format to build search URL
def convert_range_format(range_value):
     x = range_value.replace('m', '')
     return x.replace('i', '')

# Convert user input to proper format to build search URL
def convert_late_time_format(late_time):
    if  late_time == 'Any':
        return 42
    elif late_time == '8PM':
         return 40
    elif late_time == '7PM':
         return 38
    elif late_time == '6PM':
         return 36
    elif late_time == '5PM':
         return 34
    elif late_time == '4PM':
         return 32
    elif late_time == '3PM':
         return 30
    elif late_time == '2PM':
         return 28
    elif late_time == '1PM':
         return 26
    elif late_time == '12PM':
         return 24
    elif late_time == '11AM':
         return 22
    elif late_time == '10AM':
         return 20
    elif late_time == '9AM':
         return 18
    elif late_time == '8AM':
         return 16

# Convert user input to proper format to build search URL    
def convert_early_time_format(early_time):
    if early_time == '6PM':
         return 36
    elif early_time == '5PM':
         return 34
    elif early_time == '4PM':
         return 32
    elif early_time == '3PM':
         return 30
    elif early_time == '2PM':
         return 28
    elif early_time == '1PM':
         return 26
    elif early_time == '12PM':
         return 24
    elif early_time == '11AM':
         return 22
    elif early_time == '10AM':
         return 20
    elif early_time == '9AM':
         return 18
    elif early_time == '8AM':
         return 16
    elif early_time == '7AM':
         return 14
    elif early_time == '6AM':
         return 12
    elif early_time == '5AM':
         return 10

# Convert user input to proper format to build search URL    
def convert_selected_players(selected_players):
    if selected_players[0] == 'Any':
          return 0   
    elif selected_players[0] == '1':
        return 1 
    elif selected_players[0] == '2':
        return 2
    elif selected_players[0] == '3':
        return 3
    else:
         return 4   

# Convert user input to proper format to build search URL
def convert_day_format(candidate_day, year='2024'):
    # Map weekday abbreviations to weekday names
    weekday_mapping = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}

    # Check if candidate_day is a tuple
    if isinstance(candidate_day, tuple):
        # Assuming the string is the first element in the tuple
        candidate_day = candidate_day[0]

    # Extract date from candidate_day (assuming it's in the format 'YYYY-MM-DD')
    date_parts = candidate_day.split('-')
    
    # Check if the split operation was successful
    if len(date_parts) == 3:
        year, month, day = date_parts
        formatted_day = f"{month}+{day}+{year}"
        return formatted_day
    else:
        # Handle the case when there are not enough values to unpack
        print(f"Invalid format for candidate day: {candidate_day}")
        return None  # or raise an exception, depending on your needs

# Build URL that matches the inputs passed in
def build_search_url(zip_code, day, selected_holes, range_value, late_time, early_time, selected_players, lon, lat):
      golf_url = golf_base_url.format(zip_code, day, selected_holes, range_value, late_time, early_time, selected_players, lon, lat)
      print(golf_url)
      return golf_url

def format_date_for_gui(input_date):
    # Convert input string to datetime object
    date_object = datetime.strptime(input_date, "%Y-%m-%d")

    # Get the day with suffix (1st, 2nd, 3rd, etc.)
    day_with_suffix = f"{date_object.day}{get_day_suffix_for_gui(date_object.day)}"

    # Format the date as 'Mon DDth'
    formatted_date = date_object.strftime("%b ") + day_with_suffix

    return formatted_date

def get_day_suffix_for_gui(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix


