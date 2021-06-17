# Pulling historic rainfall data from Defra API

import pandas as pd
import datetime
import requests
import io

today = datetime.date.today()

# Ashton-Upon-Mersey 
station = '560557'



# Fetches last 100 readings
def historical_rainfall(station, date):
    url = f'http://environment.data.gov.uk/flood-monitoring/id/stations/560557/readings.csv?date={date}'
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
    defra_csv = historical_rainfall(station, '2021-06-01')
    