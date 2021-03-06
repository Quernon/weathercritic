from forecast import Forecast


def hasAllKeys(forecast):
    hasAll = True
    for i in range(24):
        if not str(i) in forecast:
            hasAll = False
    return hasAll


class ForecastWithAccuracy(Forecast):
    accuracy = {
        'rainfall': None,
        'temp': None
    }

    def __init__(self, forecast, actual):
        if forecast['rainfallHourly'] and hasAllKeys(forecast['rainfallHourly']) and actual['rainfallHourly'] and hasAllKeys(actual['rainfallHourly']):
            self.rainfallHourly = forecast['rainfallHourly']
            self.calculateRainfallAccuracyRMS(forecast, actual)

        if forecast['tempHourly'] and hasAllKeys(forecast['tempHourly']) and actual['tempHourly'] and hasAllKeys(actual['tempHourly']):
            self.tempHourly = forecast['tempHourly']
            tempAccuracy = 1
            for hour in forecast['tempHourly']:
                predictedTempString = forecast['tempHourly'][hour].replace(
                    '°', '')
                predictedTemp = int(predictedTempString)
                actualTemp = actual['tempHourly'][hour]
                diff = abs(predictedTemp - actualTemp)
                scaledDiff = 1/24 * min((1/20 * diff), 1)
                tempAccuracy = tempAccuracy - scaledDiff
            self.tempAccuracy = tempAccuracy
            # self.accuracy = tempAccuracy

    def calculateRainfallAccuracyBasic(self, forecast, actual):
        rainfallAccuracy = 1
        for hour in forecast['rainfallHourly']:
            predictedTempString = forecast['rainfallHourly'][hour].replace(
                '%', '').replace('<5', '0').replace('≥95', '100')
            chanceOfRain = int(predictedTempString)
            actualRainfall = actual['rainfallHourly'][hour]
            # if (chanceOfRain < 10 and actualRainfall > 0.2) or (chanceOfRain > 10 and actualRainfall < 0.2):
            if (chanceOfRain < 20 and actualRainfall > 0.4) or (chanceOfRain > 20 and actualRainfall < 0.4):
                rainfallAccuracy = rainfallAccuracy - 1/24
        self.rainfallAccuracy = rainfallAccuracy
        self.accuracy = rainfallAccuracy

    def calculateRainfallAccuracyRMS(self, forecast, actual):
        hourlyRMS = []
        for hour in forecast['rainfallHourly']:
            predictedTempString = forecast['rainfallHourly'][hour].replace(
                '%', '').replace('<5', '0').replace('≥95', '100')
            chanceOfRain = float(predictedTempString) / 100
            actualRainfall = actual['rainfallHourly'][hour]
            if actualRainfall > 0:
                binaryActualRainfall = 1
            else:
                binaryActualRainfall = 0
            hourlyRMS.append((chanceOfRain - binaryActualRainfall) ** 2)
        rainfallAccuracyRMS = sum(hourlyRMS) ** 0.5
        self.rainfallAccuracyRMS = rainfallAccuracyRMS
