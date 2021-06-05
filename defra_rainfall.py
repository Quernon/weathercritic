# Pulling historic rainfall data from Defra API

import pandas as pd
import datetime
import requests
import io

today = datetime.date.today()

# 
station = '560557'


# URL forms for last 100 readings and today respectively
url_100 = f"http://environment.data.gov.uk/flood-monitoring/id/stations/{station}/readings.csv?_limit=100&_sorted&parameter=rainfall"
url_today = f"http://environment.data.gov.uk/flood-monitoring/id/stations/{station}/readings.csv?today&_sorted&parameter=rainfall"

# Fetches last 100 readings
def defra_historical(station, url):
    
    response = requests.get(url)
    
    if response.ok:
        data = response.content.decode('utf8')
        rainfall_csv = pd.read_csv(io.StringIO(data))
    
    # Convert to datetime and resample to hourly data
    rainfall_csv['dateTime'] = pd.to_datetime(rainfall_csv['dateTime'])
    rainfall_csv.set_index('dateTime', inplace=True)
    rainfall_csv_resample = rainfall_csv.resample('1h').sum()
    rainfall_csv_resample.reset_index(drop=False, inplace=True)
    return rainfall_csv_resample

if __name__ == '__main__':
    defra_csv_100 = defra_historical(station, url_100)
    defra_csv_today = defra_historical(station, url_today)
