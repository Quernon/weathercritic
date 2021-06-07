# Python script to scrape forecast data from the metoffice

import requests
from bs4 import BeautifulSoup
import datetime

# Scrape met office data and save probability of precipiation forecast to dictionary
today = datetime.date.today()

# Location key corresponding to Manchester
location_key = 'gcw2hzs1u'

# Create URL from location key and today's date
url = f"https://www.metoffice.gov.uk/weather/forecast/{location_key}#?date={str(today)}"

# Function to scrape forecast data from URL given parameter names
def metoffice_param(url, paramdict):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    param = soup.findAll('tr', paramdict)
    param_d = {}
    for day in range(0, len(param)):
        all_tds = param[day].findAll('td')
        param_list = {}
        for hour, td in enumerate(all_tds):
            param_list[str(hour)] = td.text.strip()
        param_d[day] = param_list
    tomorrow=param_d[1]
    return tomorrow


if __name__ == '__main__':
    # Probability of precipitaion
    met_pop = metoffice_param(url, {'class':'step-pop'})
    
    # Actual temperature
    met_temp = metoffice_param(url, {'class':'step-temp','data-type':'temp'})
