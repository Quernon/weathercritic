from pymongo import MongoClient
from datetime import datetime
from dayforecast import DayForecast
from metoffice import metoffice_param
from bbc import bbc_param

uri = "mongodb+srv://weathercritic0.vdy3o.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='weathercritic_mongodb.pem')

def insert_tomorrows_forecast():
    db = client['weathercritic']
    collection = db['forecasts']

    location_key = 'gcw2hzs1u'
    url = f"https://www.metoffice.gov.uk/weather/forecast/{location_key}"
    met_temp = metoffice_param(url, {'class':'step-temp','data-type':'temp'})
    met_pop = metoffice_param(url, {'class':'step-pop'})

    bbc_pop = bbc_param('div', {'class':'wr-u-font-weight-500'}, '%')
    bbc_temp = bbc_param('span', {'class':'wr-value--temperature wr-temperature--time-slot'}, '°')

    test_day_forecast = DayForecast();

    test_day_forecast.met.tempHourly = met_temp
    test_day_forecast.met.rainfallHourly = met_pop
    test_day_forecast.bbc.tempHourly = bbc_temp
    test_day_forecast.bbc.rainfallHourly = bbc_pop

    test_day_forecast.met = vars(test_day_forecast.met)
    test_day_forecast.bbc = vars(test_day_forecast.bbc)
    test_day_forecast.actual = vars(test_day_forecast.actual)
    document = vars(test_day_forecast)

    print(document)

    post_id = collection.insert_one(document).inserted_id
    print(post_id)  

    # to replace a document that is already there, do this instead - eventually we can write code that will either insert or replace depending on whether a document with that _id exists already (we are using the date as the _id or unique id of the document)
    # post_id = collection.replace_one({'_id': document['_id']}, document).upserted_id
    # print(post_id)
    return post_id

if __name__ == '__main__':
    insert_tomorrows_forecast()