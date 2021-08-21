from dayforecastwithaccuracy import DayForecastWithAccuracy
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dayforecast import DayForecast

app = Flask(__name__)

# uri = os.environ.get('MONGO_URI')
uri = 'mongodb+srv://weatherhenry:btxV7fpcMhTXTpng@weathercritic0.vdy3o.mongodb.net/weathercritic?retryWrites=true&w=majority'


client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client['weathercritic']
collection = db['forecasts']

accuracyKeyName = 'rainfallAccuracyRMS'


@app.route('/forecasts')
def index():
    results = collection.find({})
    resultsList = list(map(withAccuracy, list(results)))
    resultsWithAccuracyOnly = list(filter(
        lambda day: 'bbc' in day and accuracyKeyName in day['bbc'], resultsList))
    response = jsonify(resultsWithAccuracyOnly)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/accuracy')
def accuracy():
    results = collection.find({})
    resultsList = list(map(withAccuracyOnly, list(results)))
    resultsWithAccuracyOnly = list(filter(
        lambda day: day['bbcAccuracy'] != False and day['metAccuracy'] != False, resultsList))

    response = jsonify(resultsWithAccuracyOnly)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/leaguetable')
def leaguetable():
    results = collection.find({})
    resultsList = list(map(withAccuracyOnly, list(results)))
    resultsWithAccuracyOnly = list(filter(
        lambda day: day['bbcAccuracy'] != False and day['metAccuracy'] != False, resultsList))
    bbcWins = 0
    metWins = 0
    draw = 0
    for result in resultsWithAccuracyOnly:
        if result['winner'] == 'bbc':
            bbcWins = bbcWins + 1
        if result['winner'] == 'met':
            metWins = metWins + 1
        if result['winner'] == 'draw':
            draw = draw + 1

    res = {
        'bbcWins': bbcWins,
        'metWins': metWins,
        'draw': draw
    }

    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def withAccuracy(dayForecastDict):
    dayForecast = DayForecast(dayForecastDict)
    dayForecastWithAccuracy = DayForecastWithAccuracy(dayForecast)
    return DayForecastWithAccuracy.asDict(dayForecastWithAccuracy)


def withAccuracyOnly(dayForecastDict):
    dayForecast = DayForecast(dayForecastDict)
    dayForecastWithAccuracy = DayForecastWithAccuracy(dayForecast)
    diction = DayForecastWithAccuracy.asDict(dayForecastWithAccuracy)
    draw = accuracyKeyName in diction['met'] and accuracyKeyName in diction[
        'bbc'] and diction['met'][accuracyKeyName] == diction['bbc'][accuracyKeyName]
    winner = 'met' if accuracyKeyName in diction['met'] and accuracyKeyName in diction[
        'bbc'] and diction['met'][accuracyKeyName] > diction['bbc'][accuracyKeyName] else 'bbc'
    return {
        'date': diction['_id'],
        'bbcAccuracy': diction['bbc'][accuracyKeyName] if accuracyKeyName in diction['bbc'] else False,
        'metAccuracy': diction['met'][accuracyKeyName] if accuracyKeyName in diction['met'] else False,
        'winner': 'draw' if draw else winner
    }


def calculateRainfallAccuracy(forecastedRainfall, actualRainfall):
    accuracy = 1
    for hour in forecastedRainfall:
        if forecastedRainfall[hour] != actualRainfall[hour]:
            accuracy = accuracy - 1/24
    print(accuracy)
