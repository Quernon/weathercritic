# Pulling historic rainfall data from Defra API

import pandas as pd
import datetime
import requests
import io

today = datetime.date.today()

station = '560557'

url = f"http://environment.data.gov.uk/flood-monitoring/data/readings.csv?date={str(today)}"

response = requests.get(url)

if response.ok:
    data = response.content.decode('utf8')
    rainfall_csv = pd.read_csv(io.StringIO(data))

# Fetches last 100 readings
url = f"http://environment.data.gov.uk/flood-monitoring/id/stations/{station}/readings.csv?_limit=100&_sorted&parameter=rainfall"

response = requests.get(url)

if response.ok:
    data = response.content.decode('utf8')
    rainfall_csv100 = pd.read_csv(io.StringIO(data))
    
# Fetches today's readings
url = f"http://environment.data.gov.uk/flood-monitoring/id/stations/{station}/readings.csv?today&_sorted&parameter=rainfall"

response = requests.get(url)

if response.ok:
    data = response.content.decode('utf8')
    rainfall_csv_today = pd.read_csv(io.StringIO(data))
    
rainfall_csv_today['dateTime'] =  pd.to_datetime(rainfall_csv_today['dateTime'])

