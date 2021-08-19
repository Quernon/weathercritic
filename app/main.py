from app.dayforecastwithaccuracy import DayForecastWithAccuracy
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from forecast import Forecast
from dayforecast import DayForecast
from forecastwithaccuracy import ForecastWithAccuracy

app = Flask(__name__)

uri = os.environ.get('MONGO_URI')

client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client['weathercritic']
collection = db['forecasts']


@app.route('/forecasts')
def index():
    results = collection.find({})
    resultsList = list(map(withAccuracy, list(results)))
    resultsWithAccuracyOnly = list(filter(
        lambda day: 'bbc' in day and 'accuracy' in day['bbc'], resultsList))
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
    draw = 'accuracy' in diction['met'] and 'accuracy' in diction[
        'bbc'] and diction['met']['accuracy'] == diction['bbc']['accuracy']
    winner = 'met' if 'accuracy' in diction['met'] and 'accuracy' in diction[
        'bbc'] and diction['met']['accuracy'] > diction['bbc']['accuracy'] else 'bbc'
    return {
        'date': diction['_id'],
        'bbcAccuracy': diction['bbc']['accuracy'] if 'accuracy' in diction['bbc'] else False,
        'metAccuracy': diction['met']['accuracy'] if 'accuracy' in diction['met'] else False,
        'winner': 'draw' if draw else winner
    }


def calculateRainfallAccuracy(forecastedRainfall, actualRainfall):
    accuracy = 1
    for hour in forecastedRainfall:
        if forecastedRainfall[hour] != actualRainfall[hour]:
            accuracy = accuracy - 1/24
    print(accuracy)
