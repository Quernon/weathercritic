# Git push test
# Python script to scrape forecast data from BBC weather
import requests
from bs4 import BeautifulSoup
import datetime

# Scrape met office data and save probability of precipiation forecast to dictionary
today = datetime.date.today()

# Location key corresponding to Manchester
location_key = '2643123'

# Day list, used to cycle through pages on BBC weather
day_list = ['today', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 
            'day8', 'day9', 'day10', 'day11', 'day12', 'day13']

# Function to scrape forecast data from URL given parameter names
def bbc_param(tag, paramdict, denominator):
    param_d = {}
    for day in day_list:
        # Create URL from location key and today's date
        url = f"https://www.bbc.co.uk/weather/{location_key}/{day}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        param = soup.findAll(tag, paramdict)
        param_list = {}
        for hour in range(0, len(param)):
            param_list[str(hour)] = param[hour].text.strip().split(denominator)[0]
        param_d[day] = param_list    
    tomorrow = param_d['day1']    
    return tomorrow


if __name__ == '__main__':
    # Probability of precipitaion
    bbc_pop = bbc_param('div', {'class':'wr-u-font-weight-500'}, '%')
    print(bbc_pop)
    
    # Actual temperature
    bbc_temp = bbc_param('span', {'class':'wr-value--temperature wr-temperature--time-slot'}, '°')
    print(bbc_temp)
