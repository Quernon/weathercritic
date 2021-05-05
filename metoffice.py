# Python script to scrape forecast data from the metoffice

import requests
from bs4 import BeautifulSoup
import datetime

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

location_key = 'gcw2hzs1u'

url = f"https://www.metoffice.gov.uk/weather/forecast/{location_key}#?date={str(today)}"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

parse_today = soup.findAll('div', {"id":str(today)})

parse_tomorrow = soup.findAll('div', {'id':str(tomorrow)})
