# Python script to scrape forecast data from the metoffice
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
def bbc_param(paramdict):
    param_d = {}
    for day in day_list:
        # Create URL from location key and today's date
        url = f"https://www.bbc.co.uk/weather/{location_key}/{day}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        param = soup.findAll('div', paramdict)
        param_list = []
        for p in range(0, len(param)):
            td = param[p].findAll('td', class_=True)
            param_list.append(param[p].text.strip().split('%')[0])
        param_d[day] = param_list
    return param_d

# Probability of precipitaion
bbc_pop = bbc_param({'class':'wr-u-font-weight-500'})

# Feels like temperature
bbc_flt = bbc_param({'class':'wr-value--temperature--c','data-type':'temp'})
