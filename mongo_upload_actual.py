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
    
    # Create document to contain rainfall data    
    test_day = DayForecast()
    test_day.actual.rainfallHourly = actual_pop
    test_day.actual = vars(test_day.actual)
    
    
    # Create DB query and define updated values
    filters = {'_id':date}
    newvalues = {'$set':{'actual':{'rainfallHourly':test_day.actual['rainfallHourly']['value'].to_dict()}}}
    
    
    collection.update_one(filters, newvalues)
    
    return test_day
    
if __name__ == '__main__':
    test_day = insert_yesterdays_data(yesterday=False, date = '2021-06-07')