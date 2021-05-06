# Python script to scrape forecast data from the metoffice

import requests
from bs4 import BeautifulSoup
import datetime

# Scrape met office data and save probability of precipiation forecast to dictionary
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

# Location key corresponding to Manchester
location_key = 'gcw2hzs1u'

# Create URL from location key and today's date
url = f"https://www.metoffice.gov.uk/weather/forecast/{location_key}#?date={str(today)}"

# Function to scrape forecast data from URL given parameter names
def metoffice_param(url, paramdict):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    parse_today = soup.findAll('div', {"id":str(today)})
    parse_tomorrow = soup.findAll('div', {'id':str(tomorrow)})
    param = soup.findAll('tr', paramdict)
    param_d = {}
    for p in range(0, len(param)):
        td = param[p].findAll('td', class_=True)
        param_list = []
        for i in range(0,len(td)):
            param_list.append(param[p].findAll('td', class_=True)[i].text.strip())
        param_d[p] = param_list
    return param_d

# Probability of precipitaion
met_pop = metoffice_param(url, {'class':'step-pop'})

# Feels like temperature
met_flt = metoffice_param(url, {'class':'detailed-view','data-type':'temp'})
