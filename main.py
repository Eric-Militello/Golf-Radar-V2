from location import *
from datetime import datetime, timedelta, date
import calendar
from golf import scrape_tee_times
from datetime import datetime
import re

# URLs
golf_base_url = "https://www.golfnow.com/tee-times/search#qc=GeoLocation&q={}&sortby=Facilities.Distance.0&view=Course&date={}&holes={}&radius={}&timemax={}&timemin={}&players={}&pricemax=10000&pricemin=0&promotedcampaignsonly=false&hotdealsonly=false&longitude=-74.8223&latitude=39.8637"


def main(zip_code, range_value, early_time, late_time,min_temp, max_temp, conditions_blacklist, selected_players, selected_holes):
     # Call weather API
     daily_weather_info = get_weather_info(zip_code)
     valid_days = []
     for day in daily_weather_info:
        day_result = valid_day(min_temp, max_temp, conditions_blacklist, day, daily_weather_info)
        if day_result:
          valid_days.append(day_result)
     for day in valid_days:
          scrape_tee_times(build_search_url(zip_code, convert_day_format(day, '2024'), convert_hole_format(selected_holes), 
                                            convert_range_format(range_value), convert_late_time_format(late_time), 
                                            convert_early_time_format(early_time), convert_selected_players(selected_players)))




    
def valid_day(min_temp, max_temp, conditions_blacklist, day, daily_weather_info):
    day_info = daily_weather_info.get(day, {})  # Get the info for the specified day or an empty dictionary if not found

    conditions = {condition.lower() for condition in day_info.get('conditions', set())}
    blacklist = {condition.lower() for condition in conditions_blacklist}

    print(f'Day: {day}, Conditions: {conditions}, Blacklist: {blacklist}')

    if (
        day_info
        and float(day_info['min']) >= float(min_temp)
        and float(day_info['max']) <= float(max_temp)
        and not any(condition in blacklist for condition in conditions)
    ):
        return (day, day_info['min'], day_info['max'], day_info['conditions'])
    else:
        return None




def convert_hole_format(selected_holes):
    if selected_holes[0] == '08':
        return 2
    elif selected_holes[0] == '9':
        return 1
    else:
         return 3

def convert_range_format(range_value):
     x = range_value.replace('m', '')
     return x.replace('i', '')

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



def build_search_url(zip_code, day, selected_holes, range_value, late_time, early_time, selected_players):
      golf_url = golf_base_url.format(zip_code, day, selected_holes, range_value, late_time, early_time, selected_players,)
      return golf_url








