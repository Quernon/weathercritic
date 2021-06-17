from pymongo import MongoClient
from datetime import date, timedelta
from dayforecast import DayForecast
from defra_rainfall import historical_rainfall

uri = "mongodb+srv://weathercritic0.vdy3o.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='weathercritic_mongodb.pem')

# Rainfall station for Ashton-upon-Mersey
station = '560557'

def insert_yesterdays_data(yesterday=True, date=None):
    db = client['weathercritic']
    collection = db['forecasts']
    
    if yesterday:
        # Get yesterdays date as a string
        today = date.today()
        yesterday = str(today - timedelta(days = 1))
        date=yesterday
    elif type(date) == str:
        pass
    else:
        print('Select either yesterday or input a date as a string.')
        exit()
    
    
    # Scrape actual rain data
    actual_pop = historical_rainfall(station, date)
    
    # Format scraped data into dictionary of hour:value pairs
    actual_pop.drop(columns=['dateTime'], inplace=True)
    actual_pop = actual_pop.to_dict()
    actual_pop = actual_pop['value']
    actual_pop = {str(key): value for key, value in actual_pop.items()}


    # Create DB query and define updated values
    filters = {'_id':date}
    newvalues = {'$set':{'actual':{'rainfallHourly':actual_pop}}}
    
    # Update values
    collection.update_one(filters, newvalues)
    
    return
    
if __name__ == '__main__':
    test_day = insert_yesterdays_data(yesterday=False, date = '2021-06-07')